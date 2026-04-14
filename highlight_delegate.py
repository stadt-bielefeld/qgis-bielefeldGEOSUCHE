# -*- coding: utf-8 -*-
"""Benutzerdefinierter Delegate für die hervorgehobene Darstellung von Suchergebnissen.

Dieses Modul stellt einen Qt-Delegate bereit, der Einträge im
Autovervollständigungs-Popup als HTML rendert und Suchbegriffe
durch Fettschrift hervorhebt.
"""

from __future__ import annotations

import re
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .bielefeld_geosuche import bielefeldGeosuche

from qgis.PyQt.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionViewItem
from qgis.PyQt.QtGui import QTextDocument, QPainter
from qgis.PyQt.QtCore import Qt, QObject, QRectF, QModelIndex

from qgis.core import QgsMessageLog, Qgis


class HighlightDelegate(QStyledItemDelegate):
    """Delegate zur farblichen Hervorhebung von Suchbegriffen in der Ergebnisliste.

    Rendert die Einträge des Autovervollständigungs-Popups als HTML und hebt
    die eingegebenen Suchbegriffe durch Fettschrift hervor.
    """

    def __init__(self, plugin: bielefeldGeosuche, parent: Optional[QObject] = None) -> None:
        """Konstruktor.

        Args:
            plugin (bielefeldGeosuche): Referenz auf die Plugin-Instanz.
            parent (QObject): Optionales Elternobjekt.
        """
        super().__init__(parent)
        self.plugin = plugin

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
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
        
        if len(text) > 50:
            text = text[:47] + "..."

        search = self.plugin.current_search_term

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
