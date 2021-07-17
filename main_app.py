import json
import requests
import time
import re
from data_update import *
TOKEN= "1596204291:AAG-WpZ1QuQaqKWA1JvQc00KW0NFzL5imXo"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
# dbname ="telegram_db"
# tablename ='test'

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def internetcheck():
	success = False
	attempts = 0
	while not success and attempts < 15: # or however many times you want to attempt
		#print("00000000 success:",success,attempts)
		try:
			js=get_updates(offset=None)
			print('internetcheck js',js)
			success = True
		except:
			time.sleep(5)
			print("---url attempts:",attempts)
			attempts+=1
		
	return js

def main():
	try:
		count=0
		last_update_id = None
		#print("main coreapp stage1")
		while True:
			# count+=1;print(count,end=",")
			# if count==100:
			# 	text=" bot Status : Running"
			# 	send_message(751552666,URL,text)
			# 	print("###---Server is running Current Time",datetime.datetime.now(),"---###")
			# 	count=0

			try:
				updates = get_updates(last_update_id)
			except:
				updates =internetcheck()
				
			if len(updates["result"]) > 0:
				last_update_id = get_last_update_id(updates) + 1
				data_parsar(updates)
			time.sleep(0.1)

	except Exception as err:
		print("---main function implementation failed(66,CoreApp.py)---",err)
		pass

def data_parsar(updates):

    num_updates = len(updates["result"])
    last_update = num_updates - 1
    # last_msg=updates["result"][last_update]
    # print(last_msg)
    chat_type=updates["result"][last_update]["message"]["chat"]["type"]
    if chat_type=="private":
        text = updates["result"][last_update]["message"]["text"]
        # print(text)
        # return text
        data_extractor(text)

def data_extractor(text):
    if text!="":
        city=text.split('\n', 1)[0]
        msg=text.split('\n', 1)[1]
        bed_list=["bed","Beds","Bed","ICU","BED","BEDS","icu","seat","Seat","beds"]
        oxygen_list=["cylinders","CYLINDERS","Cylinders","cylinders","CYLINDERS","Cylinders","Oxygen","OXYGEN","oxygen"]
        medcine_lit=["Remedesivir","remedesivir","REMEDESIVIR","Tocilzumab","tocilzumab","Medcine","MEDCINE","medcine","Fabiflu","fabiflu","Favipiravir","favipiravir"]
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

if __name__ == '__main__':
    main()

