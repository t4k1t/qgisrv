"""qgisrv authentication helpers."""

import base64
import crypt
import logging
import functools

from settings import settings


class BasicAuth(object):
    """Basic Authentication helper class."""

    @staticmethod
    def basic_auth(auth_func=lambda *args, **kwargs: True,
                   after_login_func=lambda *args, **kwargs: None,
                   realm='Restricted'):
        """Basic auth helper."""
        def basic_auth_decorator(handler_class):
            def wrap_execute(handler_execute):
                def require_basic_auth(handler, kwargs):
                    def create_auth_header():
                        handler.set_status(401)
                        handler.set_header(
                            'WWW-Authenticate', 'Basic realm=%s' % realm)
                        handler._transforms = []
                        handler.finish()

                    if settings['auth']['required'] is False:
                        logging.debug("skipping authentication")
                        return

                    auth_header = handler.request.headers.get('Authorization')

                    if (auth_header is None or not
                            auth_header.startswith('Basic ')):
                        create_auth_header()
                    else:
                        auth_decoded = base64.b64decode(
                            auth_header[6:]).decode()
                        user, pwd = auth_decoded.split(':', 2)

                        if auth_func(user, pwd):
                            after_login_func(handler, kwargs, user, pwd)
                        else:
                            create_auth_header()

                def _execute(self, transforms, *args, **kwargs):
                    require_basic_auth(self, kwargs)
                    return handler_execute(self, transforms, *args, **kwargs)

                return _execute

            handler_class._execute = wrap_execute(handler_class._execute)
            return handler_class
        return basic_auth_decorator

    @staticmethod
    def check_credentials(user, password):
        """Compare login to list of authorized users."""
        login = "{}:{}\n".format(
            user, crypt.crypt(
                password, base64.b64encode(password.encode()).decode()))
        if login in authorized_users():
            return True
        else:
            logging.debug("invalid basic auth credentials")
            return False


@functools.lru_cache(maxsize=1)
def authorized_users():
    """Read list of authorized users from file."""
    acceptable = set()
    with open(settings['auth']['basic_auth']['path'], 'r') as f:
        acceptable = set(f.readlines())
    return acceptable
