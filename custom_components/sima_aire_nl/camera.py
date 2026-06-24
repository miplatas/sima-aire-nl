"""Cámara del mapa SIMA Aire NL."""
import logging
from urllib.parse import quote

import aiohttp
from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, URL_SIMA

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([SimaMapCamera(hass, entry.entry_id)], True)


class SimaMapCamera(Camera):
    """Cámara que muestra una vista del mapa web de SIMA."""

    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        super().__init__()
        self.hass = hass
        self._entry_id = entry_id
        self._attr_unique_id = f"sima_map_{entry_id}"
        self._attr_name = "SIMA Mapa Calidad del Aire"
        self._attr_content_type = "image/png"
        self._attr_icon = "mdi:map-search"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"map_{self._entry_id}")},
            "name": "SIMA Mapa Calidad del Aire",
            "manufacturer": "SIMA Aire NL",
            "model": "Mapa de Calidad del Aire",
            "configuration_url": URL_SIMA,
        }

    @property
    def extra_state_attributes(self):
        return {
            "source_url": URL_SIMA,
            "provider": "thum.io",
        }

    async def async_camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        size = width or 1280
        target_url = quote(URL_SIMA, safe="")
        snapshot_url = f"https://image.thum.io/get/png/noanimate/width/{size}/{target_url}"

        session = async_get_clientsession(self.hass)
        try:
            async with session.get(snapshot_url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status != 200:
                    _LOGGER.warning("Error obteniendo imagen del mapa SIMA: HTTP %s", resp.status)
                    return None
                return await resp.read()
        except aiohttp.ClientError as err:
            _LOGGER.warning("Error obteniendo imagen del mapa SIMA: %s", err)
            return None
