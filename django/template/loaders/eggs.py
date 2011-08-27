# Wrapper for loading templates from eggs via pkg_resources.resource_string.
from django.apps import cache

try:
    from pkg_resources import resource_string
except ImportError:
    resource_string = None

from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.conf import settings

class Loader(BaseLoader):
    is_usable = resource_string is not None

    def load_template_source(self, template_name, template_dirs=None):
        """
        Loads templates from Python eggs via pkg_resource.resource_string.

        For every installed app, it tries to get the resource (app, template_name).
        """
        if resource_string is not None:
            pkg_name = 'templates/' + template_name
            for app in cache.loaded_apps:
                try:
                    return (resource_string(app._meta.name, pkg_name).decode(settings.FILE_CHARSET), 'egg:%s:%s' % (app._meta.name, pkg_name))
                except Exception, e:
                    pass
        raise TemplateDoesNotExist(template_name)

_loader = Loader()
