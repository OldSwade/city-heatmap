# -*- coding: utf-8 -*-
"""
Author : Morgan Mootoosamy
Date : 06/12/2024 (MM/DD/YYYY)
Updated : 07/09/2024 (MM/DD/YYYY)
Title : heatmap creator
File : heatmap.py
"""

# Import necessary libraries

import folium
from folium.plugins import MiniMap, MousePosition
import sqlite3
import os
from tkinter import * 
from typing import List
import tkinter as tk
import webbrowser


# Create the main tkinter window

def Graph_user_int() -> None:
    """
    GUI (Graphical User Interface) that allows the user to choose filters to generate a WiFi heatmap.

    Returns
    -------
    None.

    """

    GUI = tk.Tk()
    GUI.title("HEATMAP CREATOR GUI")
    GUI.geometry('750x800+400+0')
    GUI.minsize(750,800)
    
    
    # Frames for organizing widgets
    SSID_frame = tk.Frame(GUI, borderwidth=5, relief="groove", padx=5, pady=5)
    Power_frame = tk.Frame(GUI, borderwidth=5, relief="groove", padx=5, pady=5)
    CH_frame = tk.Frame(GUI, borderwidth=5, relief="groove", padx=5, pady=5)
    Enc_frame = tk.Frame(GUI, borderwidth=5, relief="groove", padx=5, pady=5)
    frame_button = tk.Frame(GUI)
    
    # Checkbuttons variables
    var_ssid_rogers = tk.BooleanVar()
    var_ssid_ppcow = tk.BooleanVar()
    var_ssid_tplink = tk.BooleanVar()
    var_ssid_telus = tk.BooleanVar()
    var_ssid_bell = tk.BooleanVar()
    var_ssid_nsh = tk.BooleanVar()
    var_ssid_iwk = tk.BooleanVar()
    var_ssid_hot = tk.BooleanVar()
    var_ssid_dal = tk.BooleanVar()
    var_ssid_edu = tk.BooleanVar()
    var_ssid_tims = tk.BooleanVar()
    var_ssid_fop = tk.BooleanVar()
    
    var_rssi_30 = tk.BooleanVar()
    var_rssi_67 = tk.BooleanVar()
    var_rssi_70 = tk.BooleanVar()
    var_rssi_80 = tk.BooleanVar()
    var_rssi_90 = tk.BooleanVar()
    var_rssi_b90 = tk.BooleanVar()
    var_rssi_NO = tk.BooleanVar()
    
    var_ch_1 = tk.BooleanVar()
    var_ch_2 = tk.BooleanVar()
    var_ch_3 = tk.BooleanVar()
    var_ch_4 = tk.BooleanVar()
    var_ch_5 = tk.BooleanVar()
    var_ch_6 = tk.BooleanVar()
    var_ch_7 = tk.BooleanVar()
    var_ch_8 = tk.BooleanVar()
    var_ch_9 = tk.BooleanVar()
    var_ch_10 = tk.BooleanVar()
    var_ch_11 = tk.BooleanVar()
    var_ch_12 = tk.BooleanVar()
    var_ch_13 = tk.BooleanVar()
    var_ch_14 = tk.BooleanVar()
    
    var_enc_open = tk.BooleanVar()
    var_enc_wep = tk.BooleanVar()
    var_enc_wpa = tk.BooleanVar()
    var_enc_wpawpa2 = tk.BooleanVar()
    var_enc_wpa2 = tk.BooleanVar()
    var_enc_wpa2eap = tk.BooleanVar()
    var_enc_wpa2wpa3 = tk.BooleanVar()
    var_enc_wpa3 = tk.BooleanVar()
    
    # Checkbutton initialization
    list_chk_buttons_SSID = [
        tk.Checkbutton(SSID_frame, text="ROGERS", variable=var_ssid_rogers, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="Purple Cow", variable=var_ssid_ppcow, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="TP Link", variable=var_ssid_tplink, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="TELUS", variable=var_ssid_telus, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="BELL", variable=var_ssid_bell, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="NSH", variable=var_ssid_nsh, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="IWK", variable=var_ssid_iwk, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="Hotspot", variable=var_ssid_hot, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="Dalhousie", variable=var_ssid_dal, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="Eduroam", variable=var_ssid_edu, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="Tim Hortons", variable=var_ssid_tims, onvalue=True, offvalue=False),
        tk.Checkbutton(SSID_frame, text="FibreOP", variable=var_ssid_fop, onvalue=True, offvalue=False)
    ]
    
    list_chk_buttons_Power = [
        tk.Checkbutton(Power_frame, text="x >= -30 dBm", variable=var_rssi_30, onvalue=True, offvalue=False),
        tk.Checkbutton(Power_frame, text="-30 dBm > x >= -67 dBm", variable=var_rssi_67, onvalue=True, offvalue=False),
        tk.Checkbutton(Power_frame, text="-67 dBm > x >= -70 dBm", variable=var_rssi_70, onvalue=True, offvalue=False),
        tk.Checkbutton(Power_frame, text="-70 dBm > x >= -80 dBm", variable=var_rssi_80, onvalue=True, offvalue=False),
        tk.Checkbutton(Power_frame, text="-80 dBm > x >= -90 dBm", variable=var_rssi_90, onvalue=True, offvalue=False),
        tk.Checkbutton(Power_frame, text="x < -90 dBm", variable=var_rssi_b90, onvalue=True, offvalue=False),
        tk.Checkbutton(Power_frame, text="No Signal", variable=var_rssi_NO, onvalue=True, offvalue=False)
    ]
    
    list_chk_buttons_channel = [
        tk.Checkbutton(CH_frame, text="1", variable=var_ch_1, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="2", variable=var_ch_2, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="3", variable=var_ch_3, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="4", variable=var_ch_4, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="5", variable=var_ch_5, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="6", variable=var_ch_6, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="7", variable=var_ch_7, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="8", variable=var_ch_8, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="9", variable=var_ch_9, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="10", variable=var_ch_10, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="11", variable=var_ch_11, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="12", variable=var_ch_12, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="13", variable=var_ch_13, onvalue=True, offvalue=False),
        tk.Checkbutton(CH_frame, text="14", variable=var_ch_14, onvalue=True, offvalue=False)
    ]
    
    list_chk_buttons_Enc = [
        tk.Checkbutton(Enc_frame, text="open", variable=var_enc_open, onvalue=True, offvalue=False),
        tk.Checkbutton(Enc_frame, text="WEP", variable=var_enc_wep, onvalue=True, offvalue=False),
        tk.Checkbutton(Enc_frame, text="WPA", variable=var_enc_wpa, onvalue=True, offvalue=False),
        tk.Checkbutton(Enc_frame, text="WPA/WPA2", variable=var_enc_wpawpa2, onvalue=True, offvalue=False),
        tk.Checkbutton(Enc_frame, text="WPA2", variable=var_enc_wpa2, onvalue=True, offvalue=False),
        tk.Checkbutton(Enc_frame, text="WPA2-EAP", variable=var_enc_wpa2eap, onvalue=True, offvalue=False),
        tk.Checkbutton(Enc_frame, text="WPA2/WPA3", variable=var_enc_wpa2wpa3, onvalue=True, offvalue=False),
        tk.Checkbutton(Enc_frame, text="WPA3", variable=var_enc_wpa3, onvalue=True, offvalue=False)
    ]
    
    # Pack the Checkbuttons into their respective frames
    for chk_button_SSID in list_chk_buttons_SSID:
        chk_button_SSID.pack(anchor=tk.W)
    
    for chk_button_Power in list_chk_buttons_Power:
        chk_button_Power.pack(anchor=tk.W)
    
    for chk_button_channel in list_chk_buttons_channel:
        chk_button_channel.pack(anchor=tk.W)
    
    for chk_button_Enc in list_chk_buttons_Enc:
        chk_button_Enc.pack(anchor=tk.W)
    
    # Function to select or deselect all checkboxes in a list
    def select_all_checkboxes(checkbutton_list : List[Checkbutton]) -> None:
        """
        Function that selects checkboxes with a loop.

        Parameters
        ----------
        checkbutton_list : List[Checkbutton]
            List of checkbuttons.

        Returns
        -------
        None

        """

        for chk_button in checkbutton_list:
            chk_button.select()
            
                
    
    # Functions for selecting all checkboxes in each frame
    def select_all_SSID() -> None:
        """
        Function that selects all SSID checkboxes.

        Returns
        -------
        None

        """
        select_all_checkboxes(list_chk_buttons_SSID)
    
    def select_all_Power() -> None:
        """
        Function that selects all Power checkboxes.

        Returns
        -------
        None

        """
        select_all_checkboxes(list_chk_buttons_Power)
    
    def select_all_Channel() -> None:
        """
        Function that selects all Channel checkboxes.

        Returns
        -------
        None
        

        """
        select_all_checkboxes(list_chk_buttons_channel)
    
    def select_all_Enc() -> None:
        """
        Function that selects all Encryption checkboxes.

        Returns
        -------
        None

        """
        select_all_checkboxes(list_chk_buttons_Enc)
        
    def deselect_all() -> None:
        """
        Function that deselects all checkbuttons of the GUI.

        Returns
        -------
        None

        """
        for chk_button in list_chk_buttons_SSID:
            chk_button.deselect()
            
        for chk_button in list_chk_buttons_Power :
            chk_button.deselect()
        
        for chk_button in list_chk_buttons_channel :
            chk_button.deselect()
            
        for chk_button in list_chk_buttons_Enc:
            chk_button.deselect()
            
        
        
    def send_req() -> str:
        """
        Function that generates a SQL request depending of the selected checkboxes.

        Returns
        -------
        request_to_send : str
        
            A string that represents the request for the SQL database.

        """
        btn_select_all_SSID['state'] = DISABLED
        btn_select_all_Power['state'] = DISABLED
        btn_select_all_Enc['state'] = DISABLED
        btn_select_all_Channel['state'] = DISABLED    
        btn_enter['state'] = DISABLED
        
        list_req_bool = []    
        temp_list = []
        
        temp_list.append(var_ssid_rogers.get())
        temp_list.append(var_ssid_ppcow.get())
        temp_list.append(var_ssid_tplink.get())
        temp_list.append(var_ssid_telus.get())
        temp_list.append(var_ssid_bell.get())
        temp_list.append(var_ssid_nsh.get())
        temp_list.append(var_ssid_iwk.get())
        temp_list.append(var_ssid_hot.get())
        temp_list.append(var_ssid_dal.get())
        temp_list.append(var_ssid_edu.get())
        temp_list.append(var_ssid_tims.get())
        temp_list.append(var_ssid_fop.get())
        
        list_req_bool.append(temp_list)
        temp_list = []
    
        temp_list.append(var_rssi_30.get())
        temp_list.append(var_rssi_67.get())
        temp_list.append(var_rssi_70.get())
        temp_list.append(var_rssi_80.get())
        temp_list.append(var_rssi_90.get())
        temp_list.append(var_rssi_b90.get())
        temp_list.append(var_rssi_NO.get())
        
        list_req_bool.append(temp_list)
        temp_list = []
        
        temp_list.append(var_enc_open.get())
        temp_list.append(var_enc_wep.get())
        temp_list.append(var_enc_wpa.get())
        temp_list.append(var_enc_wpawpa2.get())
        temp_list.append(var_enc_wpa2.get())
        temp_list.append(var_enc_wpa2eap.get())
        temp_list.append(var_enc_wpa2wpa3.get())
        temp_list.append(var_enc_wpa3.get())
    
        list_req_bool.append(temp_list)
        temp_list = []
        
        temp_list.append(var_ch_1.get())
        temp_list.append(var_ch_2.get())
        temp_list.append(var_ch_3.get())
        temp_list.append(var_ch_4.get())
        temp_list.append(var_ch_5.get())
        temp_list.append(var_ch_6.get())
        temp_list.append(var_ch_7.get())
        temp_list.append(var_ch_8.get())
        temp_list.append(var_ch_9.get())
        temp_list.append(var_ch_10.get())
        temp_list.append(var_ch_11.get())
        temp_list.append(var_ch_12.get())
        temp_list.append(var_ch_13.get())
        temp_list.append(var_ch_14.get())
    
        list_req_bool.append(temp_list)
        
        btn_select_all_SSID['state'] = NORMAL
        btn_select_all_Power['state'] = NORMAL
        btn_select_all_Enc['state'] = NORMAL
        btn_select_all_Channel['state'] = NORMAL  
        btn_enter['state'] = NORMAL
        
        
        req_msg = ''
        
        
        req_list = [
                    [
                        "lower(SSID) like lower('ROGERS%')",
                        "lower(SSID) like lower('purple cow%') OR lower(SSID) like lower('purplecow%')",
                        "lower(SSID) like lower('tplink%') OR lower(SSID) like lower('tp link%')",
                        "lower(SSID) like lower('telus%')",
                        "lower(SSID) like lower('bell%')",
                        "lower(SSID) like lower('nsh%')",
                        "lower(SSID) like lower('iwk%')",
                        "lower(SSID) like lower('hotspot%')",
                        "lower(SSID) like lower('dal-%')",
                        "lower(SSID) like lower('eduroam')",
                        "lower(SSID) like lower('Tim Hortons%')",
                        "lower(SSID) like lower('Fibreop%')"
                    ],
                    [
                        "RSSI >= -30",
                        "RSSI < -30 AND RSSI >= -67",  
                        "RSSI < -67 AND RSSI >= -70",
                        "RSSI < -70 AND RSSI >= -80",
                        "RSSI < -80 AND RSSI >= -90",
                        "RSSI < -90 AND RSSI != -999",
                        "RSSI = -999"
                    ],
                    [
                        "Encryption = 'open'",
                        "Encryption = 'WEP'",
                        "Encryption = 'WPA'",
                        "Encryption = 'WPA/WPA2'",
                        "Encryption = 'WPA2'",
                        "Encryption = 'WPA2-EAP'",
                        "Encryption = 'WPA2/WPA3'",
                        "Encryption = 'WPA3'"
                    ],
                    [
                        "Channel = 1",    
                        "Channel = 2",   
                        "Channel = 3",   
                        "Channel = 4",       
                        "Channel = 5",   
                        "Channel = 6",   
                        "Channel = 7",   
                        "Channel = 8",   
                        "Channel = 9",   
                        "Channel = 10",   
                        "Channel = 11",   
                        "Channel = 12",   
                        "Channel = 13",   
                        "Channel = 14"
                    ]
                   ]
        
        
        request_to_send = ''
        req_msg = ''
        
        if list_req_bool[1][-1] and list_req_bool[1][-2] :
            req_list[1][-2] = "RSSI < -90"
        
        for icol in range(len(list_req_bool)):
            for i_bool in range(len(list_req_bool[icol])):
                if list_req_bool[icol][i_bool]:
                    
                    
                    req_msg = ' ' +req_list[icol][i_bool] + ' OR'
                
                    
                    
                    if req_msg[-2:] == 'OR' and i_bool+1 == (len(list_req_bool[icol])):
                        req_msg = req_msg[:-3]
                        

                        
                    request_to_send = request_to_send + req_msg
                    req_msg = ''
                    
            if request_to_send[-2:] == 'OR' :        
                request_to_send = request_to_send[:-3] + ' AND'  
    
                   
                
            elif request_to_send != '':
                if request_to_send[-3:] != 'AND':
                    request_to_send = request_to_send + ' AND'
                
            
           
                    
                    
                
        if request_to_send[-3:] == 'AND' and request_to_send != '':    
            request_to_send = request_to_send[:-4]
            request_to_send = 'SELECT * FROM net_scan WHERE' + request_to_send + ' AND SSID != "LR-FHSS Mobile Plateform" AND SSID != "Iphone de Alexis";' 
            
        elif request_to_send[-2:] == 'OR' and request_to_send != '':
            request_to_send = request_to_send[:-3]
            request_to_send = 'SELECT * FROM net_scan WHERE' + request_to_send + ' AND SSID != "LR-FHSS Mobile Plateform" AND SSID != "Iphone de Alexis";' 
        
    
        
        return request_to_send
    
        
        
        
    # Button to select all checkboxes in each frame
    btn_select_all_SSID = tk.Button(frame_button, text="Select All SSID", command=select_all_SSID)
    btn_select_all_Power = tk.Button(frame_button, text="Select All RSSI", command=select_all_Power)
    btn_select_all_Channel = tk.Button(frame_button, text="Select All Channels", command=select_all_Channel)
    btn_select_all_Enc = tk.Button(frame_button, text="Select All Encryptions", command=select_all_Enc)
    btn_deselect_all = tk.Button(frame_button, text="Clear all",background="grey", command=deselect_all)
    btn_enter = tk.Button(frame_button, text="Create map",background="red",command= lambda : heatmap_create(send_req(),"mymap.html"))
    btn_gen_all = tk.Button(frame_button, text="Open map with all points", background="lightblue",command= open_map_all)
    
    btn_select_all_SSID.pack(side=tk.LEFT, padx=5, pady=5)
    btn_select_all_Power.pack(side=tk.LEFT, padx=5, pady=5)
    btn_select_all_Channel.pack(side=tk.LEFT, padx=5, pady=5)
    btn_select_all_Enc.pack(side=tk.LEFT, padx=5, pady=5)
    btn_deselect_all.pack(side=tk.LEFT, padx=5, pady=5)
    btn_enter.pack(side=tk.LEFT, padx=5, pady=5)
    btn_gen_all.pack(side=tk.LEFT, padx=5, pady=5) 
    
    # Grid frames in root window
    frame_button.grid(column=0, row=0, columnspan=2, pady=10)  # Assuming this is where you want to place your buttons
    SSID_frame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")  # Adjust column and row according to your design
    Power_frame.grid(column=1, row=1, padx=10, pady=10, sticky="nsew")  # Adjust column and row according to your design
    CH_frame.grid(column=0, row=2, padx=10, pady=10, sticky="nsew")  # Adjust column and row according to your design
    Enc_frame.grid(column=1, row=2, padx=10, pady=10, sticky="nsew")  # Adjust column and row according to your design
    
    # Configure grid weights to make frames stick together
    GUI.grid_rowconfigure(1, weight=1)
    GUI.grid_columnconfigure(0, weight=1)
    GUI.grid_columnconfigure(1, weight=1)
    
    
    # Start the GUI main loop
    GUI.mainloop()




