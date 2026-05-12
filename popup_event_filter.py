# -*- coding: utf-8 -*-
"""Ereignisfilter für das Completer Popup.

Dieses Modul stellt einen Qt-Ereignisfilter bereit, der das Completer Popup überwacht,
um sich die Scroll-Position des Popups zu merken, wenn sich das Completer Popup schließt.
"""

from qgis.PyQt.QtCore import QObject, QEvent


class PopupEventFilter(QObject):
    """Ereignisfilter, der das Completer Popup überwacht.

    Wenn sich das Completer Popup schließt, wird dieser Filter verwendet, 
    um sich die Scroll-Position des Popups zu merken.
    """

    def __init__(self, plugin):
        """Konstruktor.

        Args:
            plugin (bielefeldGeosuche): Referenz auf die Plugin-Instanz.
        """
        super().__init__()
        self.plugin = plugin

    def eventFilter(self, obj, event):
        """Filtert Qt-Ereignisse und reagiert auf das Completer Popup.

        Wenn das Completer Popup sich schließt, wird dieser Filter verwendet, 
        um sich die Scroll-Position des Popups zu merken.

        Args:
            obj (QObject): Das überwachte Qt-Objekt.
            event (QEvent): Das eingehende Qt-Ereignis.

        Returns:
            bool: False, damit das Ereignis nicht blockiert wird.
        """
        if obj == self.plugin.completer.popup() and event.type() in (QEvent.Hide, QEvent.Close):
            # Speichert die Scroll-Position des Suchergebnis-Popups, wenn es ohne Auswahl geschlossen wird
            self.plugin.saved_scroll_pos = self.plugin.completer.popup().verticalScrollBar().value()

        return False  # Event NICHT blockieren!