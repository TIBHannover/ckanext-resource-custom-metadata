import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.resource_custom_metadata.lib.helper import Helper
from ckanext.resource_custom_metadata.controllers.base import BaseController
from flask import Blueprint


class ResourceCustomMetadataPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('public/statics', 'ckanext-resource-custom-metadata')
    

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__)        
        blueprint.add_url_rule(
            u'/resource_custom_metadata/index/<id>',
            u'index',
            BaseController.index,
            methods=['GET']
            )
        
        blueprint.add_url_rule(
            u'/resource_custom_metadata/save_metadata',
            u'save_metadata',
            BaseController.save_metadata,
            methods=['POST']
            )

        return blueprint


    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def _custom_resource_schema(self, schema):
        # Add our custom_resource_text metadata field to the schema
        schema['resources'].update({'material_combination' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'surface_preparation' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'atmosphere' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'data_type' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'analysis_method' : [toolkit.get_validator('ignore_missing')] })
        return schema

    def create_package_schema(self):
        schema = super(ResourceCustomMetadataPlugin, self).create_package_schema()
        schema = self._custom_resource_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(ResourceCustomMetadataPlugin, self).update_package_schema()
        schema = self._custom_resource_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(ResourceCustomMetadataPlugin, self).show_package_schema()
        schema['resources'].update({'material_combination' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'surface_preparation' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'Atmosphere' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'data_type' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'analysis_method' : [toolkit.get_validator('ignore_missing')] })
        return schema


     #ITemplateHelpers

    def get_helpers(self):
        return {'is_plugin_enabled': Helper.is_plugin_enabled
        }