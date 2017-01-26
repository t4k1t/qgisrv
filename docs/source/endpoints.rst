.. _endpoints:

Endpoints
*********

``qgisrv`` provides a handful of endpoints which are explained on this page.

.. _root_endpoint:

/
===

Simply returns plugin manifest.

   .. note::

      The manifest returned here is read directly from the disk so it might
      actually differ from the loaded manifest. However, calling the /refresh
      endpoint will reload the manifest from the disk.

.. _refresh_endpoint:

/refresh
========

Reloads the plugin manifest from the disk. Useful if you have added or updated
metadata of a plugin.

*Example Request*
   .. code-block:: bash

      GET /refresh

*Example Response*
   .. code-block:: bash

      ""

.. _plugins_endpoint:

/plugins/<plugin name>
======================

Returns metadata of the latest version of the specified plugin.

*Example Request*
   .. code-block:: bash

      GET /plugins/myplugin

.. _packages_endpoint:

/packages/<package-file.zip>
============================

Delivers plugin package file for installation in QGIS.

.. _static_endpoint:

/static
=======

Static content.
