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
    plugins.implements(plugins.IResourceController)

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
        schema['resources'].update({'is_automated_processed' : [toolkit.get_validator('ignore_missing')] })
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
        schema['resources'].update({'atmosphere' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'data_type' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'analysis_method' : [toolkit.get_validator('ignore_missing')] })
        schema['resources'].update({'is_automated_processed' : [toolkit.get_validator('ignore_missing')] })
        return schema


     #ITemplateHelpers

    def get_helpers(self):
        return {'is_plugin_enabled': Helper.is_plugin_enabled
        }
    

    # IResourceController

    def after_create(self, context, resource):
        if resource['url_type'] == 'upload':
            dataframe = []
            xls_dataframes = None
            if Helper.is_csv(resource):
                dataframe = Helper.csv_to_dataframe(resource['id'])
            elif Helper.is_xlsx(resource):
                xls_dataframes = Helper.xlsx_to_dataframe(resource['id'])
            else:
                return resource
            
            if len(dataframe) != 0:
                # resource is csv
                if not Helper.is_possible_to_automate(dataframe):
                    return resource
                
                resource['material_combination'] = Helper.get_metadata_value(dataframe, 'Werkstoff-1') + ', ' + Helper.get_metadata_value(dataframe, 'Werkstoff-2')
                resource['atmosphere'] = Helper.get_metadata_value(dataframe, 'Atmosphaere')
                resource['data_type'] = Helper.get_metadata_value(dataframe, 'Datentyp')
                resource['surface_preparation'] = Helper.get_metadata_value(dataframe, 'Vorbehandlung')
                resource['is_automated_processed'] = True

  
            
        return resource


    
    def before_create(self, context, resource):
        return resource

    def before_update(self, context, current, resource):
        return resource
    
    def after_update(self, context, resource):
        return resource
    
    def before_delete(self, context, resource, resources):
        return resources
    
    def after_delete(self, context, resources):
        return resources
    
    def before_show(self, resource_dict):
        return resource_dict