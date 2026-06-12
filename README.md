# 🔐 NetSec — Network Security Attacks Lab
**Estudiante:** Enmanuel Feliz Soto | **Matrícula:** 20251402
**Institución:** Instituto Tecnológico de Las Américas (ITLA)
**Curso:** Seguridad en Redes

> Este repositorio es el índice general. Cada ataque tiene su propio repositorio independiente con script, documentación y video.

## 📹 Playlist YouTube
🔗 [Ver todos los videos](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj)

---

## 📦 Práctica 1 — Ataques Capa 2/3

| # | Ataque | Repositorio | Video |
|---|--------|-------------|-------|
| 1 | CDP DoS Flooding | [EnmanuelFelizSoto_20251402_CDP_DoS_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_CDP_DoS_P1) | [▶ YouTube](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj) |
| 2 | ARP MitM Poisoning | [EnmanuelFelizSoto_20251402_ARP_MitM_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_ARP_MitM_P1) | [▶ YouTube](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj) |
| 3 | DHCP Spoofing | [EnmanuelFelizSoto_20251402_DHCP_Spoofing_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_DHCP_Spoofing_P1) | [▶ YouTube](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj) |
| 4 | DHCP Starvation | [EnmanuelFelizSoto_20251402_DHCP_Starvation_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_DHCP_Starvation_P1) | [▶ YouTube](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj) |
| 5 | MAC Flooding | [EnmanuelFelizSoto_20251402_MAC_Flooding_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_MAC_Flooding_P1) | [▶ YouTube](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj) |
| 6 | STP Root Claim | [EnmanuelFelizSoto_20251402_STP_Root_P1](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_STP_Root_P1) | [▶ YouTube](https://www.youtube.com/playlist?list=PLn9wGcsdOtleB6unDjCUvq4LdJYgd4TTj) |

## 📦 Práctica 2 — VTP / DTP / DNS

| # | Ataque | Repositorio | Video |
|---|--------|-------------|-------|
| 7 | VTP VLAN Attack | [EnmanuelFelizSoto_20251402_VTP_Attack_P2](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_VTP_Attack_P2) | [▶ YouTube](https://youtu.be/3wIp_Bs5HmA) |
| 8 | DTP VLAN Hopping | [EnmanuelFelizSoto_20251402_DTP_VLANHopping_P2](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_DTP_VLANHopping_P2) | [▶ YouTube](https://youtu.be/4JSALP-O0Sg) |
| 9 | DNS Spoofing + ARP | [EnmanuelFelizSoto_20251402_DNS_Spoofing_P2](https://github.com/Enmafs/EnmanuelFelizSoto_20251402_DNS_Spoofing_P2) | [▶ YouTube](https://youtu.be/NbU1oIHrnOo) |

---

## 🗺️ Topología
**Entorno:** PNetLab — Cisco IOL + Docker containers
**Direccionamiento:** Basado en matrícula 20251402 → Red base 14.2.0.0/16

| VLAN | Uso | Red | CIDR |
|------|-----|-----|------|
| 10 | Usuarios | 14.2.0.0 | /25 |
| 20 | Gestión | 14.2.0.128 | /27 |
| 30 | Servidores | 14.2.0.160 | /28 |

> ⚠️ Todos los ataques fueron realizados en entorno controlado con contrato de ética firmado.
