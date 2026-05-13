# -*- coding: utf-8 -*-
"""Benutzerdefinierter Delegate für die hervorgehobene Darstellung von Suchergebnissen.

Dieses Modul stellt einen Qt-Delegate bereit, der Einträge im
Autovervollständigungs-Popup als HTML rendert und Suchbegriffe
durch Fettschrift hervorhebt.
"""

import re

from qgis.PyQt.QtWidgets import QStyledItemDelegate, QStyle, QMessageBox
from qgis.PyQt.QtGui import QTextDocument, QFontMetrics
from qgis.PyQt.QtCore import Qt, QEvent, QRect, QSize

from qgis.core import QgsMessageLog, Qgis


class HighlightDelegate(QStyledItemDelegate):
    """Delegate zur farblichen Hervorhebung von Suchbegriffen in der Ergebnisliste.

    Rendert die Einträge des Autovervollständigungs-Popups als HTML und hebt
    die eingegebenen Suchbegriffe durch Fettschrift hervor.
    """

    def __init__(self, plugin, parent=None):
        """Konstruktor.

        Args:
            plugin (bielefeldGeosuche): Referenz auf die Plugin-Instanz.
            parent (QObject): Optionales Elternobjekt.
        """
        super().__init__(parent)
        self.plugin = plugin


    def paint(self, painter, option, index):
        """Zeichnet einen einzelnen Listeneintrag mit HTML-Formatierung.

        Hebt Suchbegriffe im Anzeigetext fett hervor. Selektierte Einträge
        werden mit der Systemhervorhebungsfarbe hinterlegt und vertikal
        zentriert dargestellt.

        Args:
            painter (QPainter): Der QPainter zum Zeichnen des Eintrags.
            option (QStyleOptionViewItem): Stiloptionen für das Element (Position, Zustand, Palette).
            index (QModelIndex): Modellindex des darzustellenden Eintrags.
        """
        text = index.data(Qt.DisplayRole)

        search = self.plugin.current_search_term

        if self.plugin.debug_log:
            QgsMessageLog.logMessage(
                "paint() search? " + search,
                "bielefeldGeosuche",
                Qgis.Info
            )

        if self.plugin.current_search_mode == "search" and not search:
            super().paint(painter, option, index)
            return

        # Unterscheidung ob das Suchergebnis selektiert ist oder nicht
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            text_color = option.palette.highlightedText().color().name()
        else:
            text_color = option.palette.text().color().name()

        formatted = self.formatText(text, search, text_color)
        
        doc = self.buildDocument(formatted)
        doc.setTextWidth(option.rect.width())

        painter.save()
        
        # Dokumentgröße berechnen
        doc_height = doc.size().height()

        # Vertikal zentrieren
        y = option.rect.top() + (option.rect.height() - doc_height) / 2

        painter.translate(option.rect.left(), y)

        popup = self.plugin.completer.popup()

        viewport_width = popup.viewport().width()

        scrollbar_width = popup.style().pixelMetric(
            popup.style().PM_ScrollBarExtent
        )

        if self.plugin.debug_log:
            QgsMessageLog.logMessage(
                "formatted: " + formatted + ", viewport_width: " + str(viewport_width) + ", option.rect.width(): " + str(option.rect.width()) + ", doc.size().width(): " + str(doc.size().width()) + ", doc.pageSize(): " + str(doc.pageSize()) + ", scrollbar_width: " + str(scrollbar_width),
                "bielefeldGeosuche",
                Qgis.Info
            )
        

        doc.drawContents(painter)
        painter.restore()


    def sizeHint(self, option, index):
        """Berechnet die Größe einer Suchergebnis-Zeile.

        Args:
            option (QStyleOptionViewItem): Stiloptionen für das Element (Position, Zustand, Palette).
            index (QModelIndex): Modellindex des darzustellenden Eintrags.
        """
        text = index.data(Qt.DisplayRole) 

        search = self.plugin.current_search_term
        formatted = self.formatText(text, search, option.palette.text().color().name())
        
        doc = self.buildDocument(formatted)

        exact_width = doc.idealWidth()

        fm = QFontMetrics(option.font)
        line_height = fm.height()

        if  option.rect.width() < exact_width:
            line_height = line_height * 2
        else:
            line_height = line_height * 1.1

        return QSize(
            int(option.rect.width()),
            int(line_height)
        )


    def formatText(self, text, search, text_color):
        """Hilfsmethode um den Suchtext in den Suchergebnissen hervorzuheben.

        Args:
            text (str): Text eines Suchergebnisses
            search (str): Suchstring
            text_color (str): Hex-Farbe

        Returns:
            Str: HTML-formatierten Text.
        """
        formatted = text
        # Teile fett markieren (case insensitive)
        if self.plugin.current_search_mode == "search" and search:
            tokens = [re.escape(t) for t in search.split() if len(t) > 1]

            if tokens:
                pattern = "(" + "|".join(tokens) + ")"

                formatted = re.sub(
                    pattern,
                    r"<b>\1</b>",
                    text,
                    flags=re.IGNORECASE
                )

        if len(self.plugin.search_metadata) > 0:
            formatted = f'<span style="font-weight:bold;color:#000;">&nbsp;&nbsp;i&nbsp;&nbsp;</span> <span style="color:{text_color};">{formatted}</span>'
        else:
            formatted = f'<span style="color:{text_color};">{formatted}</span>'

        return formatted


    def buildDocument(self, formatted):
        """Hilfsmethode um das QTextDocument Objekt zu erstellen.

        Args:
            formatted (str): HTML-formatierter Text

        Returns:
            QTextDocument: HTML-Textdokument eines Suchergebnisses.
        """
        doc = QTextDocument()
        doc.setHtml(formatted)
        return doc


    def editorEvent(self, event, model, option, index):
        """Hier wird geprüft ob ein Metadaten-Link angeklickt wurde.

        Wenn ein Info-i in der geoKATALOG-Suche angeklickt wurde, kann hier optional der dazugehörige
        Metadaten-Link zu diesem Thema in einem externen Webbrowser aufgerufen werden.

        Args:
            event (QEvent): Das QEvent enthält Informationen zum Klick-Event.
            model (QStringListModel): Das QStringListModel welches die Suchergebnisse enthält.
            option (QStyleOptionViewItem): Stiloptionen für das Element (Position, Zustand, Palette).
            index (QModelIndex): Modellindex des darzustellenden Eintrags.
        """

        if self.plugin.debug_log:
            QgsMessageLog.logMessage(
                "editorEvent() event.type():" + str(event.type()),
                "bielefeldGeosuche",
                Qgis.Info
            )

        
        if len(self.plugin.search_metadata) > 0 and event.type() == QEvent.MouseButtonPress:

            fm = QFontMetrics(option.font)
            line_height = fm.height()

            icon_rect = QRect(
                option.rect.left(),
                option.rect.top(),
                20,
                line_height
            )

            text = index.data(Qt.DisplayRole)

            if self.plugin.debug_log:
                QgsMessageLog.logMessage(
                    "editorEvent() icon_rect:" + str(icon_rect) + ", event.pos() " + str(event.pos()) + " , text: " + text,
                    "bielefeldGeosuche",
                    Qgis.Info
                )

            # Wenn grob der Bereich des Info-i angeklickt wurde, dann soll der Benutzer entscheiden können, ob er den Link öffnen will.
            if icon_rect.contains(event.pos()):
                link = self.plugin.search_metadata[text]

                parent = self.plugin.iface.mainWindow()

                reply = QMessageBox.question(
                    parent,
                    "Link öffnen",
                    f"Soll der folgende Link geöffnet werden?\n\n{link}",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    import webbrowser
                    webbrowser.open(link)
                

                return True  # Event verbraucht

        return super().editorEvent(event, model, option, index)
