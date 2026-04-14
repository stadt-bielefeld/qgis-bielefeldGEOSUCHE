# coding=utf-8
"""QGIS plugin implementation.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

.. note:: This source code was copied from the 'postgis viewer' application
     with original authors:
     Copyright (c) 2010 by Ivan Mincik, ivan.mincik@gista.sk
     Copyright (c) 2011 German Carrillo, geotux_tuxman@linuxmail.org
     Copyright (c) 2014 Tim Sutton, tim@linfiniti.com

"""

__author__ = 'tim@linfiniti.com'
__revision__ = '$Format:%H$'
__date__ = '10/01/2011'
__copyright__ = (
    'Copyright (c) 2010 by Ivan Mincik, ivan.mincik@gista.sk and '
    'Copyright (c) 2011 German Carrillo, geotux_tuxman@linuxmail.org'
    'Copyright (c) 2014 Tim Sutton, tim@linfiniti.com'
)

from __future__ import annotations

import logging
from typing import Optional, List

from qgis.PyQt.QtCore import QObject, Qt, pyqtSlot, pyqtSignal
from qgis.PyQt.QtWidgets import QAction, QDockWidget
from qgis.core import QgsMapLayer, QgsMapLayerRegistry
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer
LOGGER = logging.getLogger('QGIS')


#noinspection PyMethodMayBeStatic,PyPep8Naming
class QgisInterface(QObject):
    """Class to expose QGIS objects and functions to plugins.

    This class is here for enabling us to run unit tests only,
    so most methods are simply stubs.
    """
    currentLayerChanged = pyqtSignal(QgsMapCanvasLayer)

    def __init__(self, canvas: QgsMapCanvas) -> None:
        """Constructor
        :param canvas:
        """
        QObject.__init__(self)
        self.canvas = canvas
        # Set up slots so we can mimic the behaviour of QGIS when layers
        # are added.
        LOGGER.debug('Initialising canvas...')
        # noinspection PyArgumentList
        QgsMapLayerRegistry.instance().layersAdded.connect(self.addLayers)
        # noinspection PyArgumentList
        QgsMapLayerRegistry.instance().layerWasAdded.connect(self.addLayer)
        # noinspection PyArgumentList
        QgsMapLayerRegistry.instance().removeAll.connect(self.removeAllLayers)

        # For processing module
        self.destCrs = None

    @pyqtSlot('QStringList')
    def addLayers(self, layers: List[QgsMapLayer]) -> None:
        """Handle layers being added to the registry so they show up in canvas.

        :param layers: list<QgsMapLayer> list of map layers that were added

        .. note:: The QgsInterface api does not include this method,
            it is added here as a helper to facilitate testing.
        """
        #LOGGER.debug('addLayers called on qgis_interface')
        #LOGGER.debug('Number of layers being added: %s' % len(layers))
        #LOGGER.debug('Layer Count Before: %s' % len(self.canvas.layers()))
        current_layers = self.canvas.layers()
        final_layers = []
        for layer in current_layers:
            final_layers.append(QgsMapCanvasLayer(layer))
        for layer in layers:
            final_layers.append(QgsMapCanvasLayer(layer))

        self.canvas.setLayerSet(final_layers)
        #LOGGER.debug('Layer Count After: %s' % len(self.canvas.layers()))

    @pyqtSlot('QgsMapLayer')
    def addLayer(self, layer: QgsMapLayer) -> None:
        """Handle a layer being added to the registry so it shows up in canvas.

        :param layer: list<QgsMapLayer> list of map layers that were added

        .. note: The QgsInterface api does not include this method, it is added
                 here as a helper to facilitate testing.

        .. note: The addLayer method was deprecated in QGIS 1.8 so you should
                 not need this method much.
        """
        pass

    @pyqtSlot()
    def removeAllLayers(self) -> None:
        """Remove layers from the canvas before they get deleted."""
        self.canvas.setLayerSet([])

    def newProject(self) -> None:
        """Create new project."""
        # noinspection PyArgumentList
        QgsMapLayerRegistry.instance().removeAllMapLayers()

    # ---------------- API Mock for QgsInterface follows -------------------

    def zoomFull(self) -> None:
        """Zoom to the map full extent."""
        pass

    def zoomToPrevious(self) -> None:
        """Zoom to previous view extent."""
        pass

    def zoomToNext(self) -> None:
        """Zoom to next view extent."""
        pass

    def zoomToActiveLayer(self) -> None:
        """Zoom to extent of active layer."""
        pass

    def addVectorLayer(self, path: str, base_name: str, provider_key: str) -> None:
        """Add a vector layer.

        :param path: Path to layer.
        :type path: str

        :param base_name: Base name for layer.
        :type base_name: str

        :param provider_key: Provider key e.g. 'ogr'
        :type provider_key: str
        """
        pass

    def addRasterLayer(self, path: str, base_name: str) -> None:
        """Add a raster layer given a raster layer file name

        :param path: Path to layer.
        :type path: str

        :param base_name: Base name for layer.
        :type base_name: str
        """
        pass

    def activeLayer(self) -> Optional[QgsMapLayer]:
        """Get pointer to the active layer (layer selected in the legend)."""
        # noinspection PyArgumentList
        layers = QgsMapLayerRegistry.instance().mapLayers()
        for item in layers:
            return layers[item]

    def addToolBarIcon(self, action: QAction) -> None:
        """Add an icon to the plugins toolbar.

        :param action: Action to add to the toolbar.
        :type action: QAction
        """
        pass

    def removeToolBarIcon(self, action: QAction) -> None:
        """Remove an action (icon) from the plugin toolbar.

        :param action: Action to add to the toolbar.
        :type action: QAction
        """
        pass

    def addToolBar(self, name: str) -> None:
        """Add toolbar with specified name.

        :param name: Name for the toolbar.
        :type name: str
        """
        pass

    def mapCanvas(self) -> QgsMapCanvas:
        """Return a pointer to the map canvas."""
        return self.canvas

    def mainWindow(self) -> None:
        """Return a pointer to the main window.

        In case of QGIS it returns an instance of QgisApp.
        """
        pass

    def addDockWidget(self, area: Qt.DockWidgetArea, dock_widget: QDockWidget) -> None:
        """Add a dock widget to the main window.

        :param area: Where in the ui the dock should be placed.
        :type area:

        :param dock_widget: A dock widget to add to the UI.
        :type dock_widget: QDockWidget
        """
        pass

    def legendInterface(self) -> QgsMapCanvas:
        """Get the legend."""
        return self.canvas
