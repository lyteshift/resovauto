import requests
import json
import pprint
import datetime

today = str(datetime.datetime.today()).split()[0]
yesterday = str(datetime.datetime.today()-datetime.timedelta(days=1)).split()[0]
tomorrow = str(datetime.datetime.today()+datetime.timedelta(days=1)).split()[0]



headers = {
    "accept": "application/json",
    "X-API-KEY": "yNkdOIZtkMdfKR24xIMP6ZbpMv049a125lhxQL57O8wG2v07GGknrw9q70mn9H"
}

def resova(target):
    response = requests.get(target, headers=headers)
    response_dejson = json.loads(response.text)

    return response_dejson

def get_rooms():

    items_api = "https://api.resova.co.uk/v1/items"

    response = resova(items_api)

    room_list = []

    for rooms in response["data"]:
        room_list.append(rooms["id"])
    return room_list



print(get_rooms())
count = 0
for rooms in get_rooms():

    avail_req = "https://api.resova.co.uk/v1/availability/calendar?start_date="+today+"&end_date="+today+"&item_ids="+str(rooms)

    for instances in resova(avail_req)["data"][today]["items"]:
        for availability in instances["instances"]:
            print(availability["availability"]["spaces"]["booked"], availability["booking_customer"])
            count += availability["availability"]["spaces"]["booked"]
print(count," TOTAL CUSTOMERS TODAY")

avail_id = "https://api.resova.co.uk/v1/availability/instance/YTo1OntpOjA7czoxOiJmIjtpOjE7aToyNTtpOjI7czo4OiIyMDI0MTIwNyI7aTozO3M6MToiYSI7aTo0O2k6NzIyOTk7fQ"
#pprint.pprint(resova(avail_id))
    