def heatmap_create(request : str = None,filename : str = "mymap.html") -> None:
    """
    

    Parameters
    ----------
    request : str, optional
        DESCRIPTION. The default is None.
    filename : str, optional
        DESCRIPTION. The default is "mymap.html".

    Returns
    -------
    None

    """
    # Create a map centered on a specific location
    m = folium.Map([44.637, -63.585], zoom_start=12)

    if os.path.isfile("scans_DBSQL.db") and os.path.getsize("scans_DBSQL.db") > 0:
        print("Creating map ...")

        # Add plugins and legend
        folium.plugins.Fullscreen(position="topright", title="Expand me", title_cancel="Exit me",
                                  force_separate_button=True).add_to(m)
        MiniMap(toggle_display=True).add_to(m)
        MousePosition().add_to(m)

        # Legend HTML
        legend_html = '''
         <div style="position: fixed; 
         bottom: 50px; left: 50px; width: 200px; height: auto; 
         border:2px solid grey; z-index:9999; font-size:14px;background-color:white;
         ">
         &nbsp; <b>Legend</b> <br>
         &nbsp; Signal Strength <br>
         &nbsp; >= -30 dBm &nbsp; <i class="fa fa-circle" style="color:pink"></i><br>
         &nbsp; -30 to -67 dBm &nbsp; <i class="fa fa-circle" style="color:red"></i><br>
         &nbsp; -67 to -70 dBm &nbsp; <i class="fa fa-circle" style="color:orange"></i><br>
         &nbsp; -70 to -80 dBm &nbsp; <i class="fa fa-circle" style="color:yellow"></i><br>
         &nbsp; -80 to -90 dBm &nbsp; <i class="fa fa-circle" style="color:green"></i><br>
         &nbsp; <= -90 dBm &nbsp; <i class="fa fa-circle" style="color:blue"></i><br>
         &nbsp; No Signal &nbsp; <i class="fa fa-circle" style="color:black"></i><br>
         </div>
         '''
        m.get_root().html.add_child(folium.Element(legend_html))

        # Connect to SQLite database
        connection = sqlite3.connect("scans_DBSQL.db")
        cursor = connection.cursor()

        # Fetch data from the database
        #print(request) # To see request
        dict_txt = cursor.execute(request).fetchall()

        # Close database connection
        connection.close()

        # Organize data into list_scans
        list_scan = []
        list_scans = []
        for i_scan in range(len(dict_txt)):
            if dict_txt[i_scan][0] != dict_txt[i_scan-1][0]:
                list_scans.append(list_scan)
                list_scan = []

            list_scan.append(dict_txt[i_scan])
        list_scans.append(list_scan)
        list_scans.pop(0)

        print("Adding markers ...")

        # Add markers for each scan
        for i_scan in range(len(list_scans)):
            # Determine signal strength
            if list_scans[i_scan][0][6] >= -30:
                color = "pink"
            elif list_scans[i_scan][0][6] >= -67:
                color = "red"
            elif list_scans[i_scan][0][6] >= -70:
                color = "orange"
            elif list_scans[i_scan][0][6] >= -80:
                color = "yellow"
            elif list_scans[i_scan][0][6] >= -90:
                color = "green"
            elif list_scans[i_scan][0][6] < -90 and list_scans[i_scan][0][6] != -999:
                color = "blue"
            else:
                color = "black"

            # Create CircleMarker
            marker = folium.CircleMarker(
                location=[list_scans[i_scan][0][2], list_scans[i_scan][0][3]],
                radius=(0.2 * len(list_scans[i_scan])),
                fill_opacity=0.6,
                fill=True,
                color=color,
            )

            # Create HTML table for popup
            popup_html = '''
            <table style="width:100%">
              <tr>
                <th>SSID</th>
                <th>Encryption</th>
                <th>RSSI</th>
                <th>CH</th>
              </tr>
            '''
            for scan in list_scans[i_scan]:
                popup_html += '''
                <tr>
                  <td>{}</td>
                  <td>{}</td>
                  <td>{}</td>
                  <td>{}</td>
                </tr>
                '''.format(scan[4], scan[8], scan[6], scan[7])

            popup_html += '</table>'

            # Add popup to marker
            marker.add_child(folium.Popup(popup_html))

            # Add marker to map
            marker.add_to(m)

        print("[COMPLETE]")

        # Save map
        print("Saving map as "+filename)
        m.save(filename)
        print("[COMPLETE]")

        # Open map in browser
        webbrowser.open(filename)
        print("Map is open in your browser.")

    else:
        print("Error: Database file not found or empty.")



def open_map_all() -> None:
    """
    Function that opens the map from "mymapall.html" containing all the points from the database.

    Returns
    -------
    None

    """
    # Open map in browser
    webbrowser.open('mymapall.html')
    print("Map is open in your browser.")
    

# Call the function to create the custom heatmap with options (GUI)
#Graph_user_int()

