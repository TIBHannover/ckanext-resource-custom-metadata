import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class ResourceCustomMetadataPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm, inherit=False)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'resource_custom_metadata')

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def _custom_resource_schema(self, schema):
        # Add our custom_resource_text metadata field to the schema
        schema['resources'].update({
                'custom_resource_text' : [ toolkit.get_validator('ignore_missing') ]
                })
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

        schema['resources'].update({
                'custom_resource_text' : [ toolkit.get_validator('ignore_missing') ]
            })
        return schema
