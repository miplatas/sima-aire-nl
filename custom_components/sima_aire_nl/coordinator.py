"""Coordinator SIMA Aire NL — scraping del PHP del mapa."""
import logging
import re
import json
from datetime import timedelta

import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, URL_SIMA, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class SimaCoordinator(DataUpdateCoordinator):

    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    URL_SIMA, timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"HTTP {resp.status} al consultar SIMA")
                    html = await resp.text(encoding="utf-8", errors="replace")
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error de conexión con SIMA: {err}") from err

        return self._parse(html)

    def _parse(self, html: str) -> dict:
        data1 = self._extract_array(html, "arrayIMKTodo1")
        data11 = self._extract_array(html, "arrayIMKTodo11")

        stations = {}
        timestamp = None

        for entry in data1:
            est = entry.get("Estacion", "").lower()
            param = entry.get("Parameter", "")
            ias = entry.get("HrAveData")
            date = entry.get("Date")
            if date and not timestamp:
                timestamp = date
            if est not in stations:
                stations[est] = {}
            stations[est][param] = {"ias": ias}

        for entry in data11:
            est = entry.get("Estacion", "").lower()
            if est in stations:
                stations[est]["dominant"] = {
                    "contaminante": entry.get("contaminante"),
                    "ias": entry.get("HrAveData"),
                    "concentracion": entry.get("concentracion"),
                }

        return {"timestamp": timestamp, "stations": stations}

    def _extract_array(self, html: str, var_name: str) -> list:
        pattern = rf"var\s+{re.escape(var_name)}\s*=\s*(\[.*?\])\s*(?://|;|var\s)"
        match = re.search(pattern, html, re.DOTALL)
        if not match:
            _LOGGER.warning("No se encontró %s en el HTML del SIMA", var_name)
            return []
        raw = match.group(1)
        raw = re.sub(r'//.*', '', raw)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as err:
            _LOGGER.error("Error parseando %s: %s", var_name, err)
            return []
