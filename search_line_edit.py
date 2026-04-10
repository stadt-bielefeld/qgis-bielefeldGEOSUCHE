# -*- coding: utf-8 -*-
"""Benutzerdefiniertes Sucheingabefeld für das bielefeldGEOSUCHE-Plugin.

Dieses Modul erweitert QLineEdit um plugin-spezifisches Verhalten:
Das Autovervollständigungs-Popup wird beim Klick auf das Feld erneut geöffnet,
sofern bereits Suchergebnisse vorliegen.
"""

from qgis.PyQt.QtWidgets import QLineEdit
from qgis.PyQt.QtCore import Qt, QTimer

from qgis.core import (
    QgsMessageLog,
    Qgis
)


class SearchLineEdit(QLineEdit):
    """Erweitertes Eingabefeld mit automatischer Popup-Wiederöffnung.

    Öffnet das Autovervollständigungs-Popup erneut, wenn der Benutzer in das
    Feld klickt und bereits Suchergebnisse vorhanden sind.
    """

    def __init__(self, plugin, *args, **kwargs):
        """Konstruktor.

        Args:
            plugin (bielefeldGeosuche): Referenz auf die Plugin-Instanz.
        """
        super().__init__(*args, **kwargs)
        self.plugin = plugin

    def mouseReleaseEvent(self, event):
        """Öffnet das Autovervollständigungs-Popup bei Mausklick erneut.

        Wird ausgelöst, wenn der Benutzer das Eingabefeld anklickt. Falls
        bereits Suchergebnisse vorliegen und das Popup geschlossen ist,
        wird es wieder geöffnet.

        Args:
            event (QMouseEvent): Das Mausereignis.
        """
        super().mouseReleaseEvent(event)
        #QgsMessageLog.logMessage(
        #    "mouseReleaseEvent() self.hasSelectedText(): " + self.selectedText(),
        #    "bielefeldGeosuche",
        #    Qgis.Info
        #)

        # Wenn bereits Ergebnisse existieren → Popup wieder öffnen
        if (
            self.plugin.last_result_count > 0
            and not self.plugin.completer.popup().isVisible()
        ):
            QTimer.singleShot(0, lambda: self.plugin.completer.complete())


    def focusInEvent(self, event):
        """Behandelt das Eintreten des Tastaturfokus in das Eingabefeld.

        Args:
            event (QFocusEvent): Das Fokusereignis.
        """
        super().focusInEvent(event)
        #QgsMessageLog.logMessage(
        #    "focusInEvent()",
        #    "bielefeldGeosuche",
        #    Qgis.Info
        #)


    def focusOutEvent(self, event):
        """Behandelt den Verlust des Tastaturfokus aus dem Eingabefeld.

        Das Autovervollständigungs-Popup darf sich normal schließen.

        Args:
            event (QFocusEvent): Das Fokusereignis.
        """
        super().focusOutEvent(event)
        #QgsMessageLog.logMessage(
        #    "focusOutEvent()",
        #    "bielefeldGeosuche",
        #    Qgis.Info
        #)
        # Popup darf sich normal schließen
