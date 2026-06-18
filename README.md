# 🔐 NetSec — Network Security Attacks Lab
**Estudiante:** Enmanuel Feliz Soto | **Matrícula:** 20251402
**Institución:** Instituto Tecnológico de Las Américas (ITLA)
**Curso:** Seguridad en Redes

> Índice general. Cada ataque tiene su **repositorio independiente** con script, documentación técnica y video.

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

## 📦 Práctica 3 Semana 6 — VPNs (IPsec, GRE, DMVPN)

| # | Laboratorios | Repositorio / Carpeta |
|---|--------------|-------------|
| 10 | IPSec, GRE, DMVPN | [VPN_Labs](./VPN_Labs) |

---

## 🗺️ Topología
**Entorno:** PNetLab — Cisco IOL + Docker
**Direccionamiento:** Matrícula 20251402 → Red base 14.2.0.0

| VLAN | Uso | Red | CIDR |
|------|-----|-----|------|
| 10 | Usuarios | 14.2.0.0 | /25 |
| 20 | Gestión | 14.2.0.128 | /27 |
| 30 | Servidores | 14.2.0.160 | /28 |

> ⚠️ Todos los ataques realizados en entorno controlado.
