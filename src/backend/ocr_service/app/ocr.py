import easyocr
import torch
import base64


class OCR:
    #init models and parameters
    def __init__(self):
        self.device = True if torch.cuda.is_available() else False
        self.model = easyocr.Reader(['ru','en'], gpu=self.device) #lang codes for recognition

    #recognize image using easyocr pipeline
    def recognize(self, b64_string):
        image_data = base64.b64decode(b64_string)

        with open('out.png', 'wb') as file:
            file.write(image_data)

        result = self.model.readtext('out.png', detail=0)
        return result