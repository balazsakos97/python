from google_api_auths.create_api_services import CreateServiceEndpoints


class UpdateGoogleSheet:
    def updateGsheet(spreadsheet_id='string',sheet_id=0, data=[]):
        service = CreateServiceEndpoints().create_api_endpoints()
        service = service['sheets']
        maxr=len(data)
        maxc=len(data[1])
        tot = maxr * maxc
        b=0
        for i in range(len(data)):
            for f in range(len(data[i])):
                b = b+1
                print('{}/{} Fields Updated'.format(b,tot), end='\r')
                startR = i
                startC = f
                endR = startR+1
                endC = startC+1
                value = data[i][f]
                v_type = type(value)

                if v_type is bool:
                    types = 'boolValue'
                elif v_type is int:
                    types = 'numberValue'
                else:
                    value = str(value)
                    types = 'stringValue'
                
                reqs = [
                    {'repeatCell':{
                        'range':    {
                                    "sheetId": sheet_id,
                                    "startRowIndex": startR,
                                    "endRowIndex": endR,
                                    "startColumnIndex": startC,
                                    "endColumnIndex": endC
                                    },
                        'cell': {"userEnteredValue": {types: value}},
                        'fields': '*'
                    }},
                ]
                
                service.spreadsheets().batchUpdate(body={'requests': reqs}, spreadsheetId=spreadsheet_id).execute()
        print('Done')




