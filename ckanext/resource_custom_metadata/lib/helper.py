# encoding: utf-8

import os.path

import ckan.plugins.toolkit as toolkit
import clevercsv
import pandas as pd


STANDARD_HEADERS_V1 = ['X-Kategorie', 'Y-Kategorie', 'Datentyp', 'Werkstoff-1', 'Werkstoff-2', 'Atmosphaere', 'Vorbehandlung']
STANDARD_HEADERS_V2 = ['X-Category', 'Y-Category', 'Measurement/Analysis Method', 'Material or Material Combination', 'Atmosphere', 'Data type (mechanical, chemical ...)', 'Surface Preparation']


class Helper():

    def is_plugin_enabled(plugin_name):
        plugins = toolkit.config.get("ckan.plugins", "")
        if plugin_name in plugins.split():
            return True
        return False
    

    @staticmethod
    def is_possible_to_automate(resource_df):
        df_columns = resource_df.columns
        df_columns = [i.strip() for i in df_columns]
        answer = True        
        for annot in STANDARD_HEADERS_V1:
            if annot not in df_columns:
                answer = False
                break
        
        if answer:
            return [True, "v1"]
                
        if not df_columns:
            return [False, ""]

        for col in df_columns:
            if "Data type" in col:
                if "Data type (mechanical, chemical " not in col:
                    return [False, ""]
            else:
                if col not in STANDARD_HEADERS_V2:
                    return [False, ""]
            
        
        return [True, "v2"]
        

    
    @staticmethod
    def get_metadata_value(dataframe, column_title):
        if column_title == "Data type (mechanical, chemical ...)":
            for col in dataframe.columns:
                if "Data type (mechanical, chemical" in col:
                    if len(list(dataframe[col])) < 1:
                        return ''
                    
                    value = list(dataframe[col])[0]
                    return '' if pd.isna(value) else value


        if len(list(dataframe[column_title])) < 1:
            return ''
        
        value = list(dataframe[column_title])[0]
        return '' if pd.isna(value) else value


    @staticmethod
    def resource_file_path(resource_id):
        storage_path = toolkit.config.get('ckan.storage_path')
        if not storage_path:
            raise RuntimeError('ckan.storage_path is not configured')

        return os.path.join(
            storage_path,
            'resources',
            resource_id[0:3],
            resource_id[3:6],
            resource_id[6:],
        )


    @staticmethod
    def csv_to_dataframe(resource_id):
        '''
            Read a csv file as pandas dataframe.

            Args:
                - resource_id: the data resource id in ckan
            
            Returns:
                - a python dataframe
        '''

        file_path = Helper.resource_file_path(resource_id)
        df = clevercsv.read_dataframe(file_path, encoding='utf-8')
        df = df.fillna('')

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
        file_path = Helper.resource_file_path(resource_id)
        data_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
        for sheet, data_f in data_sheets.items():
            temp_df = data_f.dropna(how='all').dropna(how='all', axis=1)
            if len(temp_df) > 0:
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
            format = resource.get('format') or ''
            name = resource.get('name') or resource.get('url') or ''
        else:
            format = resource.format or ''
            name = resource.name or ''
        
        return (format.upper() in ['CSV']) or name.lower().endswith('.csv')

    
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
            format = resource.get('format') or ''
            name = resource.get('name') or resource.get('url') or ''
        else:
            format = resource.format or ''
            name = resource.name or ''
        
        return (format.upper() in ['XLSX']) or name.lower().endswith('.xlsx')
