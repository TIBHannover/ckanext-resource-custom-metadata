import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import pandas as pd
from ckanext.resource_custom_metadata.lib.helper import Helper
from ckanext.resource_custom_metadata.controllers.base import BaseController
from flask import Blueprint


log = logging.getLogger(__name__)

CUSTOM_RESOURCE_FIELDS = [
    'material_combination',
    'surface_preparation',
    'atmosphere',
    'data_type',
    'analysis_method',
    'is_automated_processed',
]


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
        for field in CUSTOM_RESOURCE_FIELDS:
            schema['resources'].update({field: [toolkit.get_validator('ignore_missing')]})
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
        schema = self._custom_resource_schema(schema)
        return schema


     #ITemplateHelpers

    def get_helpers(self):
        return {'is_plugin_enabled': Helper.is_plugin_enabled
        }
    

    # IResourceController

    def before_resource_create(self, context, resource):
        pass

    def after_resource_create(self, context, resource):
        self._process_and_persist_resource_metadata(context, resource)

    def before_resource_update(self, context, current, resource):
        pass

    def after_resource_update(self, context, resource):
        self._process_and_persist_resource_metadata(context, resource)

    def before_resource_delete(self, context, resource, resources):
        pass

    def after_resource_delete(self, context, resources):
        pass

    def before_resource_show(self, resource_dict):
        pass

    def _process_and_persist_resource_metadata(self, context, resource):
        if context.get('resource_custom_metadata_skip_automation'):
            return

        metadata = self._extract_metadata_from_resource(resource)
        if not metadata:
            return

        patch = {'id': resource['id']}
        for field, value in metadata.items():
            if resource.get(field) != value:
                patch[field] = value

        if len(patch) == 1:
            return

        patch_context = dict(context)
        patch_context['resource_custom_metadata_skip_automation'] = True
        toolkit.get_action('resource_patch')(patch_context, patch)
        resource.update({field: patch[field] for field in patch if field != 'id'})

    def _extract_metadata_from_resource(self, resource):
        if resource.get('url_type') != 'upload':
            return {}

        try:
            if Helper.is_csv(resource):
                dataframe = Helper.csv_to_dataframe(resource['id'])
                return self._metadata_from_dataframe(dataframe)

            if Helper.is_xlsx(resource):
                xls_dataframes = Helper.xlsx_to_dataframe(resource['id'])
                for sheet_name, sheet_dataframe in xls_dataframes.items():
                    metadata = self._metadata_from_dataframe(sheet_dataframe)
                    if metadata:
                        return metadata
                return {}
        except (FileNotFoundError, OSError, UnicodeDecodeError, ValueError, KeyError, pd.errors.ParserError) as exc:
            log.info(
                'Could not automate custom metadata for resource %s: %s',
                resource.get('id'),
                exc,
            )

        return {}

    def _metadata_from_dataframe(self, dataframe):
        if dataframe is None or len(dataframe) == 0:
            return {}

        is_automated = Helper.is_possible_to_automate(dataframe)
        if not is_automated[0]:
            return {}

        if is_automated[1] == "v1":
            return {
                'material_combination': Helper.get_metadata_value(dataframe, 'Werkstoff-1') + ', ' + Helper.get_metadata_value(dataframe, 'Werkstoff-2'),
                'atmosphere': Helper.get_metadata_value(dataframe, 'Atmosphaere'),
                'data_type': Helper.get_metadata_value(dataframe, 'Datentyp'),
                'surface_preparation': Helper.get_metadata_value(dataframe, 'Vorbehandlung'),
                'is_automated_processed': True,
            }

        if is_automated[1] == "v2":
            return {
                'material_combination': Helper.get_metadata_value(dataframe, 'Material or Material Combination'),
                'atmosphere': Helper.get_metadata_value(dataframe, 'Atmosphere'),
                'data_type': Helper.get_metadata_value(dataframe, 'Data type (mechanical, chemical ...)'),
                'surface_preparation': Helper.get_metadata_value(dataframe, 'Surface Preparation'),
                'analysis_method': Helper.get_metadata_value(dataframe, 'Measurement/Analysis Method'),
                'is_automated_processed': True,
            }

        return {}
