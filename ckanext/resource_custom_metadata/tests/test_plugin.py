# encoding: utf-8

import csv
import io
from packaging.version import parse as parse_version

import ckan
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.tests import factories, helpers
from flask import Flask
import pandas as pd
import pytest

from ckanext.resource_custom_metadata.lib.helper import Helper
from ckanext.resource_custom_metadata.plugin import (
    CUSTOM_RESOURCE_FIELDS,
    ResourceCustomMetadataPlugin,
)


RESOURCE_ID = 'abcdef1234567890'


def csv_text(headers, row):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerow(row)
    return output.getvalue()


CSV_V1 = csv_text(
    [
        'X-Kategorie',
        'Y-Kategorie',
        'Datentyp',
        'Werkstoff-1',
        'Werkstoff-2',
        'Atmosphaere',
        'Vorbehandlung',
    ],
    ['load', 'elongation', 'mechanical', 'Steel', 'Aluminum', 'Air', 'Polished'],
)

CSV_V2 = csv_text(
    [
        'X-Category',
        'Y-Category',
        'Measurement/Analysis Method',
        'Material or Material Combination',
        'Atmosphere',
        'Data type (mechanical, chemical ...)',
        'Surface Preparation',
    ],
    ['time', 'current', 'EIS', 'Copper/Nickel', 'Argon', 'chemical', 'Ground'],
)


def write_resource_file(tmp_path, monkeypatch, content, suffix='.csv'):
    monkeypatch.setitem(toolkit.config, 'ckan.storage_path', str(tmp_path))
    path = tmp_path / 'resources' / RESOURCE_ID[0:3] / RESOURCE_ID[3:6] / RESOURCE_ID[6:]
    path.parent.mkdir(parents=True)
    if suffix == '.xlsx':
        with pd.ExcelWriter(str(path), engine='openpyxl') as writer:
            content.to_excel(writer, index=False, header=False)
    else:
        path.write_text(content, encoding='utf-8')
    return path


@pytest.mark.ckan_config('ckan.plugins', 'resource_custom_metadata')
def test_plugin_loads(with_plugins):
    assert plugins.plugin_loaded('resource_custom_metadata')


def test_custom_resource_fields_are_added_to_dataset_resource_schemas():
    plugin = ResourceCustomMetadataPlugin()

    for schema in (
        plugin.create_package_schema(),
        plugin.update_package_schema(),
        plugin.show_package_schema(),
    ):
        for field in CUSTOM_RESOURCE_FIELDS:
            assert field in schema['resources']
            assert schema['resources'][field] == [toolkit.get_validator('ignore_missing')]


def test_blueprint_routes_are_registered():
    blueprint = ResourceCustomMetadataPlugin().get_blueprint()
    flask_app = Flask(__name__)
    flask_app.register_blueprint(blueprint)

    routes = {rule.rule: rule.endpoint for rule in flask_app.url_map.iter_rules()}

    assert routes['/resource_custom_metadata/index/<id>'].endswith('.index')
    assert routes['/resource_custom_metadata/save_metadata'].endswith('.save_metadata')


@pytest.mark.ckan_config('ckan.plugins', 'resource_custom_metadata')
def test_blueprint_index_returns_404_for_missing_dataset(app, with_plugins):
    response = app.get('/resource_custom_metadata/index/missing-dataset')

    assert response.status_code == 404


@pytest.mark.ckan_config('ckan.plugins', 'resource_custom_metadata')
def test_save_metadata_rejects_invalid_form_data(app, with_plugins):
    response = app.post('/resource_custom_metadata/save_metadata', data={})

    assert response.status_code == 400


@pytest.mark.parametrize(
    ('configured_plugins', 'expected'),
    [
        ('resource_custom_metadata organization_group', True),
        (['resource_custom_metadata', 'organization_group'], True),
        (['resource_custom_metadata'], False),
    ],
)
def test_is_plugin_enabled_accepts_string_and_list_config(monkeypatch, configured_plugins, expected):
    monkeypatch.setitem(toolkit.config, 'ckan.plugins', configured_plugins)

    assert Helper.is_plugin_enabled('organization_group') is expected


def test_csv_v1_annotation_metadata_is_extracted(tmp_path, monkeypatch):
    write_resource_file(tmp_path, monkeypatch, CSV_V1)
    resource = {'id': RESOURCE_ID, 'url_type': 'upload', 'format': 'CSV', 'name': 'data.csv'}

    metadata = ResourceCustomMetadataPlugin()._extract_metadata_from_resource(resource)

    assert metadata == {
        'material_combination': 'Steel, Aluminum',
        'atmosphere': 'Air',
        'data_type': 'mechanical',
        'surface_preparation': 'Polished',
        'is_automated_processed': True,
    }


def test_csv_v2_annotation_metadata_is_extracted(tmp_path, monkeypatch):
    write_resource_file(tmp_path, monkeypatch, CSV_V2)
    resource = {'id': RESOURCE_ID, 'url_type': 'upload', 'format': 'CSV', 'name': 'data.csv'}

    metadata = ResourceCustomMetadataPlugin()._extract_metadata_from_resource(resource)

    assert metadata == {
        'material_combination': 'Copper/Nickel',
        'atmosphere': 'Argon',
        'data_type': 'chemical',
        'surface_preparation': 'Ground',
        'analysis_method': 'EIS',
        'is_automated_processed': True,
    }


