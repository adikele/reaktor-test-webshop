'''
GET /products/:category – Return a listing of products in a given category.
GET /availability/:manufacturer – Return a list of availability info.
The APIs are running at https://bad-api-assignment.reaktor.com/.

To do their work efficiently, the warehouse workers need a fast and simple listing page per product category, 
where they can check simple product and availability information from a single UI.

Yes, all ids from accessories displayed in 21 seconds!
As expected, only 5 manuf names printed (because there are only 5 of them!)
'''
import time

import json
import requests
from flask import Flask
from flask import redirect, render_template, request

app = Flask(__name__)

@app.route("/")
def index(): 
    t0 = time.time() 
    api_address =  "https://bad-api-assignment.reaktor.com/products/accessories"
    MAX_TRIES = 3
    tries = 0
    response = None

    while True:
        response = requests.get(api_address)
        if response.status_code == 500 and tries < MAX_TRIES:
            tries += 1
            continue
        break
    
    response_str = response.json()

    id_dict = { }
    availability_info_dict = { } 
    
    i = 0
    for a in response_str:
            i +=1 
            current_id = a["id"]
            current_name = a["name"]
            id_dict[current_id] = [current_name] 

            api_address_manuf = "https://bad-api-assignment.reaktor.com/availability/"  
            manufacturer = a["manufacturer"]
            api_address_manuf += manufacturer
            current_id_upper = current_id.upper()   
           
            #if manufacturer already encountered earlier
            if manufacturer in availability_info_dict.keys():
                for a in availability_info_dict[manufacturer]:
                    current_id_new = a["id"]
                    if current_id_new == current_id_upper:
                        availability_info_product = a["DATAPAYLOAD"]                   
                id_dict[current_id].append(availability_info_product)  

            else:
                availability_info = find_manuf_name(api_address_manuf, current_id_upper) 
                for a in availability_info:
                    current_id_new = a["id"]
                    if current_id_new == current_id_upper:
                        availability_info_product = a["DATAPAYLOAD"]                   
                id_dict[current_id].append(availability_info_product)

                availability_info_dict[manufacturer] = availability_info 
    
    t1 = time.time()
    nsec = t0-t1  
    print (nsec)

    return render_template("index.html", main_info= id_dict, info_out = availability_info_product) 

def find_manuf_name(api,id):
    '''
    Takes a product id and API for the availability data
    Returns availability data for a particular product
    '''
    #print (id)  #deleting
    MAX_TRIES = 3
    tries = 0
    while True:
        response = requests.get(api)
        if response.status_code == 500 and tries < MAX_TRIES:
            tries += 1
            continue
        break
      
    response_str = response.json()
    info = response_str ["response"]
    print (id)
    return info
 
if __name__ == '__main__':
    app.debug = True
    app.run()

