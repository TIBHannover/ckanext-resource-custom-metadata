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
    

    def save_metadata():
        metadata_fields = ['material_combination', 'surface_preparation', 'atmosphere', 'data_type', 'analysis_method']
        resource_count = request.form.get('resources_count')
        package_name = request.form.get('pkg_name')
        
        try:
            for field in metadata_fields:
                for i in range(1, int(resource_count) + 1):
                    resource_ids = request.form.getlist('custom_metadata_' + field + '_' + str(i))
                    field_text = request.form.get(field + '_' + str(i))

                    for res_id in resource_ids:
                        resource = toolkit.get_action('resource_show')({}, {'id': res_id})
                        resource[field] = field_text
                        toolkit.get_action('resource_update')({}, resource)
        
        except:
            return '0'


        if Helper.is_plugin_enabled("organization_group"): # if organization_group plugin exists:
            return redirect(h.url_for('organization_group.add_ownership_view', id=str(package_name) ,  _external=True)) 

        elif Helper.is_plugin_enabled("media_wiki"): # if media_wiki plugin exists
            return redirect(h.url_for('media_wiki.machines_view', id=str(package_name) ,  _external=True)) 

        return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True)) 
        
        