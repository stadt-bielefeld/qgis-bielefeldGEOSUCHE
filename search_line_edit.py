# -*- coding: utf-8 -*-
"""Benutzerdefiniertes Sucheingabefeld für das bielefeldGEOSUCHE-Plugin.

Dieses Modul erweitert QLineEdit um plugin-spezifisches Verhalten:
Das Autovervollständigungs-Popup wird beim Klick auf das Feld erneut geöffnet,
sofern bereits Suchergebnisse vorliegen.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bielefeld_geosuche import bielefeldGeosuche

from qgis.PyQt.QtWidgets import QLineEdit
from qgis.PyQt.QtCore import Qt, QTimer
from qgis.PyQt.QtGui import QMouseEvent, QFocusEvent

from qgis.core import (
    QgsMessageLog,
    Qgis
)


class SearchLineEdit(QLineEdit):
    """Erweitertes Eingabefeld mit automatischer Popup-Wiederöffnung.

    Öffnet das Autovervollständigungs-Popup erneut, wenn der Benutzer in das
    Feld klickt und bereits Suchergebnisse vorhanden sind.
    """

    def __init__(self, plugin: bielefeldGeosuche, *args, **kwargs) -> None:
        """Konstruktor.

        Args:
            plugin (bielefeldGeosuche): Referenz auf die Plugin-Instanz.
        """
        super().__init__(*args, **kwargs)
        self.plugin = plugin

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Öffnet das Autovervollständigungs-Popup bei Mausklick erneut.

        Wird ausgelöst, wenn der Benutzer das Eingabefeld anklickt. Falls
        bereits Suchergebnisse vorliegen und das Popup geschlossen ist,
        wird es wieder geöffnet.

        Args:
            event (QMouseEvent): Das Mausereignis.
        """
        super().mouseReleaseEvent(event)

        # Wenn bereits Ergebnisse existieren → Popup wieder öffnen
        if (
            self.plugin.last_result_count > 0
            and not self.plugin.completer.popup().isVisible()
        ):
            QTimer.singleShot(0, lambda: self.plugin.completer.complete())


    def focusInEvent(self, event: QFocusEvent) -> None:
        """Behandelt das Eintreten des Tastaturfokus in das Eingabefeld.

        Args:
            event (QFocusEvent): Das Fokusereignis.
        """
        super().focusInEvent(event)


    def focusOutEvent(self, event: QFocusEvent) -> None:
        """Behandelt den Verlust des Tastaturfokus aus dem Eingabefeld.

        Das Autovervollständigungs-Popup darf sich normal schließen.

        Args:
            event (QFocusEvent): Das Fokusereignis.
        """
        super().focusOutEvent(event)
        # Popup darf sich normal schließen
