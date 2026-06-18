# 🔐 Lab 07 — DMVPN Fase 2 + IKEv1 + EIGRP

**Estudiante:** Enmanuel Feliz Soto | **Matrícula:** 2025-1402  
**Institución:** Instituto Tecnológico de Las Américas (ITLA)  
**Curso:** Seguridad en Redes | **Sección:** 2-1C  
**Docente:** Jonathan Esteban Rondón Corniel

---

## 📋 Descripción

DMVPN Fase 2 permite túneles Spoke-to-Spoke dinámicos sin pasar por el Hub. NHRP resuelve el mapping NBMA. EIGRP distribuye rutas.

| Campo | Valor |
|-------|-------|
| **Tipo de VPN** | DMVPN Hub-and-Spoke |
| **Protocolo** | IKEv1 + IPSec ESP-AES256-SHA256 (mode transport) + mGRE |
| **Mecanismo** | NHRP + mGRE + IPSec transport mode — Túneles Spoke-to-Spoke directos |
| **Routing** | EIGRP AS 1402 sobre Tunnel0 mGRE |
| **Pre-shared Key** | `Cisco2025-1402-DMVPN1!` |

---

## 🗺️ Topología

> 📸 **[INSERTAR CAPTURA DE TOPOLOGÍA AQUÍ]**

<!-- Coloca aquí el screenshot de PNetLab con la topología del Lab 07 -->

**Entorno:** PNetLab — Cisco IOL  
**Peers:** HUB R1-S1 (20.25.7.2) | SPOKE1 R4-S2 (20.25.7.6) | SPOKE2 R5 (20.25.7.10)

### Tabla de Direccionamiento

| Rol | Router | IP WAN | IP Tunnel | LAN |
|-----|--------|--------|-----------|-----|
| HUB | R1-S1 | 20.25.7.2/30 | 14.0.2.1/24/24 | 10.14.16.0/24 (HUB) |
| SPOKE1 | R4-S2 | 20.25.7.6/30 | 14.0.2.2/24 | 10.14.26.0/24 (SPOKE1) |
| SPOKE2 | R5 | 20.25.7.10/30 | 14.0.2.3/24 | 10.14.36.0/25 VLAN10 + 10.14.36.128/25 VLAN20 (SPOKE2) |

### ISP

| Interfaz ISP | IP | Descripción |
|-------------|-----|-------------|
| Ethernet0/0 | 20.25.7.1/30 | Link to R1-S1 HUB |
| Ethernet0/1 | 20.25.7.5/30 | Link to R4-S2 SPOKE1 |
| Ethernet0/2 | 20.25.7.9/30 | Link to R5 SPOKE2 |

### Dirección Túnel
| Endpoint | IP Tunnel |
|----------|-----------|



---

## ⚙️ Configuración

El script completo de configuración se encuentra en:  
📄 [`Lab07_DMVPN_Fase2_IKEv1_EIGRP.txt`](./Lab07_DMVPN_Fase2_IKEv1_EIGRP.txt)

### Parámetros IKE/IPSec

| Parámetro | Valor |
|-----------|-------|
| Encryption | AES-256 |
| Hash/Integrity | SHA-256 |
| DH Group | 14 (2048-bit) |
| SA Lifetime (IKE) | 86400 s (24h) |
| SA Lifetime (IPSec) | 3600 s (1h) |
| PFS | Group 14 |
| Auth Method | Pre-Shared Key |

---

## ▶️ Procedimiento de Ejecución

### 1. Cargar configuración en PNetLab
```
# Aplicar configuración en cada dispositivo en el orden:
# 1. ISP → 2. R1-S1 → 3. R4-S2 → 4. R5
```

### 2. Verificar la VPN

```
show dmvpn
```
```
show ip nhrp
```
```
show ip eigrp neighbors
```
```
show crypto isakmp sa
```

### 3. Prueba de conectividad
```
ping 10.14.36.1 source 10.14.26.1
```

---

## 📸 Capturas de Verificación

> 📸 **[INSERTAR CAPTURA: show crypto isakmp sa]**

<!-- Captura mostrando el estado QM_IDLE / ESTABLISHED -->

> 📸 **[INSERTAR CAPTURA: show crypto ipsec sa]**

<!-- Captura mostrando pkts encaps/decaps incrementando -->

> 📸 **[INSERTAR CAPTURA: ping exitoso]**

<!-- Captura del ping source 10.14.16.0/24 (HUB) -->

---

## 🔍 Análisis y Comparativa

### Ventajas de este tipo de VPN
- Ver documentación técnica en el informe PDF

### Diferencias con otros labs
- Ver tabla comparativa en el README principal

---

## 📎 Recursos

| Recurso | Enlace |
|---------|--------|
| Repositorio Principal | [Enmafs/NetSec](https://github.com/Enmafs/NetSec) |
| Script de configuración | [`Lab07_DMVPN_Fase2_IKEv1_EIGRP.txt`](./Lab07_DMVPN_Fase2_IKEv1_EIGRP.txt) |
| Video demostración | 🎬 **[PENDIENTE — agregar link de YouTube]** |

---

> ⚠️ *Laboratorio realizado en entorno controlado (PNetLab). Fines exclusivamente académicos.*
