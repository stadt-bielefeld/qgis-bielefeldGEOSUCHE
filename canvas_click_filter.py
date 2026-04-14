# -*- coding: utf-8 -*-
"""Ereignisfilter für Klicks auf den QGIS-Kartenausschnitt.

Dieses Modul stellt einen Qt-Ereignisfilter bereit, der Mausklicks auf den
Kartenausschnitt abfängt und eine vorhandene RubberBand-Markierung entfernt.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bielefeld_geosuche import bielefeldGeosuche

from qgis.PyQt.QtCore import QObject, QEvent, Qt


class CanvasClickFilter(QObject):
    """Ereignisfilter, der Linksklicks auf den QGIS-Kartenausschnitt überwacht.

    Bei einem Linksklick auf den Kartenausschnitt wird eine vorhandene
    RubberBand-Markierung automatisch entfernt.
    """

    def __init__(self, plugin: bielefeldGeosuche) -> None:
        """Konstruktor.

        Args:
            plugin (bielefeldGeosuche): Referenz auf die Plugin-Instanz.
        """
        super().__init__()
        self.plugin = plugin

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Filtert Qt-Ereignisse und reagiert auf Mausklicks.

        Entfernt die RubberBand-Markierung, wenn der Benutzer mit der linken
        Maustaste in den Kartenausschnitt klickt.

        Args:
            obj (QObject): Das überwachte Qt-Objekt.
            event (QEvent): Das eingehende Qt-Ereignis.

        Returns:
            bool: False, damit das Ereignis nicht blockiert wird.
        """
        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                if self.plugin.rubber_band:
                    self.plugin.clear_rubber_band()

        return False  # Event NICHT blockieren!