# -*- coding: utf-8 -*-
"""Testpaket für das bielefeldGEOSUCHE-Plugin.

Importiert QGIS-Bibliotheken, um die korrekte SIP-API-Version zu setzen,
bevor andere Module geladen werden.
"""

# import qgis libs so that ve set the correct sip api version
import qgis   # pylint: disable=W0611  # NOQA