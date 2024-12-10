import requests
import json
import datetime
from rich import print
from rich.progress import track
import os

title = """                                                          [bold deep_sky_blue1]/[/bold deep_sky_blue1]   
[bold white]           ___  __   ___  __  [/bold white][bold deep_sky_blue1][bold deep_sky_blue1]    __   ___  __   __      /[/bold deep_sky_blue1][bold deep_pink2]          ___  __  [/bold deep_pink2]
[bold white]            |  / _` |__  / _` [/bold white][bold deep_sky_blue1][bold deep_sky_blue1]   |__) |__  /__` /  \ \  / [/bold deep_sky_blue1][bold deep_pink2] /\  |  |  |  /  \ [/bold deep_pink2]
[bold white]            |  \__> |___ \__> [/bold white][bold deep_sky_blue1][bold deep_sky_blue1]   |  \ |___ .__/ \__/  \/  [/bold deep_sky_blue1][bold deep_pink2]/  \ \__/  |  \__/ [/bold deep_pink2]
[bold white]           Written by George Cash-Blackmore[/bold white]        [bold deep_pink2]v1.0.0-beta.1 "Strelizia"[/bold deep_pink2]
                                                        [bold deep_pink2]/[/bold deep_pink2]"""

# // RESOVAUTO
# Written by George Cash-Blackmore
# for The Great Escape Game
# Copyright 2024

# // Room IDs
king_arthur = 25
underworld = 26
subs1 = 27
nhih = 29
abd = 87
subs2 = 89
raid60_id = 133
cgl = 136

# // Deprecated Room IDs
haunted = 105
raid45_id = 127

# // Other IDs
meeting_per_hour = 107
meeting_per_person = 109
cocktails = 118

active_rooms = [king_arthur,underworld,nhih,cgl,abd,subs1,subs2]

# Date Setters
today = str(datetime.datetime.today()).split()[0]
yesterday = str(datetime.datetime.today()-datetime.timedelta(days=1)).split()[0]
tomorrow = str(datetime.datetime.today()+datetime.timedelta(days=1)).split()[0]

#Cost Values
item_extras_value = 4.00

just_launched = True

api_calls = 0

key = open("key.txt")
headers = {
    "accept": "application/json",
    "X-API-KEY": str(key.read())
}
key.close()

def cls(): # Terminal clear function taken from StackOverflow lol
    os.system('cls' if os.name=='nt' else 'clear')

def resova(target):
    response = requests.get(target, headers=headers)
    response_dejson = json.loads(response.text)
    global api_calls
    api_calls += 1
    return response_dejson

def get_rooms():
    items_api = "https://api.resova.co.uk/v1/items"

    response = resova(items_api)
    room_list = []

    for rooms in response["data"]:
        if rooms["id"] in active_rooms:
            room_list.append(rooms["id"])

    return room_list

def get_rooms_verbose():
    items_api = "https://api.resova.co.uk/v1/items"

    response = resova(items_api)
    room_list = []

    for rooms in response["data"]:
        if rooms["id"] in active_rooms:
            room_list.append([rooms["id"],rooms["name"]])
        
    return room_list

def count_daily_customers(date):
    count = 0
    for rooms in track(get_rooms(),"    [bold sea_green2]Getting daily customers...[/bold sea_green2]"):

        avail_req = "https://api.resova.co.uk/v1/availability/calendar?start_date="+date+"&end_date="+date+"&item_ids="+str(rooms)

        for instances in resova(avail_req)["data"][date]["items"]:
            if instances["item_id"] != 133:
                for availability in instances["instances"]:
                   count += availability["availability"]["spaces"]["booked"]

    return(count)

def get_daily_instances(date):
    all_instances = []
    for rooms in track(get_rooms(),"    [bold sea_green2]Getting booking data...[/bold sea_green2] "):

        avail_req = "https://api.resova.co.uk/v1/availability/calendar?start_date="+date+"&end_date="+date+"&item_ids="+str(rooms)
        for items in resova(avail_req)["data"][date]["items"]:
            for instances in items["instances"]:
                all_instances.append(instances["instance_id"])
    return(all_instances)

def get_presales(date):

    daily_instances = get_daily_instances(date)

    total_presales = 0
    item_extras_total = 0.00

    for instance in track(daily_instances,"    [bold sea_green2]Calculating pre-sales...[/bold sea_green2]"):
        
        booking = resova("https://api.resova.co.uk/v1/availability/instance/"+instance)

        if booking["bookings"] != []:
            if booking["bookable"] == False:
                if booking["type"] != "blocked":
                    if booking["bookings"][0]["item"]["id"] != 133:
                        for tickets in booking["bookings"][0]["quantities"]:
                            if tickets["pricing_category"]["single_price"] == "26.00":
                                total_presales += tickets["quantity"] * 1

                            if tickets["pricing_category"]["single_price"] == "30.00":
                                total_presales += tickets["quantity"] * 2

                            if tickets["pricing_category"]["single_price"] == "38.00":
                                total_presales += tickets["quantity"] * 4
                        extras = booking["bookings"][0]["extras"]
                        try: 
                            item_extras_total += float(extras[0]["total"])
                        except:
                            pass

    total_presales += (item_extras_total/item_extras_value)
    return total_presales

def get_same_day(date):

    daily_instances = get_daily_instances(date)
    count = 0

    for instance in track(daily_instances,"    [bold sea_green2]Counting bookings...    [/bold sea_green2]"):
        booking = resova("https://api.resova.co.uk/v1/availability/instance/"+instance)
        if booking["bookings"] != []:
            if booking["bookable"] == False:
                if booking["type"] != "blocked":
                    if booking["bookings"][0]["item"]["id"] != 133:
                        if booking["bookings"][0]["transaction"]["formatted"]["created_d_string"] == date:
                            count += 1
    return count

