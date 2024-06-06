import easyocr
import torch


class OCR:
    #init models and parameters
    def __init__(self):
        self.device = 'cpu'
        self.model = easyocr.Reader(['ru','en']) #lang codes for recognition

    #recognize image using easyocr pipeline
    def recognize(self, filename):
        result = self.model.readtext(filename, detail = 0)
        return result