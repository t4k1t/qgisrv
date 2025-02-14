======
qgisrv
======

**NOTE: Technically this might still work, however, the dependencies haven't been updated in years and it's untested with current versions of QGIS.**

Simple web server to host QGIS plugins.

You will have to supply your own plugins.xml which tells QGIS where to find
packages. However qgisrv can serve these packages.

Authentication
==============
Per default all requests can be done unauthenticated. If you want
authentication you can enable basic auth in the settings.