last_output = ""
last_output_msg = ""
last_output_date = ""

def set_last_output(output,msg,date):
    global last_output
    global last_output_msg
    global last_output_date
    global just_launched

    last_output = output
    last_output_msg = msg
    last_output_date = date   
    just_launched = False



def print_footer():
    print("""   [deep_sky_blue1][/deep_sky_blue1][bold white on deep_sky_blue1] {last_output} [/bold white on deep_sky_blue1][deep_pink2 on deep_sky_blue1][/deep_pink2 on deep_sky_blue1][bold white on deep_pink2] {msg} {date} [/bold white on deep_pink2][deep_pink2][/deep_pink2]
""".format(last_output=last_output,msg=last_output_msg,date=last_output_date))

def main():
    while True:
        cls()
        print(title)
        print("""   [orange1][/orange1][bold black on orange1]Choose an option from below to begin...[/bold black on orange1][orange1][/orange1]
              
   [1] Daily customers (exc. RA/ID)  [2] Daily presales  [3] Same-day bookings 
   [deep_pink2][0] Exit (ctrl+c)[/deep_pink2]  [bold sea_green2]\[help][/bold sea_green2]
            """)
        
        global just_launched
        if not just_launched:
            print_footer()
        
        userinput = input(": ")
        if userinput == "0":
            break
        if userinput == "1":
            cls()
            print(title)
            print("""   [orange1][/orange1][bold black on orange1]For which day?[/bold black on orange1][orange1][/orange1]
   \[[bold deep_sky_blue1]t[/bold deep_sky_blue1]oday] \[[bold deep_sky_blue1]y[/bold deep_sky_blue1]esterday] \[YYYY-MM-DD]
                  """)
            date = input(": ")
            print("")
            if date == "today" or date == "t":
                date = today
            if date == "yesterday" or date ==  "y":
                date = yesterday
            try:
                
                cls()
                print(title)
                print("")
                total_customers = count_daily_customers(date)
                print(total_customers,"customers visited on",date)
                set_last_output(total_customers,"customers visited on",date)
                if input("Continue? [y/n]? ") == "n":
                    break
            except:
                cls()
                print(title)
                print("\n[deep_pink2]ERROR! Maybe you typed the date wrong?[/deep_pink2]")
                if input("Try again? [y/n]? ") == "n":
                    break
        if userinput == "2":
            
            cls()
            print(title)
            print("""   [orange1][/orange1][bold black on orange1]For which day?[/bold black on orange1][orange1][/orange1]
   \[[bold deep_sky_blue1]t[/bold deep_sky_blue1]oday] \[[bold deep_sky_blue1]y[/bold deep_sky_blue1]esterday] \[YYYY-MM-DD]
                  """)
            date = input(": ")
            print("")
            if date == "today" or date == "t":
                date = today
            if date == "yesterday" or date ==  "y":
                date = yesterday
            try:
                
                cls()
                print(title)
                presales = get_presales(date)
                print("\n",presales," total presale drinks on",date)
                print("£",presales*4.00,"total value @ £4.00/token")
                set_last_output(str("£"+str(presales*4.00)),"total presales value on",date)
                if input("Continue? [y/n]? ") == "n":
                    break
            except:
                
                cls()
                print(title)
                print("\n[deep_pink2]ERROR! Maybe you typed the date wrong?[/deep_pink2]")
                if input("Try again? [y/n]? ") == "n":
                    break
        if userinput == "3":
            cls()
            print(title)
            print("""   [orange1][/orange1][bold black on orange1]For which day?[/bold black on orange1][orange1][/orange1]
   \[[bold deep_sky_blue1]t[/bold deep_sky_blue1]oday] \[[bold deep_sky_blue1]y[/bold deep_sky_blue1]esterday] \[YYYY-MM-DD]
                  """)
            date = input(": ")
            print("")
            if date == "today" or date == "t":
                date = today
            if date == "yesterday" or date ==  "y":
                date = yesterday
            try:
                cls()
                print(title)
                same_day = get_same_day(date)
                print(same_day,"same day bookings on",date)
                set_last_output(same_day,"same day bookings on",date)
                if input("Continue? [y/n]? ") == "n":
                    break
            except:
                cls()
                print(title)
                print("\n[deep_pink2]ERROR! Maybe you typed the date wrong?[/deep_pink2]")
                if input("Try again? [y/n]? ") == "n":
                    break
        if userinput == "debug":
            cls()
            print(title)
            print("[bold orange1]   ++DEBUG++[/bold orange1]")
            print("   Check documentation for debug features")
            debuginput = input(": ")
            if debuginput == "instance_id":
                print(get_daily_instances(today))
                print("   Holding for input...")
            if debuginput == "avail":
                print(resova("https://api.resova.co.uk/v1/availability/calendar?start_date="+today+"&end_date="+today))
                print("   Holding for input...")
            if debuginput == "rooms":
                print(get_rooms_verbose())
                print("   Holding for input...")
            if debuginput == "calls":
                print(api_calls,"api calls since start.")

            if input(": "):
                pass
        if userinput == "help":
            cls()
            print(title)
            print("""   [sea_green2][/sea_green2][bold black on sea_green2]Help Page                                                                          [/bold black on sea_green2][sea_green2][/sea_green2]
   In the main menu, type one of the listed numbers to access a function. Must functions
   will ask you for a date, you may type "today", "yesterday", or any date in the format
   "YYYY-MM-DD", where YYYY is the year, MM, is the month, and DD is the day. 
   
   If you find your input isn't working, the most likely problem is a misformed input,
   so make sure you've included a dash "-" on your date input, and don't have any spaces
   " " before or after the input.
   
   """)
            if input("Return to menu? [y/n]? ") == "n":
                break

main()