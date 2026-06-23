# SIMA Aire Nuevo León

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Integración para Home Assistant que expone los datos de calidad del aire del **Sistema Integral de Monitoreo Ambiental (SIMA)** del Gobierno del Estado de Nuevo León — [aire.nl.gob.mx](https://aire.nl.gob.mx).

Los datos se actualizan cada hora, igual que el sitio oficial.

## Estaciones (15 en total)

| Clave | Nombre | Municipio |
|---|---|---|
| centro | CENTRO | Monterrey |
| noreste | NORESTE | San Nicolás |
| noreste2 | NORESTE 2 | Apodaca |
| noroeste | NOROESTE | Monterrey |
| noroeste2 | NOROESTE 2 | García |
| noroeste3 | NOROESTE 3 | García |
| norte | NORTE | Escobedo |
| norte2 | NORTE 2 | San Nicolás |
| sur | SUR | Monterrey |
| sureste | SURESTE | Guadalupe |
| sureste2 | SURESTE 2 | Juárez |
| sureste3 | SURESTE 3 | Cadereyta |
| suroeste | SUROESTE | Santa Catarina |
| suroeste2 | SUROESTE 2 | San Pedro |
| este | ESTE | Pesquería |

## Sensores por estación

| Sensor | Descripción |
|---|---|
| `sensor.sima_<est>_indice_ias` | Índice IAS contaminante dominante |
| `sensor.sima_<est>_pm10nc` | PM10 (IAS) |
| `sensor.sima_<est>_pm25nc` | PM2.5 (IAS) |
| `sensor.sima_<est>_o3nc` | Ozono (IAS) |
| `sensor.sima_<est>_no2nc` | NO2 (IAS) |
| `sensor.sima_<est>_so21nc` | SO2 (IAS) |
| `sensor.sima_<est>_conc` | CO (IAS) |

## Atributos del sensor IAS

```yaml
contaminante_dominante: "O3"
concentracion: "32"
calidad: "Buena"
riesgo: "Bajo"
semaforo: "green"   # green | yellow | orange | red | purple | gray
municipio: "Monterrey"
timestamp: "2026-06-23 17:00"
```

## Semáforo

| Color | Calidad | Riesgo | IAS |
|---|---|---|---|
| 🟢 green | Buena | Bajo | 0–50 |
| 🟡 yellow | Aceptable | Moderado | 51–100 |
| 🟠 orange | Mala | Alto | 101–150 |
| 🔴 red | Muy mala | Muy alto | 151–200 |
| 🟣 purple | Extremadamente mala | Extremadamente alto | >200 |
| ⬜ gray | Sin datos / Mantenimiento | — | — |

## Instalación vía HACS

1. HACS → ⋮ → Repositorios personalizados
2. URL: `https://github.com/miplatas/sima_aire_nl` — Categoría: **Integración**
3. Instalar → Reiniciar HA
4. Ajustes → Dispositivos y servicios → Agregar → **SIMA Aire Nuevo León**
