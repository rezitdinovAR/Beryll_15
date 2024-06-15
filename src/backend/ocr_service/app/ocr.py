import easyocr
import torch
import base64


class OCR:
    #init models and parameters
    def __init__(self):
        self.device = True if torch.cuda.is_available() else False
        self.model = easyocr.Reader(['ru','en'], gpu=self.device) #lang codes for recognition

    #recognize image using easyocr pipeline
    def recognize(self, b64_strings,size):


        temps = []


        for i in range(len(b64_strings)):
            image_data = base64.b64decode(b64_strings[i])


            with open(f'out{i}.png', 'wb') as file:
                file.write(image_data)
                temps.append(f'out{i}.png')
            
        print(size)
        results = self.model.readtext_batched(temps,n_width=size[0],n_height=size[1], detail=0)
        return results