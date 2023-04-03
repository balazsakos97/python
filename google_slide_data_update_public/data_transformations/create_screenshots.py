from __future__ import print_function
from hashlib import new
import pandas as pd
from prep_dataframes import GoogleSheetValues
import imgkit

class CssFormattings():
    '''This class takes an array of DFs and turns them into PNGs by applying CSS formatting to it's HTML render'''
    def __init__(self):
        pass

    # define css formatting that should be applied
    def single_cell_no_variable(val, attr):
        return attr

    def apply_non_variable_css(data, attr_str):
        outp = []
        for i in data:
            outp.append(attr_str)
        return outp


    def add_background_color(data, color='grey'):
        attr = 'background-color: {}'.format(color)
        outp = []
        for i in data:
            outp.append(attr)
        return outp

    def change_text_color(data, color='white'):
        attr = 'color: {}'.format(color)
        outp = []
        for i in data:
            outp.append(attr)
        return outp

    def color_row_background(data, color='#efefef'):
        outp=[]
        if data[5] == '':
            attr='white'
        else:
            attr= color
        css = 'background-color: {}'.format(attr)
        for i in data:
            outp.append(css)
        return outp

    def colorcode_delta(data, delta_i=[11]):
        green = '#0b8043'
        red = '#cc0000'

        if data[2] == 'TRUE':
            reverse = True
        else:
            reverse = False

        if reverse:
            negative = green
            positive = red
        else:
            negative = red
            positive = green

        outp = []
        for i in range(len(data)):
            if i in delta_i:
                data_str = data[i]
                if '-' in data_str:
                    attr = 'color: {}'.format(negative)
                else:
                    attr = 'color: {}'.format(positive)
                outp.append(attr)
            else:
                outp.append('')  
        
        return outp
    
    def color_status_tickers(data):
        outp = []
        attr = ''
        for i in range(len(data)):
            if data[i] == 'Green':
                attr = 'background-color: #d9ead3'
            elif data[i] == 'Yellow':
                attr = 'background-color: #fff2cc'
            elif data[i] == 'Red': 
                attr = 'background-color: #f4cccc'
            else:
                attr = ''
            outp.append(attr)
        
        return outp

    def give_output_html(self, df): # this methoid applies the specific formatting and returns the HTML code of the tables
        s = df.style.\
            hide(axis='index').\
            hide(axis='columns').\
            hide(subset=[0,1,2,3], axis=1).\
            applymap(CssFormattings.single_cell_no_variable, attr='font: 18px Arial, sans-serif').\
            applymap(CssFormattings.single_cell_no_variable, attr='padding: 10px 15px').\
            applymap(CssFormattings.single_cell_no_variable, attr='white-space: nowrap').\
            applymap(CssFormattings.single_cell_no_variable, attr='text-align: right', subset=pd.IndexSlice[1:,8:]).\
            apply(CssFormattings.add_background_color, color='black', axis=1, subset=0).\
            apply(CssFormattings.change_text_color, axis=1, subset=0).\
            apply(CssFormattings.apply_non_variable_css, attr_str='font-weight: bold' , axis=1, subset=0).\
            apply(CssFormattings.apply_non_variable_css, attr_str='font-weight: bold' , axis=0, subset=[4,5,13,21]).\
            apply(CssFormattings.apply_non_variable_css, attr_str='border-bottom: 1px solid grey', axis=1, subset=pd.IndexSlice[1:,:]).\
            apply(CssFormattings.color_row_background, axis=1, subset=pd.IndexSlice[1:,:]).\
            apply(CssFormattings.colorcode_delta, delta_i=[13,21], axis=1, subset=pd.IndexSlice[1:,:]).\
            apply(CssFormattings.color_status_tickers, axis=0, subset=[6,7])

        html = s.to_html()
        print('DataFrame Formatted!')
        return html
    
    def turn_dfs_to_png(self, dataframe_array=[], prefix='unknown'): #this method takes the above methods and applies them on the chosen array of DFs
        file_names = []
        pref = prefix
        for i in range(len(dataframe_array)):
           html = CssFormattings.give_output_html(self, df=dataframe_array[i])
           number = i+1
           file_name = '%s_image_%i' % (pref,number)
           imgkit.from_string(html, 'screen_shots/%s.png' % file_name)
           file_names.append(file_name)
           print('%s image %i is done' % (pref,number))        
        return file_names