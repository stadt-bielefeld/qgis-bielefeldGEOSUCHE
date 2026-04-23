# bielefeldGEOSUCHE

Official geosearch functionality, just for Bielefeld!

This Plugin brings the search functionality from the bielefeldGEOCLIENT and other Bielefeld services to QGIS. You can search for addresses, cadastre parcels, coordinates in EPSG:25832 and EPSG:4326, POIs, streets with all associated parcels and several other themes. 

The results can include all geometry types: points, lines and polygons. The geosearch you need in Bielefeld :-)

For the development of this plugin the artificial intelligences ChatGPT and Microsoft Copilot has been used.

## Installation

### Option 1: Install from official QGIS Plugin Repository

* Open the Plugin repository in QGIS and search for bielefeldGEOSUCHE
* Click Install
* That's all! You should see the search bar in the QGIS GUI and you can start searching :-)

### Option 2: Install from ZIP

* Make sure this folder is named `bielefeldGEOSUCHE` and zip this folder, e.g. into `bielefeldGEOSUCHE.zip`
* In QGIS > Plugins > Install from ZIP, select `bielefeldGEOSUCHE.zip`
* That's all! You should see the search bar in the QGIS GUI and you can start searching :-)

### Option 3: Clone directly into the QGIS plugins folder

This is useful if you want to update or modify the plugin without re-zipping.

First, find your QGIS plugins folder:

* **Windows:** `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
* **macOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
* **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`

Then clone this repository into that folder and make sure the folder is named `bielefeldGEOSUCHE`:

```bash
cd <plugins-folder>
git clone https://github.com/stadt-bielefeld/qgis-bielefeldGEOSUCHE bielefeldGEOSUCHE
```

Restart QGIS and enable the plugin under Plugins > Manage and Install Plugins.

On Linux and macOS you can alternatively create a symlink to a clone located elsewhere:

```bash
ln -s /path/to/qgis-bielefeldGEOSUCHE ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/bielefeldGEOSUCHE
```