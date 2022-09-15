from datetime import datetime
from sqlite3 import paramstyle
from typing import Union

import requests


class FotoparadiesStatus:
    """
    Klasse zum Abrufen und Verabeiten des akutellen Auftragstatus von Fotoarbeiten
    """

    def __init__(
        self, shop: int, order: int, name: str = None, fetch_data=True
    ) -> None:
        """Initialisiert einen Fotoparadies Status

        Args:
            shop (int): Filialnummer
            order (int): Auftragsnummer
        """

        self._order = order
        self._shop = shop
        self._name = name

        if fetch_data:
            self.refresh()

    def refresh(self):
        """Aktualisiert die Auftragsdaten mit der Fotoparadies API"""
        self._statusjson = self._get_json_status(shop=self._shop, order=self._order)

    @property
    def ordername(self) -> str:
        """Gibt den Auftragsnamen (entweder die Auftragsnummer oder benutzerdefiniert) zurück

        Returns:
            str: Auftragsnamen (entweder die Auftragsnummer oder benutzerdefiniert)
        """
        return self._name if self._name else str(self._order)

    @property
    def order(self) -> int:
        """Gibt die Auftragsnummerzurück

        Returns:
            int: Auftragsnummer
        """
        return self._statusjson["orderNo"]

    @property
    def currentstatus(self) -> str:
        """Aktueller Status als Kurztext

        Returns:
            str: Status (Kurz)
        """
        return self._statusjson["summaryStateCode"]

    @property
    def getlastupdate(self) -> datetime:
        """Zeitpunkt des letzten Updates

        Returns:
            datetime: Letztes Update
        """
        return self._statusjson["summaryDate"]

    @property
    def price(self) -> str:
        """Preis für den Auftrag

        Returns:
            float: Auftragspreis
        """
        return self._statusjson["summaryPriceText"]

    @staticmethod
    def _get_json_status(
        shop: int, order: int, config: int = 1320
    ) -> dict[str, Union[str, int, float, None]]:
        """Gibt den aktuellen Status des Auftragstatus zurück

        Args:
            shop (int): Filialnummer
            order (int): Auftragsnummer
            config (int, optional): Abfragekonfiguration. Standard ist 1320.

        Returns:
            dict[str, Union[str, int, float, None]]: Den Auftragszustand.
        """

        requesturl = f"https://spot.photoprintit.com/spotapi/orderInfo/forShop"
        parameters = {"config": config, "shop": shop, "order": order}
        request = requests.get(requesturl, params=parameters)

        return request.json()
