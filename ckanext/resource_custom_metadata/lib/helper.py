# encoding: utf-8

import ckan.plugins.toolkit as toolkit

class Helper():

    def is_plugin_enabled(plugin_name):
        plugins = toolkit.config.get("ckan.plugins")
        if plugin_name in plugins:
            return True
        return False
