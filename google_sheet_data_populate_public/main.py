from pull_snowflake_data import PullSnowflakeData
from update_gsheet import UpdateGoogleSheet

user='user'
pswrd='pswrd'
accountid='xyz.abc-1'
q="""
  select * from table limit 10
  """

pull = PullSnowflakeData
df = pull.query_dwh(user=user, pswrd=pswrd, accountid=accountid, query=q)
df.info()

spreadsheet_id = 'spreadsheet_id'
sheet_id=0
array=df.to_numpy()

UpdateGoogleSheet.updateGsheet(spreadsheet_id=spreadsheet_id,sheet_id=0, data=array)
