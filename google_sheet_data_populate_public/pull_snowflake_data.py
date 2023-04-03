from sqlalchemy import create_engine
import pandas as pd



class PullSnowflakeData:
    def __init__(self):
        pass

    def create_engine(user, pswrd, accountid):
        
        engine = create_engine(
            'snowflake://{user}:{password}@{account_identifier}/'.format(
                user= user, 
                password= pswrd, 
                account_identifier= accountid, 
            )
        )
        connection = engine.connect()
        print('{} connection successfully created!'.format(user))
        engine.dispose()
        return connection

    def query_dwh(user, pswrd, accountid, query='string'):
        connection = PullSnowflakeData.create_engine(user=user, pswrd=pswrd, accountid=accountid)
        df = pd.read_sql(query,connection)
        print('Data successfully pulled')
        connection.close()
        return df