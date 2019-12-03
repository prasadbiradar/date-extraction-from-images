# encoding=utf8
import sys







import csv
import boto3

from data import Data
from PIL import Image
import pytesseract
import cv2
import os
import re


class TestData:
    """docstring for TestData"""
    @staticmethod
    def get():
        data = Data()
        data.set('Filename', 'in.jpg')
        data.set('Extracted text', 'abc xxx def')
        return data

    @staticmethod
    def extract(filename):

        with open('credentials.csv', 'r') as input:
            next(input)
            reader = csv.reader(input)
            for line in reader:
                access_key_id = line[2]
                secret_access_key = line[3]


        client = boto3.client('rekognition',
                              aws_access_key_id=access_key_id,
                              aws_secret_access_key=secret_access_key, region_name='us-east-1')



        UPLOADED_FILE = '/root/Desktop/image_to_text_api2/image_to_text_api/temp_files/'+filename

        filename = "{}.png|jpeg|jpg".format(os.getpid())
        
        with open(UPLOADED_FILE, 'rb') as source_image:
            source_bytes = source_image.read()

        response = client.detect_text(Image={'Bytes': source_bytes})

        text = str(" ".join(re.findall(r"[a-z0-9\/\-\.\,]+", str(response), flags=re.I))).strip().title()
        text = re.sub(r"([a-z]+)([0-9]+)", r"\1 \2", text, flags=re.I)
        text = re.sub(r"([0-9]+)([a-z]+)", r"\1 \2", text, flags=re.I)

        l1=[]
        date=[]
        opt = dict()
        date_reg_exp2 = re.compile(r'detectedtext\s*[a-zA-Z0-9\s]{0,30}((?:(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])(?:\D)(?:0[1-9]|1[0-2])(?:\D)(?:(?:19[7-9]\d|20\d{2})|\d{2}))|(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)(?:\D)(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])(?:\D)(?:(?:19[7-9]\d|20\d{2})|\d{2}))|(?:(?:0[1-9]|1[0-2])(?:\D)(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])(?:\D)(?:(?:19[7-9]\d|20\d{2})|\d{2}))|(?:(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])(?:\D)(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)(?:\D)(?:(?:19[7-9]\d|20\d{2})|\d{2})))',flags=re.I)

        line = re.search(date_reg_exp2, str(text))

        if line:
            l1 =list(filter(None,line.groups()))    
            date=re.split('[- / . ' ' ]',l1[0])
            opt["date"] = [date[2] + "/" + date[1] + "/" + date[0]]
            
            return opt

        else:
            opt['date'] = "date is not present"
            return opt

        
        # os.remove(filename)

        # return text


