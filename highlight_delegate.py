import re

from qgis.PyQt.QtWidgets import QStyledItemDelegate, QStyle
from qgis.PyQt.QtGui import QTextDocument
from qgis.PyQt.QtCore import Qt, QRectF

from qgis.core import QgsMessageLog, Qgis

class HighlightDelegate(QStyledItemDelegate):

    def __init__(self, plugin, parent=None):
        super().__init__(parent)
        self.plugin = plugin

    def paint(self, painter, option, index):
        text = index.data(Qt.DisplayRole)
        
        if len(text) > 50:
            text = text[:47] + "..."

        search = self.plugin.current_search_term

        #QgsMessageLog.logMessage(
        #    "paint() search? " + search,
        #    "bielefeldGeosuche",
        #    Qgis.Info
        #)

        if self.plugin.current_search_mode == "search" and not search:
            super().paint(painter, option, index)
            return

        formatted = text
        # Teile fett markieren (case insensitive)
        if self.plugin.current_search_mode == "search" and search:
            tokens = [t for t in search.split() if len(t) > 1]
            pattern = "(" + "|".join(tokens) + ")"

            formatted = re.sub(
                pattern,
                r"<b>\1</b>",
                text,
                flags=re.IGNORECASE
            )

        #QgsMessageLog.logMessage(
        #    "formatted: " + formatted,
        #    "bielefeldGeosuche",
        #    Qgis.Info
        #)


        # Unterscheidung ob das Suchergebnis selektiert ist oder nicht
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            text_color = option.palette.highlightedText().color().name()
        else:
            text_color = option.palette.text().color().name()

        formatted = f'<span style="color:{text_color};">{formatted}</span>'

        doc = QTextDocument()
        doc.setHtml(formatted)
        doc.setTextWidth(option.rect.width())

        painter.save()
        
        # Dokumentgröße berechnen
        doc_height = doc.size().height()

        # Vertikal zentrieren
        y = option.rect.top() + (option.rect.height() - doc_height) / 2

        painter.translate(option.rect.left(), y)
        doc.drawContents(painter)
        painter.restore()
