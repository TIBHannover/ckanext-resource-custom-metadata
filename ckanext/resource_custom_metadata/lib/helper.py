# encoding: utf-8

import ckan.plugins.toolkit as toolkit
import clevercsv
import pandas as pd


RESOURCE_DIR = toolkit.config['ckan.storage_path'] + '/resources/'


class Helper():

    def is_plugin_enabled(plugin_name):
        plugins = toolkit.config.get("ckan.plugins")
        if plugin_name in plugins:
            return True
        return False
    

    @staticmethod
    def csv_to_dataframe(resource_id):
        '''
            Read a csv file as pandas dataframe.

            Args:
                - resource_id: the data resource id in ckan
            
            Returns:
                - a python dataframe
        '''

        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        df = clevercsv.read_dataframe(file_path)
        df = df.fillna(0)

        return df


    @staticmethod
    def xlsx_to_dataframe(resource_id):
        '''
            Read a xlsx file as pandas dataframe.

            Args:
                - resource_id: the data resource id in ckan
            
            Returns:
                - a dictionary where key is the sheet name and value is a dataframe
        '''

        result_df = {}
        file_path = RESOURCE_DIR + resource_id[0:3] + '/' + resource_id[3:6] + '/' + resource_id[6:]
        data_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
        for sheet, data_f in data_sheets.items():
            temp_df = data_f.dropna(how='all').dropna(how='all', axis=1)
            headers = temp_df.iloc[0]
            final_data_df  = pd.DataFrame(temp_df.values[1:], columns=headers)
            result_df[sheet] = final_data_df

        return result_df
    

    @staticmethod
    def is_csv(resource):
        '''
            Check if a data resource in csv or not.

            Args:
                - resource: the data resource object.
            
            Returns:
                - Boolean        
        '''
        format = ''
        name = ''
        if isinstance(resource, dict):
            format = resource['format']
            name = resource['name']
        else:
            format = resource.format
            name = resource.name
        
        return (format in ['CSV']) or ('.csv' in name)

    
    @staticmethod
    def is_xlsx(resource):
        '''
            Check if a data resource in xlsx or not.

            Args:
                - resource: the data resource object.
            
            Returns:
                - Boolean        
        '''

        format = ''
        name = ''
        if isinstance(resource, dict):
            format = resource['format']
            name = resource['name']
        else:
            format = resource.format
            name = resource.name
        
        return (format in ['XLSX']) or ('.xlsx' in name)
