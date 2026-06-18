# 🔐 Lab 02 — IPSec IKEv1 — Route-Based (VTI)

**Estudiante:** Enmanuel Feliz Soto | **Matrícula:** 2025-1402  
**Institución:** Instituto Tecnológico de Las Américas (ITLA)  
**Curso:** Seguridad en Redes | **Sección:** 2-1C  
**Docente:** Jonathan Esteban Rondón Corniel

---

## 📋 Descripción

VPN basada en rutas usando VTI. Más flexible que Policy-Based, permite routing dinámico sobre el túnel.

| Campo | Valor |
|-------|-------|
| **Tipo de VPN** | Site-to-Site |
| **Protocolo** | IKEv1 + IPSec ESP-AES256-SHA256 |
| **Mecanismo** | Static VTI (Virtual Tunnel Interface) + Rutas Estáticas |
| **Routing** | Rutas estáticas apuntando a Tunnel0 |
| **Pre-shared Key** | `Cisco2025-1402-VTI!` |

---

## 🗺️ Topología

> 📸 **[INSERTAR CAPTURA DE TOPOLOGÍA AQUÍ]**

<!-- Coloca aquí el screenshot de PNetLab con la topología del Lab 02 -->

**Entorno:** PNetLab — Cisco IOL  
**Peers:** R1-S1 (20.25.2.2) ↔ R4-S2 (20.25.2.6)

### Tabla de Direccionamiento

| Router | Rol | IP WAN | Interfaz WAN | IP LAN | Interfaz LAN |
|--------|-----|--------|--------------|--------|--------------|
| R1-S1 | Peer 1 / Iniciador | 20.25.2.2 | Ethernet0/0 | 10.14.11.0.1/24 | **Ethernet0/3** |
| R4-S2 | Peer 2 / Respondedor | 20.25.2.6 | Ethernet0/1 | 10.14.21.0.1/24 | Ethernet0/0 |

### ISP

| Interfaz ISP | IP | Descripción |
|-------------|-----|-------------|
| Ethernet0/0 | 20.25.2.1/30 | Link to R1-S1 |
| Ethernet0/1 | 20.25.2.5/30 | Link to R4-S2 |

### Dirección Túnel
| Endpoint | IP Tunnel |
|----------|-----------|
| R1-S1 Tunnel0 | 14.0.2.1/30/30 |
| R4-S2 Tunnel0 | 14.0.2.2/30/30 |

---

## ⚙️ Configuración

El script completo de configuración se encuentra en:  
📄 [`Lab02_IPSec_IKEv1_RouteBased_VTI.txt`](./Lab02_IPSec_IKEv1_RouteBased_VTI.txt)

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
# 1. ISP → 2. R1-S1 → 3. R4-S2 → 4. R2/Server
```

### 2. Verificar la VPN

```
show crypto isakmp sa
```
```
show crypto ipsec sa
```
```
show interface Tunnel0
```

### 3. Prueba de conectividad
```
ping 10.14.21.10 source 10.14.11.2
```

---

## 📸 Capturas de Verificación

> 📸 **[INSERTAR CAPTURA: show crypto isakmp sa]**

<!-- Captura mostrando el estado QM_IDLE / ESTABLISHED -->

> 📸 **[INSERTAR CAPTURA: show crypto ipsec sa]**

<!-- Captura mostrando pkts encaps/decaps incrementando -->

> 📸 **[INSERTAR CAPTURA: ping exitoso]**

<!-- Captura del ping source 10.14.11.0/24 -->

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
| Script de configuración | [`Lab02_IPSec_IKEv1_RouteBased_VTI.txt`](./Lab02_IPSec_IKEv1_RouteBased_VTI.txt) |
| Video demostración | 🎬 **[PENDIENTE — agregar link de YouTube]** |

---

> ⚠️ *Laboratorio realizado en entorno controlado (PNetLab). Fines exclusivamente académicos.*
