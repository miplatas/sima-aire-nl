"""Sensores SIMA Aire NL."""
import logging
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, STATIONS, PARAMETERS, PARAMETERS_IAS_ATTRS, get_ias_level
from .coordinator import SimaCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: SimaCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for station_key, (station_name, municipality, lat, lon) in STATIONS.items():
        # Índice IAS (contaminante dominante)
        entities.append(SimaIASSensor(coordinator, station_key, station_name, municipality))
        # Calidad del Aire (semáforo de alerta)
        entities.append(SimaQualitySensor(coordinator, station_key, station_name, municipality))
        # Concentraciones: PM10 y PM2.5
        for param_key, param_info in PARAMETERS.items():
            entities.append(
                SimaParameterSensor(coordinator, station_key, station_name, municipality, param_key, param_info)
            )
    async_add_entities(entities)


class SimaBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, station_key, station_name, municipality):
        super().__init__(coordinator)
        self._station_key = station_key
        self._station_name = station_name
        self._municipality = municipality

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._station_key)},
            "name": f"SIMA {self._station_name}",
            "model": "Estación de Monitoreo Ambiental",
            "configuration_url": "https://aire.nl.gob.mx",
        }

    def _station_data(self):
        if not self.coordinator.data:
            return {}
        return self.coordinator.data.get("stations", {}).get(self._station_key, {})

    def _timestamp(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("timestamp")


class SimaIASSensor(SimaBaseSensor):
    """Índice IAS del contaminante dominante con IAS de otros parámetros."""

    def __init__(self, coordinator, station_key, station_name, municipality):
        super().__init__(coordinator, station_key, station_name, municipality)
        self._attr_unique_id = f"sima_{station_key}_ias"
        self._attr_name = f"SIMA {station_name} Índice IAS"
        self._attr_icon = "mdi:traffic-light"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "IAS"

    @property
    def native_value(self):
        dom = self._station_data().get("dominant", {})
        return dom.get("ias")

    @property
    def extra_state_attributes(self):
        dom = self._station_data().get("dominant", {})
        ias = dom.get("ias")
        calidad, riesgo, color = get_ias_level(ias)
        attrs = {
            "estacion": self._station_name,
            "municipio": self._municipality,
            "contaminante_dominante": dom.get("contaminante"),
            "concentracion": dom.get("concentracion"),
            "calidad": calidad,
            "riesgo": riesgo,
            "semaforo": color,
            "timestamp": self._timestamp(),
        }
        
        # Agregar IAS de cada parámetro como atributo
        station_data = self._station_data()
        for param_key, param_info in PARAMETERS_IAS_ATTRS.items():
            param_data = station_data.get(param_key, {})
            param_ias = param_data.get("ias")
            if param_ias is not None:
                attrs[f"ias_{param_info['name'].lower()}"] = param_ias
        
        return attrs


class SimaQualitySensor(SimaBaseSensor):
    """Calidad del Aire: estado humanizado basado en IAS (Buena, Aceptable, Mala, etc)."""

    def __init__(self, coordinator, station_key, station_name, municipality):
        super().__init__(coordinator, station_key, station_name, municipality)
        self._attr_unique_id = f"sima_{station_key}_calidad"
        self._attr_name = f"SIMA {station_name} Calidad del Aire"
        self._attr_icon = "mdi:traffic-light"

    @property
    def native_value(self):
        dom = self._station_data().get("dominant", {})
        ias = dom.get("ias")
        calidad, _, _ = get_ias_level(ias)
        return calidad

    @property
    def extra_state_attributes(self):
        dom = self._station_data().get("dominant", {})
        ias = dom.get("ias")
        calidad, riesgo, color = get_ias_level(ias)
        return {
            "estacion": self._station_name,
            "municipio": self._municipality,
            "ias": ias,
            "contaminante_dominante": dom.get("contaminante"),
            "riesgo": riesgo,
            "semaforo": color,
            "timestamp": self._timestamp(),
        }


class SimaParameterSensor(SimaBaseSensor):
    """Sensor de un parámetro específico."""

    def __init__(self, coordinator, station_key, station_name, municipality, param_key, param_info):
        super().__init__(coordinator, station_key, station_name, municipality)
        self._param_key = param_key
        self._param_info = param_info
        self._attr_unique_id = f"sima_{station_key}_{param_key.lower()}"
        self._attr_name = f"SIMA {station_name} {param_info['name']}"
        self._attr_icon = param_info["icon"]
        self._attr_native_unit_of_measurement = param_info["unit"]
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        return self._station_data().get(self._param_key, {}).get("concentration")

    @property
    def extra_state_attributes(self):
        ias = self._station_data().get(self._param_key, {}).get("ias")
        concentration = self._station_data().get(self._param_key, {}).get("concentration")
        calidad, riesgo, color = get_ias_level(ias)
        return {
            "estacion": self._station_name,
            "municipio": self._municipality,
            "parametro": self._param_info["name"],
            "unidad_real": self._param_info["unit"],
            "ias": ias,
            "concentracion": concentration,
            "calidad": calidad,
            "riesgo": riesgo,
            "semaforo": color,
            "timestamp": self._timestamp(),
        }
