from qgis.PyQt.QtCore import QObject, QEvent, Qt

class CanvasClickFilter(QObject):

    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin

    def eventFilter(self, obj, event):

        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                if self.plugin.rubber_band:
                    self.plugin.clear_rubber_band()

        return False  # Event NICHT blockieren!