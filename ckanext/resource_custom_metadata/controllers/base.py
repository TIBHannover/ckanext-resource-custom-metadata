# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import render_template, request, redirect
import ckan.lib.helpers as h
from ckanext.resource_custom_metadata.lib.helper import Helper


class BaseController():

    def index(id):
        package = toolkit.get_action('package_show')({}, {'name_or_id': id})
        stages = ['complete', 'complete', 'active', 'uncomplete', 'uncomplete']
        if not Helper.is_plugin_enabled('media_wiki'):
            stages = ['complete', 'complete', 'active', 'uncomplete']
        
        return render_template('add_view.html', pkg_dict=package, custom_stage=stages)