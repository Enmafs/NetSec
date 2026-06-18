# 🔐 NetSec — Network Security Attacks Lab
**Estudiante:** Enmanuel Feliz Soto | **Matrícula:** 20251402  
**Institución:** Instituto Tecnológico de Las Américas (ITLA)  
**Curso:** Seguridad en Redes  

> Índice general. Cada práctica tiene su **repositorio/carpeta independiente** con script, documentación técnica y video.

## 📹 Playlist YouTube — Todos los videos
🔗 [Ver playlist completa](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj)

---

## 📦 Práctica 1 Semana 1 & 2 — Ataques Capa 2/3

| # | Ataque | Repositorio | Video |
|---|--------|-------------|-------|
| 1 | CDP DoS Flooding | [EnmanuelFelizSoto_20251402_CDP_DoS_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_CDP_DoS_P1) | [▶ Ver](https://youtu.be/fgMcSZNa4t4) |
| 2 | ARP MitM Poisoning | [EnmanuelFelizSoto_20251402_ARP_MitM_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_ARP_MitM_P1) | [▶ Ver](https://youtu.be/q64Y0VaI00Y) |
| 3 | DHCP Spoofing | [EnmanuelFelizSoto_20251402_DHCP_Spoofing_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_DHCP_Spoofing_P1) | [▶ Ver](https://youtu.be/-5pqvlcbpdM) |
| 4 | DHCP Starvation | [EnmanuelFelizSoto_20251402_DHCP_Starvation_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_DHCP_Starvation_P1) | [▶ Ver](https://youtu.be/IQDzA9vkaCo) |
| 5 | MAC Flooding | [EnmanuelFelizSoto_20251402_MAC_Flooding_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_MAC_Flooding_P1) | [▶ Ver](https://youtu.be/hSJj7oudlSQ) |
| 6 | STP Root Claim | [EnmanuelFelizSoto_20251402_STP_Root_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_STP_Root_P1) | [▶ Ver](https://youtu.be/JIAN-dWS8p8) |

## 📦 Práctica 2 Semana 4 — VTP / DTP / DNS

| # | Ataque | Repositorio | Video |
|---|--------|-------------|-------|
| 7 | VTP VLAN Attack | [EnmanuelFelizSoto_20251402_VTP_Attack_P2](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_VTP_Attack_P2) | [▶ Ver](https://youtu.be/3wIp_Bs5HmA) |
| 8 | DTP VLAN Hopping | [EnmanuelFelizSoto_20251402_DTP_VLANHopping_P2](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_DTP_VLANHopping_P2) | [▶ Ver](https://youtu.be/4JSALP-O0Sg) |
| 9 | DNS Spoofing + ARP | [EnmanuelFelizSoto_20251402_DNS_Spoofing_P2](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_DNS_Spoofing_P2) | [▶ Ver](https://youtu.be/NbU1oIHrnOo) |

---

## 📦 Práctica 3 — VPNs (Cisco IOS + Fortigate)

> **Entorno:** PNetLab — Cisco IOL (Labs 01-08) | Fortigate VM (Labs 09-10)  
> **Topología Cisco:** R1-S1 ↔ ISP ↔ R4-S2 | R5 (DMVPN Spoke2)  
> **Topología Fortigate:** VPC ↔ Fortinet ↔ ISP-DHCP ↔ Fortinet ↔ VPC

### 🔧 Labs Cisco IOS

| # | Tipo VPN | Protocolo | Mecanismo | Carpeta | Video |
|---|----------|-----------|-----------|---------|-------|
| Lab 01 | IPSec Site-to-Site | IKEv1 | Policy-Based (Crypto Map) | [Lab01_IPSec_IKEv1_PolicyBased](./Lab01_IPSec_IKEv1_PolicyBased/) | 🎬 Pendiente |
| Lab 02 | IPSec Site-to-Site | IKEv1 | Route-Based (VTI) | [Lab02_IPSec_IKEv1_RouteBased_VTI](./Lab02_IPSec_IKEv1_RouteBased_VTI/) | 🎬 Pendiente |
| Lab 03 | GRE sobre IPSec | IKEv1 | GRE Tunnel + IPSec Profile | [Lab03_GRE_sobre_IPSec_IKEv1](./Lab03_GRE_sobre_IPSec_IKEv1/) | 🎬 Pendiente |
| Lab 04 | IPSec Site-to-Site | IKEv2 | Policy-Based (Crypto Map) | [Lab04_IPSec_IKEv2_PolicyBased](./Lab04_IPSec_IKEv2_PolicyBased/) | 🎬 Pendiente |
| Lab 05 | IPSec Site-to-Site | IKEv2 | Route-Based (VTI) | [Lab05_IPSec_IKEv2_RouteBased_VTI](./Lab05_IPSec_IKEv2_RouteBased_VTI/) | 🎬 Pendiente |
| Lab 06 | GRE sobre IPSec | IKEv2 | GRE Tunnel + IKEv2 Profile | [Lab06_GRE_sobre_IPSec_IKEv2](./Lab06_GRE_sobre_IPSec_IKEv2/) | 🎬 Pendiente |
| Lab 07 | DMVPN Fase 2 | IKEv1 + EIGRP | mGRE + NHRP + Spoke-to-Spoke | [Lab07_DMVPN_Fase2_IKEv1_EIGRP](./Lab07_DMVPN_Fase2_IKEv1_EIGRP/) | 🎬 Pendiente |
| Lab 08 | DMVPN Fase 3 | IKEv2 + EIGRP | mGRE + NHRP redirect/shortcut | [Lab08_DMVPN_Fase3_IKEv2_EIGRP](./Lab08_DMVPN_Fase3_IKEv2_EIGRP/) | 🎬 Pendiente |

### 🛡️ Labs Fortigate

| # | Tipo VPN | Plataforma | Carpeta | Video |
|---|----------|------------|---------|-------|
| Lab 09 | IPSec Site-to-Site | Fortigate VM | 🔄 Pendiente | 🎬 Pendiente |
| Lab 10 | SSL-VPN / IPSec | Fortigate VM | 🔄 Pendiente | 🎬 Pendiente |

### 📊 Tabla Comparativa — Todos los Labs Cisco

| Lab | IKE | Tipo | Tunnel IP | LAN-A | LAN-B | Routing |
|-----|-----|------|-----------|-------|-------|---------|
| 01 | v1 | Policy-Based | N/A | 10.14.10.0/24 | 10.14.20.0/24 | Estático + ACL |
| 02 | v1 | VTI | 14.0.2.1-2/30 | 10.14.11.0/24 | 10.14.21.0/24 | Estático → Tunnel0 |
| 03 | v1 | GRE/IPSec | 14.0.2.5-6/30 | 10.14.12.0/24 | 10.14.22.0/24 | Estático → Tunnel0 |
| 04 | v2 | Policy-Based | N/A | 10.14.13.0/24 | 10.14.23.0/24 | Estático + ACL |
| 05 | v2 | VTI | 14.0.2.9-10/30 | 10.14.14.0/24 | 10.14.24.0/24 | Estático → Tunnel0 |
| 06 | v2 | GRE/IPSec | 14.0.2.13-14/30 | 10.14.15.0/24 | 10.14.25.0/24 | Estático → Tunnel0 |
| 07 | v1 | DMVPN F2 | 14.0.2.0/24 | 10.14.16.0/24 | 10.14.26-36.0 | EIGRP 1402 |
| 08 | v2 | DMVPN F3 | 14.0.3.0/24 | 10.14.17.0/24 | 10.14.27-37.0 | EIGRP 1403 |

---

## 🗺️ Topología General

**Entorno:** PNetLab — Cisco IOL + Docker  
**Direccionamiento:** Matrícula 20251402 → Red base 14.x.x.x

| VLAN | Uso | Red | CIDR |
|------|-----|-----|------|
| 10 | Usuarios | 14.2.0.0 | /25 |
| 20 | Gestión | 14.2.0.128 | /27 |
| 30 | Servidores | 14.2.0.160 | /28 |

> ⚠️ Todos los laboratorios realizados en entorno controlado con fines exclusivamente académicos.
