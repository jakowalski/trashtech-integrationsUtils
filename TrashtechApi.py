import requests
import json

class TrashtechApi:
    api_base = 'https://trashtech-core-staging.herokuapp.com/api'

    def create_status(self, device_reference,encoded_image, image_created_at):


        request_json = {
            "device_status": {
                "image_created_at": image_created_at,
                "image_base": "data:image/jpg;base64,%s" % encoded_image.decode('utf-8'),
                "device_reference": device_reference,
                "container_identifier_number": device_reference,
            }
        }

        url = "%s/device_statuses/" % (self.api_base)
        requestBody =  json.dumps(request_json)
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=requestBody, headers=headers)
        jsonResult = response
        return jsonResult
