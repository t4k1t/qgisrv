.. _configuration:

Configuration
*************

Configuration happens via  a simple dictionary  in the ``settings.py`` located
in the ``qgisrv`` folder.

settings.py
===========

Per default the settings dictionary in ``settings.py`` will look something
like this:

   .. code-block:: python

      settings = {
          'log': {
              'level': "debug",  # log level
          },
          'auth': {
              'required': False,  # set to `True` to enable authentication
              'basic_auth': {
                  'path': '/dev/null',  # path to htpasswd file
              },
          },
          'server': {
              'port': 1779,  # port :-P
          },
          'staticpath': '/dev/null',  # path to static files
          'packagepath': '/dev/null',  # path to qgis plugins
      }

To change settings just change the appropriate values of the ``settings``
dictionary.

E.g. to enable basic auth you could make the following changes to the ``auth``
part of the dict:

   .. code-block:: python

       'auth': {
           'required': True,
           'basic_auth': {
               'path': '/home/exampleuser/qgisrv/users.htpasswd',
           },
        },
