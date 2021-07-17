import pandas as pd 
from data_update import *
import re

def get_data_update():
    df = pd.read_csv("resources.csv",encoding="iso-8859-1")
    for index, row in df.iterrows():
        print(row['Name of Service provider'], row['Contact person name'],row['City'], row['Phone No.'],row['Address'], row['Verified on (Date)'])

        text=f''' {row['City']}
                Service provider Name:{row['Name of Service provider']}
                Contact person:{row['Contact person name']}
                Phone No. : {row['Phone No.']}
                Address : {row['Address']}
                Type of Service: {row['Type of Service provided']}
                Note: {row['Additional']}
                Verified on : {row['Verified on (Date)']} 
                
                These details are fetched from multiple resources and social site,and verified on given date.\n
                
                '''     
        data_extractor(text)

def data_extractor(text):
    try:
        if text!="":
            city=text.split('\n', 1)[0]
            msg=text.split('\n', 1)[1]
            bed_list=["bed","Beds","Bed","ICU","BED","BEDS","icu","seat","Seat","beds"]
            oxygen_list=["cylinders","CYLINDERS","Cylinders","cylinders","CYLINDERS","Cylinders","Oxygen","OXYGEN","oxygen"]
            medcine_lit=["Remedesivir","remedesivir","REMEDESIVIR","Tocilzumab","tocilzumab","Medicine","MEDICINE","medicine","Fabiflu","fabiflu","Favipiravir","favipiravir"]
            plasma_list=["Blood","plasma","Plasma","PLASAMA","blood"]
            
            # any(re.findall(r'|'.join(a), str, re.IGNORECASE))
            if any(re.findall(r'|'.join(bed_list), msg, re.IGNORECASE)):
                cat_message="b" #bed
                # print ('possible matches thanks to regex')
            if any(re.findall(r'|'.join(oxygen_list), msg, re.IGNORECASE)) and  (any(re.findall(r'|'.join(bed_list), msg, re.IGNORECASE)))==False:
                cat_message="c" #cykinder
        
            if any(re.findall(r'|'.join(medcine_lit), msg, re.IGNORECASE)):
                cat_message="a" #medcine

            if any(re.findall(r'|'.join(plasma_list), msg, re.IGNORECASE)):
                cat_message="d" #plasma
                # print ('possible matches thanks to regex')
            city=city.replace(" ","")
            msg=msg.strip()
            print(city,cat_message,msg)
            write_data_to_db('covid_help2',city,cat_message,msg)
    except:
        pass

if __name__ == '__main__':
    get_data_update()

