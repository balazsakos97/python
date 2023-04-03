from __future__ import print_function
import pandas as pd
from google_api_auths.create_api_services import CreateServiceEndpoints


class GoogleSheetValues:
    '''
    This class stages the data found in a specified google sheet and turns them into DFs according to the calibrations provided in the sheet
    '''
    def __init__(self) -> None:
        self.data_spreadsheet_id = 'data_spreadsheet_id' #ID of spreadsheet where the WBR sheet data is imported to (in order to avoid performance issues)
        self.range = "range!A1:W" #sheet and range of data
        service = CreateServiceEndpoints().create_api_endpoints()
        service = service['sheets']
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.data_spreadsheet_id, range=self.range).execute()
        self.values = result.get('values', [])
        self.df = pd.DataFrame(self.values)
        self.title_row = self.df.iloc[1:2]

    def create_wbr_tables(self, num_sect=1): #ready DFs needed for WBR presentations
        df = self.df
        df_wbr = df[df[1] == 'TRUE']
        wbr_sect = num_sect
        i = 1
        wbr_df_array = []
        while i <= wbr_sect:
            df_wbr_subsection = df_wbr[df_wbr[3] == '{}'.format(i)]
            df_wbr_subsection = pd.concat([self.title_row,df_wbr_subsection], ignore_index = True)
            wbr_df_array.append(df_wbr_subsection)
            i+=1

        print('wbr data ready')
        return wbr_df_array

    def create_mbr_tables(self, num_sect=1): #ready DFs needed for MBR presentations
        df = self.df
        df_mbr = df[df[0] == 'TRUE']
        mbr_sect = num_sect
        b = 1
        mpr_df_array = []
        while b <= mbr_sect:
            df_mpr_subsection = df_mbr[df_mbr[3] == '{}'.format(b)]
            df_mpr_subsection = pd.concat([self.title_row,df_mpr_subsection], ignore_index = True)
            mpr_df_array.append(df_mpr_subsection)
            b+=1

        print('mpr data ready')
        return mpr_df_array
    
    def create_combined(self): # create an array with all possible DFs - in case it is needed in the future
        mpr = self.create_mbr_tables()
        wbr = self.create_wbr_tables()
        combined = {
            'mpr': mpr,
            'wbr': wbr
        }
        return combined

def main():
    main = GoogleSheetValues().create_combined()
    print ('done')

    
if __name__ == "__main__":
    main()