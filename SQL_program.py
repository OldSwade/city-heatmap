# -*- coding: utf-8 -*-
"""
Author : Morgan Mootoosamy
Date : 06/12/2024 (MM/DD/YYYY)
Updated : 07/09/2024 (MM/DD/YYYY)
Title : SQL program
File : SQL_program.py
"""

# Import necessary libraries
from pathlib import Path
import json
import os
import csv
from heatmap import heatmap_create  # heatmap_create function is imported from the file heatmap.py
import sqlite3

# Check if the scans_TXT9.txt file exists and has content
if os.path.isfile("scans_TXT9.txt") and os.path.getsize("scans_TXT9.txt") > 0:
    
    # Process to prepare the text from scans_TXT9.txt for JSON parsing
    print("JSON Format process for SQL db ...")
    
    # Read and preprocess the original text
    original_txt = Path('scans_TXT9.txt').read_text(encoding="utf8")
    original_txt = original_txt.replace('\n','')
    original_txt = original_txt.replace('\'s','s')
    original_txt = original_txt.replace('\\', '/')
    original_txt = original_txt.replace(':\"\"', ':\"\'')
    original_txt = original_txt.replace('\"\",','\'\",')
    
    # Parse JSON text into a Python dictionary
    txt = ""
    where_start = -2
    where_end = -2
    while where_start != -1 and where_end != -1:
        where_start = original_txt.find('[')
        where_end = original_txt.find('}],+')
        where_end += 3
        
        if where_start > -1 and where_end > -1:
            if original_txt[where_start+1] == '{':
                time_scan = original_txt[where_end+1:where_end+9]
                nv_txt = original_txt[where_start:where_end-1]
                nv_txt = nv_txt.replace('[{', ',[[\"'+time_scan+'\"],[{')
                nv_txt = nv_txt.replace('}]','}]]')
                txt += nv_txt
    
            original_txt = original_txt[where_end+9:]
    txt = '[' + txt[1:] + ']'
    dict_txt = json.loads(txt)  # Convert the processed text into a dictionary
    
    print("[COMPLETE]")
    
    # User input for date selection
    day = str(input("Please select a day (in DD format) : "))
    month = str(input("Please select a month (in MM format) : "))
    year = str(input("Please select a year (in YYYY format) : "))
    
    # Date string formation
    date_string = year + "-" + month + "-" + day
    
    # Type conversion and data manipulation on the dictionary
    print("Variable typing process ...")
    for scan in dict_txt:
        for net in scan[1]:
            net['Time'] = scan[0][0]
            net['Lat'] = float(scan[1][0]['Lat'])
            net['Long'] = float(scan[1][0]['Long'])
            net['id'] = int(net['id'])
            net['RSSI'] = int(net['RSSI'])
            net['CH'] = int(net['CH'])
        scan.pop(0)
        scan.pop(0)
    
    print("[COMPLETE]")
    
    # Data cleanup and standardization
    print("Replacing obsolete data in non-covered areas ...")
    for i in range(len(dict_txt)):
        for dicti in dict_txt[i]:
            if len(dict_txt[i]) == 1:
                if dicti['SSID'] == "Iphone de Alexis" or dicti['SSID'] == "LR-FHSS Mobile Plateform" or dicti['SSID'] == "ESP32-Access-Point-Morgan":
                    dicti['SSID'] = 'None'
                    dicti['BSSID'] = 'None'
                    dicti['RSSI'] = -999
                    dicti['Enc'] = 'None'
                    dicti['CH'] = -1
        print(round(((i+1)*100/len(dict_txt)),2),"%")
    print("[COMPLETE]")
    
    # Remove unnecessary data
    print("Removal of unnecessary data ...")
    for i in range(len(dict_txt)):
        for j in range(len(dict_txt[i])-1, -1, -1):
            if dict_txt[i][j]['SSID'] == "Iphone de Alexis" or dict_txt[i][j]['SSID'] == "LR-FHSS Mobile Plateform" or dict_txt[i][j]['SSID'] == "ESP32-Access-Point-Morgan":
                dict_txt[i].pop(j)
        print(round(((i+1)*100/len(dict_txt)),2),"%")
    print("[COMPLETE]")
    
    # Arrange IDs
    print("Id arrangements ...")
    for i in range(len(dict_txt)):
        for j in range(len(dict_txt[i])):
            dict_txt[i][j]['id'] = j
        print(round(((i+1)*100/len(dict_txt)),2),"%")
    print("[COMPLETE]")
    
    # Prompt to add new data to the database
    valid = str(input("Add new data into the database ? : (y/n) "))
    if valid.upper() == "Y" or valid.upper() == "YES":
        
        # Connect to SQLite database
        connection = sqlite3.connect("scans_DBSQL.db")
        cursor = connection.cursor()
        
        # Insert data into database table net_scan
        for scan_id in range(len(dict_txt)):
            for net_id in range(len(dict_txt[scan_id])):
                cursor.execute(
                    "INSERT INTO net_scan (scan_id , subnet_id , Latitude , Longitude , SSID , BSSID , RSSI, Channel , Encryption , Date_time ) VALUES (?,?,?,?,?,?,?,?,?,?);",
                    (scan_id, net_id, dict_txt[scan_id][net_id]["Lat"], dict_txt[scan_id][net_id]["Long"],
                     dict_txt[scan_id][net_id]["SSID"], dict_txt[scan_id][net_id]["BSSID"], dict_txt[scan_id][net_id]["RSSI"],
                     dict_txt[scan_id][net_id]["CH"], dict_txt[scan_id][net_id]["Enc"], date_string+" "+dict_txt[scan_id][net_id]["Time"],))
        
        connection.commit()
    
    # Option to use Alexis' GPS database
    valid = str(input("Use Alexis GPS database ? : (y/n) "))
    while valid.upper() == "Y" or valid.upper() == "YES":
        
        # Replace coordinates from Alexis' GPS database
        with open('Alexis_db.csv', mode ='r') as file:
            data = csv.reader(file, delimiter=",")
            list_data = list(data)
        
        print("Replacing coordinates from Alexis' database ...")
        
        connection = sqlite3.connect("scans_DBSQL.db")
        cursor = connection.cursor()
        
        for i in range(1, len(list_data)):
            for j in range(10, 0, -1):
                cursor.execute("UPDATE net_scan SET Latitude = ?, Longitude = ? WHERE Date_time = ?;",
                               (list_data[i][14], list_data[i][15], list_data[i][1][:17]+str(int(list_data[i][1][17:19])+j)))
                cursor.execute("UPDATE net_scan SET Latitude = ?, Longitude = ? WHERE Date_time = ?;",
                               (list_data[i][14], list_data[i][15], list_data[i][1][:17]+str(int(list_data[i][1][17:19])-j)))
        
        connection.commit()
        
        print("[COMPLETE]")
        
        valid = str(input("Use Alexis GPS database again ? : (y/n) "))
    
    # Option to use Phone's GPS database
    valid = str(input("Use Phone's GPS database ? : (y/n) "))
    while valid.upper() == "Y" or valid.upper() == "YES":
        
        # Replace coordinates from Phone's GPS database
        with open('GPS_Phone_db9.csv', mode ='r') as file:
            data = csv.reader(file, delimiter=",")
            list_data = list(data)
        
        print("Replacing coordinates from Phone's GPS database ...")
        
        connection = sqlite3.connect("scans_DBSQL.db")
        cursor = connection.cursor()
        
        for i in range(1, len(list_data)):
            for j in range(10, 0, -1):
                cursor.execute("UPDATE net_scan SET Latitude = ?, Longitude = ? WHERE Date_time = ?;",
                               (list_data[i][2], list_data[i][3], list_data[i][1][:10]+" "+str(int(list_data[i][1][10:13])-3)+list_data[i][1][13:17]+str(int(list_data[i][1][17:19])+j)))
                cursor.execute("UPDATE net_scan SET Latitude = ?, Longitude = ? WHERE Date_time = ?;",
                               (list_data[i][2], list_data[i][3], list_data[i][1][:10]+" "+str(int(list_data[i][1][10:13])-3)+list_data[i][1][13:17]+str(int(list_data[i][1][17:19])-j)))
        
        connection.commit()
        
        print("[COMPLETE]")
        
        valid = str(input("Use Phone's GPS database again ? : (y/n) "))
    
    # Remove unknown scan zones (locations with Latitude and Longitude as 0)
    print("Removing unknown scanzones ...")
    
    connection = sqlite3.connect("scans_DBSQL.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM net_scan WHERE Latitude = ? and Longitude = ?;", (0, 0))
    connection.commit()
    
    print("[COMPLETE]")
    
    # Update heatmap
    heatmap_create('SELECT * FROM net_scan WHERE SSID != "LR-FHSS Mobile Plateform" AND SSID != "Iphone de Alexis";', "mymapall.html")

# Inform the user that the program has finished
print("Program is finished")

    
    
    
    
    
    
    
    
    
    
    