def test_xlsx_annotation_metadata_is_extracted(tmp_path, monkeypatch):
    dataframe = pd.DataFrame([
        [
            'X-Category',
            'Y-Category',
            'Measurement/Analysis Method',
            'Material or Material Combination',
            'Atmosphere',
            'Data type (mechanical, chemical ...)',
            'Surface Preparation',
        ],
        ['time', 'current', 'SEM', 'Titanium', 'Vacuum', 'mechanical', 'Etched'],
    ])
    write_resource_file(tmp_path, monkeypatch, dataframe, suffix='.xlsx')
    resource = {'id': RESOURCE_ID, 'url_type': 'upload', 'format': 'XLSX', 'name': 'data.xlsx'}

    metadata = ResourceCustomMetadataPlugin()._extract_metadata_from_resource(resource)

    assert metadata['material_combination'] == 'Titanium'
    assert metadata['analysis_method'] == 'SEM'
    assert metadata['is_automated_processed'] is True


@pytest.mark.parametrize(
    'resource',
    [
        {'id': RESOURCE_ID, 'url_type': 'link', 'format': 'CSV', 'name': 'data.csv'},
        {'id': RESOURCE_ID, 'url_type': 'upload', 'format': 'TXT', 'name': 'data.txt'},
    ],
)
def test_non_automatable_resources_are_unchanged(resource):
    assert ResourceCustomMetadataPlugin()._extract_metadata_from_resource(resource) == {}


def test_malformed_uploaded_resource_is_unchanged(monkeypatch):
    resource = {'id': RESOURCE_ID, 'url_type': 'upload', 'format': 'CSV', 'name': 'data.csv'}
    monkeypatch.setattr(Helper, 'csv_to_dataframe', lambda resource_id: (_ for _ in ()).throw(ValueError('bad csv')))

    assert ResourceCustomMetadataPlugin()._extract_metadata_from_resource(resource) == {}


def test_programming_errors_are_not_suppressed(monkeypatch):
    resource = {'id': RESOURCE_ID, 'url_type': 'upload', 'format': 'CSV', 'name': 'data.csv'}
    monkeypatch.setattr(Helper, 'csv_to_dataframe', lambda resource_id: (_ for _ in ()).throw(TypeError('bug')))

    with pytest.raises(TypeError):
        ResourceCustomMetadataPlugin()._extract_metadata_from_resource(resource)


def test_generated_metadata_is_persisted_with_resource_patch(monkeypatch):
    plugin = ResourceCustomMetadataPlugin()
    resource = {'id': RESOURCE_ID, 'url_type': 'upload', 'format': 'CSV', 'name': 'data.csv'}
    monkeypatch.setattr(
        plugin,
        '_extract_metadata_from_resource',
        lambda resource: {'material_combination': 'Steel', 'is_automated_processed': True},
    )
    calls = []

    def get_action(name):
        assert name == 'resource_patch'

        def resource_patch(context, data_dict):
            calls.append((context, data_dict))

        return resource_patch

    monkeypatch.setattr(toolkit, 'get_action', get_action)

    plugin.after_resource_create({'user': 'tester'}, resource)

    assert calls == [
        (
            {'user': 'tester', 'resource_custom_metadata_skip_automation': True},
            {'id': RESOURCE_ID, 'material_combination': 'Steel', 'is_automated_processed': True},
        )
    ]
    assert resource['material_combination'] == 'Steel'
    assert resource['is_automated_processed'] is True


def test_skip_flag_prevents_recursive_resource_patch(monkeypatch):
    plugin = ResourceCustomMetadataPlugin()
    resource = {'id': RESOURCE_ID, 'url_type': 'upload', 'format': 'CSV', 'name': 'data.csv'}
    monkeypatch.setattr(plugin, '_extract_metadata_from_resource', lambda resource: pytest.fail('should not extract'))

    plugin.after_resource_update({'resource_custom_metadata_skip_automation': True}, resource)


def test_legacy_resource_hook_methods_are_not_defined_on_plugin():
    legacy_hooks = [
        'before_create',
        'after_create',
        'before_update',
        'after_update',
        'before_delete',
        'after_delete',
        'before_show',
    ]

    for hook in legacy_hooks:
        assert hook not in ResourceCustomMetadataPlugin.__dict__


def test_before_resource_show_returns_resource_unchanged():
    resource = {'id': RESOURCE_ID}

    assert ResourceCustomMetadataPlugin().before_resource_show(resource) is resource


@pytest.mark.skipif(parse_version(ckan.__version__) < parse_version('2.10'), reason='CKAN 2.10 resource hooks are required')
@pytest.mark.ckan_config('ckan.plugins', 'resource_custom_metadata')
@pytest.mark.ckan_config('ckan.uploads_enabled', True)
def test_generated_custom_metadata_survives_resource_create_and_show(clean_db, create_with_upload, with_plugins):
    dataset = factories.Dataset()

    resource = create_with_upload(
        CSV_V2,
        'annotated.csv',
        context={'ignore_auth': True},
        package_id=dataset['id'],
        url='upload',
        name='annotated.csv',
        format='CSV',
    )
    shown = helpers.call_action('resource_show', id=resource['id'])

    assert shown['material_combination'] == 'Copper/Nickel'
    assert shown['atmosphere'] == 'Argon'
    assert shown['data_type'] == 'chemical'
    assert shown['surface_preparation'] == 'Ground'
    assert shown['analysis_method'] == 'EIS'
    assert shown['is_automated_processed'] is True
