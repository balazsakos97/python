from prep_dataframes import GoogleSheetValues
from create_screenshots import CssFormattings
from update_slides import UpdateSlides


presentation_id = 'presentation_id' #ToDo: Update with actual WBR Slide ID -- Share slides with service account email
start_slide = 10 #ToDo: Update with the number of the first slide a DF shopuld be displayed on

#Invoke Google Sheets py to create the DF and stage them for usage -- return array of DFs (sliced according to sections)
dfs = GoogleSheetValues().create_wbr_tables(num_sect=10)

#Using custom .py assign CSS formatting to DF then turn them into .png
new_files = CssFormattings().turn_dfs_to_png(dataframe_array=dfs,prefix='wbr')

#Remove old PNGs and upload new ones
UpdateSlides().upload_pngs(upload_file_names=new_files,presentation_id=presentation_id, starting_slide=start_slide)
print('All WBR Slides are updated!')
