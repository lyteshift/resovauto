import requests
import json
import datetime
from rich import print
from rich.progress import track
import os

title = """[bold orange1]
       ___  __   ___  __      __   ___  __   __                 ___  __  
        |  / _` |__  / _`    |__) |__  /__` /  \ \  /  /\  |  |  |  /  \ 
        |  \__> |___ \__>    |  \ |___ .__/ \__/  \/  /  \ \__/  |  \__/ 
[/bold orange1][magenta]
                        Written by George Cash-Blackmore
                           Open to feature requests[/magenta][red bold] <3[/red bold]
"""

# // RESOVAUTO
# Written by George Cash-Blackmore
# for The Great Escape Game
# Copyright 2024

# // ROOM IDs
# RAID ID.133

# DATE SETTERS
today = str(datetime.datetime.today()).split()[0]
yesterday = str(datetime.datetime.today()-datetime.timedelta(days=1)).split()[0]
tomorrow = str(datetime.datetime.today()+datetime.timedelta(days=1)).split()[0]

last_output = "None"

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

    return response_dejson

def get_rooms():

    items_api = "https://api.resova.co.uk/v1/items"

    response = resova(items_api)

    room_list = []

    for rooms in response["data"]:
        room_list.append(rooms["id"])
    return room_list

def count_daily_customers(date):
    count = 0
    for rooms in track(get_rooms(),"    [bold green]Getting daily customers...[/bold green]"):

        avail_req = "https://api.resova.co.uk/v1/availability/calendar?start_date="+date+"&end_date="+date+"&item_ids="+str(rooms)

        for instances in resova(avail_req)["data"][date]["items"]:
            #pprint.pprint(instances)
            if instances["item_id"] != 133:
                for availability in instances["instances"]:
                    #print(availability["availability"]["spaces"]["booked"], availability["booking_customer"])
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
    for instance in track(daily_instances,"    [bold green]Calculating pre-sales...[/bold green]"):
        booking = resova("https://api.resova.co.uk/v1/availability/instance/"+instance)
        if booking["bookable"] == False:
            if booking["type"] != "blocked":
                if booking["bookings"][0]["item"]["id"] != 133:
                    #print("-----------------------------")
                    #print("got a booking here!")
                    #pprint.pprint(booking["bookings"][0]["quantities"])
                    for tickets in booking["bookings"][0]["quantities"]:
                        #if tickets["pricing_category"]["single_price"] == "22.00":
                        #print(tickets["quantity"],"standard tickets")
                        #if tickets["pricing_category"]["single_price"] == "18.00":
                        #print(tickets["quantity"],"concession tickets")
                        if tickets["pricing_category"]["single_price"] == "26.00":
                        #print(tickets["quantity"],"tree tickets (1 presale)")
                            total_presales += tickets["quantity"] * 1
                        if tickets["pricing_category"]["single_price"] == "30.00":
                            #print(tickets["quantity"],"reindeer tickets (2 presale)")
                            total_presales += tickets["quantity"] * 2
                        if tickets["pricing_category"]["single_price"] == "38.00":
                            #print(tickets["quantity"],"santa tickets (4 presale)")
                            total_presales += tickets["quantity"] * 4
                    #print(total_presales,"total presales")
    return total_presales
        
def main():
    while True:
        cls()
        print(title)
        print("[bold magenta]Welcome to the Resovauto CLI[/bold magenta]")
        if last_output != "None":
            print("Previous output:",last_output)
        print("""
    [orange1]Choose an option from below to begin...[/orange1]
    [1] Daily customers (exc. RA/ID) [2] Daily presales
    [red][0] Exit (ctrl+c)[/red]
            """)
        userinput = input(": ")
        if userinput == "0":
            break
        if userinput == "1":
            cls()
            print(title)
            print("For which day? ")
            print("""
    [orange1]Choose an option from below...[/orange1]
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
                print(count_daily_customers(date),"customers visited on",date)
                if input("Continue? [y/n]? ") == "n":
                    break
            except:
                
                cls()
                print(title)
                print("\nERROR! Maybe you typed the date wrong?")
                if input("Try again? [y/n]? ") == "n":
                    break
        if userinput == "2":
            
            cls()
            print(title)
            print("For which day? ")
            print("""
    [orange1]Choose an option from below...[/orange1]
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
                print("\n",get_presales(date),"total presales on",date)
                if input("Continue? [y/n]? ") == "n":
                    break
            except:
                
                cls()
                print(title)
                print("\nERROR! Maybe you typed the date wrong?")
                if input("Try again? [y/n]? ") == "n":
                    break

main()