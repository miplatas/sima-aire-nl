DOMAIN = "sima_aire_nl"
DEFAULT_SCAN_INTERVAL = 3600  # 1 hora

URL_SIMA = "https://aire.nl.gob.mx/airemapbing/airebing_icars_alt_ns_newNL_4_L3.php"

# (nombre_display, municipio, lat, lon)
STATIONS = {
    "centro":    ("CENTRO",     "Monterrey",      25.6760139, -100.338553),
    "noreste":   ("NORESTE",    "San Nicolás",    25.74503,   -100.25317),
    "noreste2":  ("NORESTE 2",  "Apodaca",        25.777475,  -100.1882),
    "noroeste":  ("NOROESTE",   "Monterrey",      25.7629306, -100.369578),
    "noroeste2": ("NOROESTE 2", "García",         25.8004639, -100.585011),
    "noroeste3": ("NOROESTE 3", "García",         25.785,     -100.463611),
    "norte":     ("NORTE",      "Escobedo",       25.7988361, -100.327164),
    "norte2":    ("NORTE 2",    "San Nicolás",    25.7297587, -100.310019),
    "sur":       ("SUR",        "Monterrey",      25.6169806, -100.273936),
    "sureste":   ("SURESTE",    "Guadalupe",      25.6654972, -100.243653),
    "sureste2":  ("SURESTE 2",  "Juárez",         25.646126,  -100.095616),
    "sureste3":  ("SURESTE 3",  "Cadereyta",      25.6008639, -99.9953028),
    "suroeste":  ("SUROESTE",   "Santa Catarina", 25.6794444, -100.467831),
    "suroeste2": ("SUROESTE 2", "San Pedro",      25.665275,  -100.412853),
    "este":      ("ESTE",       "Pesquería",      25.7905833, -100.078411),
}

# Parámetros de concentración a exponer como sensores (PM10, PM2.5)
PARAMETERS = {
    "PM10Nc":  {"name": "PM10",  "unit": "µg/m³", "icon": "mdi:blur"},
    "PM25Nc":  {"name": "PM2.5", "unit": "µg/m³", "icon": "mdi:blur-radial"},
}

# Parámetros adicionales cuyo IAS se incluye como atributos del sensor Índice IAS
PARAMETERS_IAS_ATTRS = {
    "O3Nc":    {"name": "O3",    "unit": "ppb"},
    "NO2Nc":   {"name": "NO2",   "unit": "ppb"},
    "SO21Nc":  {"name": "SO2",   "unit": "ppb"},
    "CONc":    {"name": "CO",    "unit": "ppm"},
}

IAS_LEVELS = [
    (0,   50,  "Buena",               "Bajo",                "green"),
    (51,  100, "Aceptable",           "Moderado",            "yellow"),
    (101, 150, "Mala",                "Alto",                "orange"),
    (151, 200, "Muy mala",            "Muy alto",            "red"),
    (201, 999, "Extremadamente mala", "Extremadamente alto", "purple"),
]

def get_ias_level(value):
    if value is None:
        return ("Sin datos", "Sin datos", "gray")
    for low, high, calidad, riesgo, color in IAS_LEVELS:
        if low <= int(value) <= high:
            return (calidad, riesgo, color)
    return ("Sin datos", "Sin datos", "gray")
