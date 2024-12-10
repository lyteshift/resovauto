import requests
import json
import datetime
from rich import print
from rich.progress import track
import os

title = """                                                          [bold blue]/[/bold blue]   
[bold white]           ___  __   ___  __  [/bold white][bold blue][bold blue]    __   ___  __   __      /[/bold blue][bold red]          ___  __  [/bold red]
[bold white]            |  / _` |__  / _` [/bold white][bold blue][bold blue]   |__) |__  /__` /  \ \  / [/bold blue][bold red] /\  |  |  |  /  \ [/bold red]
[bold white]            |  \__> |___ \__> [/bold white][bold blue][bold blue]   |  \ |___ .__/ \__/  \/  [/bold blue][bold red]/  \ \__/  |  \__/ [/bold red]
[bold white]           Written by George Cash-Blackmore[/bold white]    [bold red]v1.0.0-alpha.3 "Chlorophytum"[/bold red]
                                                        [bold red]/[/bold red]"""

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
    for rooms in track(get_rooms(),"    [bold green]Getting daily customers...[/bold green]"):

        avail_req = "https://api.resova.co.uk/v1/availability/calendar?start_date="+date+"&end_date="+date+"&item_ids="+str(rooms)

        for instances in resova(avail_req)["data"][date]["items"]:
            if instances["item_id"] != 133:
                for availability in instances["instances"]:
                   count += availability["availability"]["spaces"]["booked"]

    return(count)

def count_daily_customers_fast(date):
    count = 0
    all_rooms = get_rooms()
    avail_req = "https://api.resova.co.uk/v1/availability/calendar?start_date="+date+"&end_date="+date+"&item_ids="
    print(avail_req)
    for instances in resova(avail_req)["data"][date]["items"]:
            if instances["item_id"] != 133:
                for availability in instances["instances"]:
                   count += availability["availability"]["spaces"]["booked"]

    return(count)

def get_daily_instances(date):
    all_instances = []
    for rooms in track(get_rooms(),"    [bold green]Getting booking data...[/bold green] "):

        avail_req = "https://api.resova.co.uk/v1/availability/calendar?start_date="+date+"&end_date="+date+"&item_ids="+str(rooms)
        for items in resova(avail_req)["data"][date]["items"]:
            for instances in items["instances"]:
                all_instances.append(instances["instance_id"])
    return(all_instances)

def get_presales(date):

    daily_instances = get_daily_instances(date)

    total_presales = 0
    item_extras_total = 0.00

    for instance in track(daily_instances,"    [bold green]Calculating pre-sales...[/bold green]"):
        
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

    for instance in track(daily_instances,"    [bold green]Calculating pre-sales...[/bold green]"):
        booking = resova("https://api.resova.co.uk/v1/availability/instance/"+instance)
        if booking["bookings"] != []:
            if booking["bookable"] == False:
                if booking["type"] != "blocked":
                    if booking["bookings"][0]["item"]["id"] != 133:
                        if booking["bookings"][0]["transaction"]["formatted"]["created_d_string"] == date:
                            count += 1
    return count


def main():
    while True:
        cls()
        print(title)
        print("[bold blue]   Welcome to the Resovauto CLI[/bold blue]")
        print("""   [orange1]Choose an option from below to begin...[/orange1]
   [1] Daily customers (exc. RA/ID)  [2] Daily presales  [3] Same-day bookings 
   [red][0] Exit (ctrl+c)[/red]
            """)
        userinput = input(": ")
        if userinput == "0":
            break
        if userinput == "1":
            cls()
            print(title)
            print("[bold white]   For which day?[/bold white]")
            print("""   [orange1]Choose an option from below...[/orange1]
   \[today] \[yesterday] \[YYYY-MM-DD]
                  """)
            date = input(": ")
            print("")
            if date == "today":
                date = today
            if date == "yesterday":
                date = yesterday
            try:
                
                cls()
                print(title)
                print("")
                print(count_daily_customers_fast(date),"customers visited on",date)
                if input("Continue? [y/n]? ") == "n":
                    break
            except:
                #cls()
                print(title)
                print("\n[red]ERROR! Maybe you typed the date wrong?[/red]")
                if input("Try again? [y/n]? ") == "n":
                    break
        if userinput == "2":
            
            cls()
            print(title)
            print("[bold white]   For which day?[/bold white]")
            print("""   [orange1]Choose an option from below...[/orange1]
   \[today] \[yesterday] \[YYYY-MM-DD]
                  """)
            date = input(": ")
            print("")
            if date == "today":
                date = today
            if date == "yesterday":
                date = yesterday
            try:
                
                cls()
                print(title)
                presales = get_presales(date)
                print("\n",presales," total presale drinks on",date)
                print("£",presales*4.00,"total value @ £4.00/token")
                if input("Continue? [y/n]? ") == "n":
                    break
            except:
                
                cls()
                print(title)
                print("\n[red]ERROR! Maybe you typed the date wrong?[/red]")
                if input("Try again? [y/n]? ") == "n":
                    break
        if userinput == "3":
            cls()
            print(title)
            print("[bold white]   For which day?[/bold white]")
            print("""   [orange1]Choose an option from below...[/orange1]
   \[today] \[yesterday] \[YYYY-MM-DD]
                  """)
            date = input(": ")
            print("")
            if date == "today":
                date = today
            if date == "yesterday":
                date = yesterday
            try:
                cls()
                print(title)
                same_day = get_same_day(date)
                print(same_day,"same day bookings on",date)
                if input("Continue? [y/n]? ") == "n":
                    break
            except:
                cls()
                print(title)
                print("\n[red]ERROR! Maybe you typed the date wrong?[/red]")
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


main()