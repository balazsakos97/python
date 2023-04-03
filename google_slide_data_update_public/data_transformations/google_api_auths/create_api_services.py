from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account


class CreateServiceEndpoints:
    '''
    This is a support Class in order to speed up the service endpoint creation
    Potential ToDo: add endpoint variable so not all endpoints are opened, but only the one that is required based on the input (drive, sheets, slides)
    '''
    def __init__(self) -> None:
        self.scopes = (
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/presentations',
            'https://www.googleapis.com/auth/drive'
        )
        self.service_account_file = 'google_api_auths/project-key.json' #ToDo : add service account auth JSON
        self.credentials = service_account.Credentials.from_service_account_file(self.service_account_file, scopes=self.scopes)
    
    def create_api_endpoints(self):        
        sheets_api = build('sheets', 'v4', credentials=self.credentials)
        drive_api = build('drive', 'v3', credentials=self.credentials)
        slides_api = build('slides', 'v1', credentials=self.credentials)
        api_endpoints = {
            'drive': drive_api,
            'sheets': sheets_api,
            'slides': slides_api
        }
        return api_endpoints