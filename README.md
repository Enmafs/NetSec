# 🔐 NetSec — Network Security Attacks Lab

**Estudiante:** Enmanuel Feliz Soto  
**Matrícula:** 20251402  
**Institución:** Instituto Tecnológico de Las Américas (ITLA)  
**Curso:** Seguridad en Redes  

[![GitHub](https://img.shields.io/badge/GitHub-Enmafs%2FNetSec-blue?logo=github)](https://github.com/Enmafs/NetSec)
[![YouTube](https://img.shields.io/badge/YouTube-Playlist-red?logo=youtube)](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj)
[![Python](https://img.shields.io/badge/Python-3.x-yellow?logo=python)](https://python.org)
[![Scapy](https://img.shields.io/badge/Scapy-2.5+-green)](https://scapy.net)

---

## 📋 Objetivo del Laboratorio

Demostrar la ejecución práctica de ataques de seguridad a nivel de **Capa 2** y **Capa 3** del modelo OSI sobre una topología de red empresarial simulada en **PNetLab**, utilizando scripts Python con la librería Scapy. Cada ataque incluye su respectiva contra-medida aplicada sobre dispositivos Cisco.

---

## 🗺️ Topología de Red

> Simulada en PNetLab con dispositivos Cisco IOL y contenedores Docker (kalinet/desktop) como hosts atacantes.

![Topología]<img width="1297" height="652" alt="image" src="https://github.com/user-attachments/assets/6a56f798-cf04-4a6e-a4ba-34aa002630cb" />


### Dispositivos

| Dispositivo | Rol | Interfaces Clave |
|-------------|-----|-----------------|
| R1-Core | Router Core / Gateway Internet | e0/0 (DHCP ISP), e0/2, e0/3 |
| R2 | Router de distribución | e0/0 (trunk), e0/1 (trunk), e0/3 |
| SW1 | Switch distribución / VTP Server | e0/0-1 (EtherChannel), e0/2, e0/3 |
| SW2 | Switch de acceso / VTP Client | e0/0-1 (EtherChannel), e0/2 |
| SWM1 | Switch multicapa distribución | e0/0-1 (trunk a R1-Core) |
| SWM2 | Switch multicapa distribución | e0/0-3 (EtherChannel con SWM1) |
| SWAC1-3 | Switches de acceso | e0/0-1 (uplink), e0/2 (acceso) |
| Docker | Hosts atacantes / víctimas | eth0/eth1 |

### Direccionamiento IP (basado en matrícula 20251402)

> 🖥️ Topología simulada en **PNetLab** con dispositivos Cisco IOL (IOS on Linux) y contenedores Docker `kalinet/desktop` como hosts atacantes/víctimas.

| Subred / Uso | Hosts | CIDR | Máscara | Dir. Red | Primera IP | Última IP | Broadcast |
|---|---|---|---|---|---|---|---|
| VLAN 10: Usuarios | 120 | /25 | 255.255.255.128 | 14.2.0.0 | 14.2.0.1 | 14.2.0.126 | 14.2.0.127 |
| VLAN 20: Gestión | 30 | /27 | 255.255.255.224 | 14.2.0.128 | 14.2.0.129 | 14.2.0.158 | 14.2.0.159 |
| VLAN 30: Servidores | 14 | /28 | 255.255.255.240 | 14.2.0.160 | 14.2.0.161 | 14.2.0.174 | 14.2.0.175 |
| VLAN 40: VoIP | 6 | /29 | 255.255.255.248 | 14.2.0.176 | 14.2.0.177 | 14.2.0.182 | 14.2.0.183 |
| VLAN 50: DMZ | 6 | /29 | 255.255.255.248 | 14.2.0.184 | 14.2.0.185 | 14.2.0.190 | 14.2.0.191 |
| Mgmt Router 1 | 6 | /29 | 255.255.255.248 | 14.2.0.192 | 14.2.0.193 | 14.2.0.198 | 14.2.0.199 |
| Mgmt Router 2 | 6 | /29 | 255.255.255.248 | 14.2.0.200 | 14.2.0.201 | 14.2.0.206 | 14.2.0.207 |
| Enlace P2P #1 | 2 | /30 | 255.255.255.252 | 14.2.0.208 | 14.2.0.209 | 14.2.0.210 | 14.2.0.211 |
| Enlace P2P #2 | 2 | /30 | 255.255.255.252 | 14.2.0.212 | 14.2.0.213 | 14.2.0.214 | 14.2.0.215 |
| Enlace P2P #3 | 2 | /30 | 255.255.255.252 | 14.2.0.216 | 14.2.0.217 | 14.2.0.218 | 14.2.0.219 |
| Enlace P2P #4 | 2 | /30 | 255.255.255.252 | 14.2.0.220 | 14.2.0.221 | 14.2.0.222 | 14.2.0.223 |
| Enlace P2P #5 | 2 | /30 | 255.255.255.252 | 14.2.0.224 | 14.2.0.225 | 14.2.0.226 | 14.2.0.227 |

---

## ⚙️ Requisitos Generales

```bash
# Instalar dependencias
pip install scapy

# Todos los scripts requieren root
sudo python3 <script>.py
```

---

## 🚨 Scripts de Ataques

---

### 1. 💥 CDP DoS — CDP Flooding Attack

**Archivo:** `EnmanuelFelizSoto_20251402_CDP_DoS_P1.py`

Inunda la tabla de vecinos CDP del dispositivo objetivo con miles de entradas falsas, agotando su memoria y CPU hasta causar denegación de servicio.

**Uso:**
```bash
sudo python3 EnmanuelFelizSoto_20251402_CDP_DoS_P1.py -i eth0 --delay 0.01
```

**Parámetros:**

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `-i / --iface` | Interfaz de red | `eth0` |
| `-c / --count` | Número de paquetes (0=infinito) | `0` |
| `--delay` | Delay entre paquetes (segundos) | `0.01` |

**Contra-medida:**
```
SW(config)# no cdp run
SW(config-if)# no cdp enable
```

---

### 2. 🕵️ ARP MitM — ARP Poisoning

**Archivo:** `EnmanuelFelizSoto_20251402_ARP_MitM_P1.py`

Envenena la caché ARP de la víctima y el gateway para posicionarse como Man-in-the-Middle e interceptar el tráfico de red.

**Uso:**
```bash
sudo python3 EnmanuelFelizSoto_20251402_ARP_MitM_P1.py -i eth0 -t 14.2.0.10 -g 14.2.0.1
```

**Parámetros:**

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `-i / --iface` | Interfaz de red | `eth0` |
| `-t / --target` | IP de la víctima | — |
| `-g / --gateway` | IP del gateway | — |
| `--interval` | Segundos entre envíos | `2.0` |

**Contra-medida:**
```
SW(config)# ip dhcp snooping
SW(config)# ip arp inspection vlan 10,20,30
SW(config-if)# ip arp inspection trust
```

---

### 3. 🎭 DHCP Spoofing — Rogue DHCP Server

**Archivo:** `EnmanuelFelizSoto_20251402_DHCP_Spoofing_P1.py`

Levanta un servidor DHCP falso que responde antes que el legítimo, entregando gateway y DNS maliciosos a los clientes.

**Uso:**
```bash
sudo python3 EnmanuelFelizSoto_20251402_DHCP_Spoofing_P1.py \
  -i eth0 \
  --server-ip 14.2.0.50 \
  --gateway 14.2.0.50 \
  --dns 14.2.0.50 \
  --pool 14.2.0.60-14.2.0.100
```

**Parámetros:**

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `-i / --iface` | Interfaz de red | `eth0` |
| `--server-ip` | IP del servidor rogue | `192.168.1.50` |
| `--gateway` | Gateway malicioso | `192.168.1.50` |
| `--dns` | DNS malicioso | `192.168.1.50` |
| `--pool` | Rango de IPs a entregar | `...100-...200` |
| `--lease-time` | Tiempo de lease en segundos | `3600` |

**Contra-medida:**
```
SW(config)# ip dhcp snooping
SW(config)# ip dhcp snooping vlan 10,20,30
SW(config-if)# ip dhcp snooping trust      ← solo puerto hacia servidor legítimo
SW(config-if)# ip dhcp snooping limit rate 15
```

---

### 4. 🌊 DHCP Starvation

**Archivo:** `EnmanuelFelizSoto_20251402_DHCP_Starvation_P1.py`

Agota el pool de direcciones IP del servidor DHCP legítimo enviando solicitudes con MACs aleatorias, impidiendo que clientes reales obtengan configuración.

**Uso:**
```bash
sudo python3 EnmanuelFelizSoto_20251402_DHCP_Starvation_P1.py
# (modo interactivo — selecciona interfaz y parámetros)
```

**Parámetros interactivos:**

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| Interfaz | Interfaz de red | `eth0` |
| Cantidad | Clientes falsos a generar | `200` |
| Pausa | Segundos entre intentos | `0.02` |
| Timeout OFFER | Espera por respuesta OFFER | `0.60s` |
| Timeout ACK | Espera por respuesta ACK | `0.40s` |

**Captura del ataque:**

![DHCP Starvation](screenshots/dhcp_starvation.png)

> Pool agotado: 20 solicitudes enviadas, 0 OFFER recibidos — servidor DHCP sin IPs disponibles.

**Contra-medida:**
```
SW(config-if)# ip dhcp snooping limit rate 15
SW(config-if)# switchport port-security maximum 5
SW(config-if)# switchport port-security violation restrict
```

---

### 5. 🌀 MAC Flooding

**Archivo:** `EnmanuelFelizSoto_20251402_MAC_Flooding_P1.py`

Satura la tabla CAM del switch con MACs falsas hasta que el switch entra en modo fail-open (broadcast), permitiendo capturar tráfico de otros hosts.

**Uso:**
```bash
sudo python3 EnmanuelFelizSoto_20251402_MAC_Flooding_P1.py -i eth1 -c 15000
```

**Parámetros:**

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `-i / --interface` | Interfaz de red | requerido |
| `-c / --count` | Cantidad de frames | `1000` |
| `-d / --delay` | Retraso entre frames | `0.0` |

**Captura del ataque:**

![MAC Flooding](screenshots/mac_flooding.png)

> Tabla CAM de SW2 con 109 entradas dinámicas en VLAN 10 — todas aprendidas desde Et0/2 (puerto del atacante).

**Contra-medida:**
```
SW(config-if)# switchport port-security maximum 5
SW(config-if)# switchport port-security violation restrict
SW(config-if)# switchport port-security mac-address sticky
SW(config-if)# switchport port-security
```

---

### 6. 👑 STP Root Claim Attack

**Archivo:** `EnmanuelFelizSoto_20251402_STP_Root_P1.py`

Envía BPDUs con prioridad 0 para reclamar el rol de Root Bridge en la topología STP, alterando el flujo de tráfico y causando reconvergencia.

**Uso:**
```bash
sudo python3 EnmanuelFelizSoto_20251402_STP_Root_P1.py -i eth0 -p 0 -t 120
```

**Parámetros:**

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `-i / --interface` | Interfaz de red | requerido |
| `-p / --priority` | Bridge Priority (0=máxima) | `0` |
| `-t / --time` | Duración en segundos | `60` |

**Captura del ataque:**

![STP Root Claim](screenshots/stp_root.png)

> SW1 muestra Root ID Priority **0**, Address `0900.0000.0001` — el atacante fue aceptado como Root Bridge en VLAN 20.

**Contra-medida:**
```
SW(config-if)# spanning-tree bpduguard enable
SW(config-if)# spanning-tree guard root
SW(config)#    spanning-tree portfast bpduguard default
```

---

## 📹 Videos Demostración

Lista de reproducción completa en YouTube:  
🔗 [https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj)

Cada video incluye:
- ✅ Topología visible con nombre y matrícula
- ✅ Hora y fecha en pantalla
- ✅ Cara y voz del estudiante
- ✅ Demostración del ataque
- ✅ Aplicación de contra-medida

---

## 📁 Estructura del Repositorio

```
NetSec/
├── EnmanuelFelizSoto_20251402_CDP_DoS_P1.py
├── EnmanuelFelizSoto_20251402_ARP_MitM_P1.py
├── EnmanuelFelizSoto_20251402_DHCP_Spoofing_P1.py
├── EnmanuelFelizSoto_20251402_DHCP_Starvation_P1.py
├── EnmanuelFelizSoto_20251402_MAC_Flooding_P1.py
├── EnmanuelFelizSoto_20251402_STP_Root_P1.py
├── EnmanuelFelizSoto_20251402_Informe_P1.docx
├── topology.png
├── screenshots/
│   ├── dhcp_starvation.png
│   ├── mac_flooding.png
│   └── stp_root.png
└── README.md
```

---

> ⚠️ **Aviso Legal:** Todos los scripts fueron desarrollados exclusivamente con fines educativos en un entorno de laboratorio controlado (PNetLab). El uso de estas herramientas fuera de un entorno autorizado es ilegal.
