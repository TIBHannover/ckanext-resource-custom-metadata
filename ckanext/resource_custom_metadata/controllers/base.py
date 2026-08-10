# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import render_template, request, redirect
import ckan.lib.helpers as h
from ckanext.resource_custom_metadata.lib.helper import Helper


class BaseController():

    def index(id):
        package = toolkit.get_action('package_show')({}, {'name_or_id': id})
        stages = True    
        resouces = package['resources']
        custom_metadata_fields = {'material_combination': [], 'surface_preparation': [], 'atmosphere': [], 'data_type': [], 'analysis_method': []}
        for meta in custom_metadata_fields.keys():
            for res in resouces:
                if  meta in res.keys() and res[meta] and res[meta] != '':
                    custom_metadata_fields[meta].append(res[meta])

        for meta in custom_metadata_fields.keys():
            custom_metadata_fields[meta] = list(set( custom_metadata_fields[meta])) 

        return render_template('add_view.html', 
            pkg_dict=package, 
            custom_stage=stages,
            custom_metadata_fields=custom_metadata_fields
        )
    

    def save_metadata():
        metadata_fields = ['material_combination', 'surface_preparation', 'atmosphere', 'data_type', 'analysis_method']
        package_name = request.form.get('pkg_name')
        
        try:
            for field in metadata_fields:
                input_prefix = field + '_'
                field_inputs = (
                    key for key in request.form.keys()
                    if key.startswith(input_prefix)
                    and key[len(input_prefix):].isdigit()
                )
                for input_name in field_inputs:
                    index = input_name[len(input_prefix):]
                    resource_ids = request.form.getlist(
                        'custom_metadata_' + field + '_' + index
                    )
                    field_text = request.form.get(input_name)

                    for res_id in resource_ids:                       
                        resource = toolkit.get_action('resource_show')({}, {'id': res_id})
                        resource[field] = field_text
                        toolkit.get_action('resource_update')({}, resource)
        
        except:
            # raise
            return toolkit.abort(500, "")

        if Helper.is_plugin_enabled("organization_group"): # if organization_group plugin exists:
            return redirect(h.url_for('organization_group.add_ownership_view', id=str(package_name) ,  _external=True)) 

        elif Helper.is_plugin_enabled("media_wiki"): # if media_wiki plugin exists
            return redirect(h.url_for('media_wiki.machines_view', id=str(package_name) ,  _external=True)) 

        return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True))
        
