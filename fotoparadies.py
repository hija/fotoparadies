from datetime import datetime
from sqlite3 import paramstyle
from typing import Union

import requests


class FotoparadiesStatus:
    """
    Klasse zum Abrufen und Verabeiten des akutellen Auftragstatus von Fotoarbeiten
    """

    def __init__(self, shop: int, order: int, name: str = None) -> None:
        """Initialisiert einen Fotoparadies Status

        Args:
            shop (int): Filialnummer
            order (int): Auftragsnummer
        """
        self._statusjson = self._get_json_status(shop=shop, order=order)
        self._name = name

    @property
    def ordername(self) -> Union[str, None]:
        return self._name

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
    def price(self) -> float:
        """Preis für den Auftrag

        Returns:
            float: Auftragspreis
        """
        return self._statusjson["summaryPrice"]

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
