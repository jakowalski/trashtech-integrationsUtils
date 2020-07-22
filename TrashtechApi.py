import requests


class TrashtechApi:
    api_base = 'http://trashtech.herokuapp.com/api'

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

        response = requests.post(url, json=request_json)
        json = response.json()
        return json