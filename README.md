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

## Sensores por estación (4 entidades por dispositivo)

| Entidad | Descripción | Tipo |
|---|---|---|
| `sensor.sima_<est>_indice_ias` | Índice IAS del contaminante dominante | Numérico (IAS) |
| `sensor.sima_<est>_calidad_del_aire` | Calidad del aire: Buena, Aceptable, Mala, Muy Mala, Extremadamente Mala | Texto (semáforo) |
| `sensor.sima_<est>_pm10nc` | Concentración de PM10 | Numérico (µg/m³) |
| `sensor.sima_<est>_pm25nc` | Concentración de PM2.5 | Numérico (µg/m³) |

## Atributos del sensor Índice IAS

```yaml
contaminante_dominante: "PM25"      # Contaminante que genera el IAS más alto
concentracion: "9"                  # Concentración del contaminante dominante
calidad: "Buena"                    # Calidad del aire
riesgo: "Bajo"                      # Nivel de riesgo
semaforo: "green"                   # Color del semáforo (green | yellow | orange | red | purple | gray)
municipio: "Monterrey"
timestamp: "2026-06-24 08:00"
ias_pm10: 18                        # IAS específico de PM10
ias_pm25: 30                        # IAS específico de PM2.5
ias_o3: 10                          # IAS específico de O3
ias_no2: 5                          # IAS específico de NO2
ias_so2: 5                          # IAS específico de SO2
ias_co: 4                           # IAS específico de CO
```

## Atributos del sensor Calidad del Aire

```yaml
ias: 30                             # Valor numérico del índice
contaminante_dominante: "PM25"
riesgo: "Bajo"
semaforo: "green"
municipio: "Monterrey"
timestamp: "2026-06-24 08:00"
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
