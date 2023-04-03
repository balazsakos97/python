from google_api_auths.create_api_services import CreateServiceEndpoints
from googleapiclient.http import MediaFileUpload
import time

class UpdateSlides:
    '''
    This is a class that allows once to update designated presatation wiht PNGs located in the screen_shots folder    
    '''
    def __init__(self) -> None:
        self.folder_id = 'folder_id' # folder ID that is used to temporarily make images public (permissions revoked right after upload to slides)
        service = CreateServiceEndpoints().create_api_endpoints()
        self.drive = service['drive'] # Drive API endpoint
        self.slides = service['slides'] # Slides API endpoint

    def upload_pngs(self, upload_file_names=[], presentation_id='string', starting_slide = 1):
        presentation_id = presentation_id
        info = self.slides.presentations().get(presentationId=presentation_id, fields='slides').execute().get('slides',[]) # http request - returns Object with all available object information
        
        #Lines 19-31 unpacks the response object into the desired format
        element_array = []
        slides_array = []
        for i in range(len(info)):
            elements = info[i]['pageElements']
            pageId = info[i]['objectId']
            slides_array.append(pageId)
            for item in range(len(elements)):
                array = [pageId,elements[item]['objectId']]
                element_array.append(array)    
        start_num = starting_slide-1
        slides_to_change = slides_array[start_num:]
        total = len(upload_file_names)

        #Lines 34 - 93 updates the designated slides with their assigned PNG
        for n in range(len(upload_file_names)):
            pageObjectId = slides_to_change[n]
            uploadFilename = 'screen_shots/%s.png' % upload_file_names[n]

            elements_on_slide = []
            for element in element_array:
                if element[0] == pageObjectId:
                    elements_on_slide.append(element[1]) #create array with objectIds found on given slide
            for item in elements_on_slide: #This for loop deletes previous PNGs - All object uploaded using the slides API has the SLIDE_API string in their ID
                if 'SLIDES_API' in item: #If statement ensures that only relevant PNGs are deleted
                    reqs = [{'deleteObject': {'objectId': item}}]
                    self.slides.presentations().batchUpdate(body={'requests': reqs}, presentationId=presentation_id).execute()
                    print('{} deleted'.format(item))

            # 1. Upload a PNG file from local PC
            file_metadata = {'name': uploadFilename, 'parents': [self.folder_id]}
            media = MediaFileUpload(uploadFilename, mimetype='image/png')
            upload = self.drive.files().create(body=file_metadata, media_body=media, fields='webContentLink, id, webViewLink').execute()
            fileId = upload.get('id')
            url = upload.get('webContentLink')
            print('%i:%i Uploaded' % (n+1,total))

            # 2. Share publicly the uploaded PNG file by creating permissions.
            self.drive.permissions().create(fileId=fileId, body={'type': 'anyone', 'role': 'reader'}).execute()

            print('%i:%i PNG Shared' % (n+1,total))
            # 3. Insert the PNG file to the Slides.
            body = {
                "requests": [
                    {
                        "createImage": {
                            "url": url,
                            "elementProperties": {
                                "pageObjectId": pageObjectId,
                                'transform': {
                                    'scaleX': 1,
                                    'scaleY': 1, 
                                    'translateY': 685800, 
                                    'unit': 'EMU'
                                }
                            }
                        }
                    }
                ]
            }
            result = None
            while result is None:
                try:
                    # sometimes the request takes a few seconds for the permission change to take effect. In those cases, this section tries again after 5 seconds. 
                    result = self.slides.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
                    time.sleep(5) 
                except:
                    pass
            
                       
            print('%i:%i PNG Added to Slide' % (n+1,total))

            # 4. Delete the permissions. By this, the shared PNG file is closed.
            self.drive.permissions().delete(fileId=fileId, permissionId='anyoneWithLink').execute()
            print('%i:%i PNG Share Revoked' % (n+1,total))

            # 5. Remove file after it has been added to slide
            self.drive.files().delete(fileId=fileId).execute()
            print('%i:%i PNG Removed From Drive' % (n+1,total))
