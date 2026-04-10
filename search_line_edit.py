from qgis.PyQt.QtWidgets import QLineEdit
from qgis.PyQt.QtCore import Qt, QTimer

from qgis.core import (
    QgsMessageLog,
    Qgis
)

class SearchLineEdit(QLineEdit):

    def __init__(self, plugin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin = plugin

    def mouseReleaseEvent(self, event):
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
        super().focusInEvent(event)
        #QgsMessageLog.logMessage(
        #    "focusInEvent()",
        #    "bielefeldGeosuche",
        #    Qgis.Info
        #)


    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        #QgsMessageLog.logMessage(
        #    "focusOutEvent()",
        #    "bielefeldGeosuche",
        #    Qgis.Info
        #)
        # Popup darf sich normal schließen
