"""qgisrv main module."""

import functools
import logging

import tornado.ioloop
import tornado.web
from lxml import etree

from authentication import BasicAuth
from settings import settings


@BasicAuth.basic_auth(BasicAuth.check_credentials)
class ManifestRefreshHandler(tornado.web.RequestHandler):
    """Refresh manifest."""

    def get(self):
        """Clear manifest cache."""
        read_manifest.cache_clear()
        logging.debug("cleared manifest cache")


@BasicAuth.basic_auth(BasicAuth.check_credentials)
class PluginXMLHandler(tornado.web.RequestHandler):
    """Handle plugin metadata."""

    def get(self, name):
        """Deliver metadata of specified package."""
        root = read_manifest()
        plugin = find_plugin(root, name)
        if plugin is not None:
            updated = plugin.findtext("update_date")
            self.write("""<html>
  <head></head>
  <body>
    <h2>{}</h2>
    <h3>Version</h3>
    {}
    <h3>Last Updated</h3>
    {}
  </body>
</html>""".format(name, plugin.get("version"), updated))
        else:
            self.set_status(404)
            self.write("<html><title>404: Not Found</title><body>404: Not "
                       "Found</body></html>")
            self.finish()


@functools.lru_cache(maxsize=1)
def read_manifest():
    """Read package manifest.

    Returns lxml root element.

    """
    logging.debug("reading manifest")
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(settings['manifest'], parser)
    root = tree.getroot()
    return root


def find_plugin(root, name, version=None):
    """Find first matching plugin element in tree root."""
    eligible = []
    for plugin in root.iterfind("pyqgis_plugin"):
        if plugin.get("name", None) == name:
            if version:
                if plugin.get("version", None) == version:
                    return plugin
            else:
                eligible.append((plugin.get("version", None), plugin))
    if eligible:
        eligible.sort()
        return eligible.pop()[1]
    return None


def make_app():
    """Create the tornado."""
    return tornado.web.Application([
        (r"/refresh", ManifestRefreshHandler),
        (r"/plugins/([a-zA-Z]+)", PluginXMLHandler),
        (r"/()", tornado.web.StaticFileHandler, {
            "path": settings['packagepath'],
            "default_filename": "plugins.xml"}),
        (r"/packages/([a-zA-Z]+\.zip)", tornado.web.StaticFileHandler, {
            "path": settings['packagepath']}),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {
            "path": settings['staticpath']}),
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {
            "path": settings['staticpath']}),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(int(settings['server']['port']))
    logging.debug("starting main loop")
    tornado.ioloop.IOLoop.current().start()
