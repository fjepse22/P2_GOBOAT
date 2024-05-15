# See https://mariadb-corporation.github.io/mariadb-connector-python/usage.html for documentation about the mariadb module.

# Writen by Magnus F. Kavin
# Created 23-04-2024
# last modified: 15-05-2024
# last modified by: Magnus Kavin

"""
This is a GUI module. it connects to a database, imports relevant data from a database 
by wirelessly connecting to a server and displays it in a graphical interface.

This module takes no direct inputs from the user, and instead gets all necessary inputs from the database.
"""



import mariadb
import sys
import datetime #not actively used, but utilized for testing
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock




# class forms connection to database
class DatabaseConnection:
    """
    DatabaseConnection(user,password,host,port=3306,database=goboatv2)

    This class is used to connect to the Goboat database in order to insert battery logs into the Goboat database.
    The class have the following methods
    - insert_boat_data(self,boat_ID,Date,Lok_lat,Lok_long,Battery_temperature,Watt_hour,Voltage_array)
    """

    def __init__(self,user,password,host,port=3306,database='goboatv2'):

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        
        

    def get_boats(self):
        """
        No inputs
        Queries the database and returns a list of all boats
        """
        try:
            connection = mariadb.connect(user = self.user, password = self.password,host = self.host,port = self.port, database = self.database)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        # Get Cursor
        cursor = connection.cursor()

        # Fetch the battery_ID's
        cursor.execute(
            f"""SELECT Boat_ID FROM goboatv2.boats""", 
        )


        # getting results from cursor, storing them in a list.
        results= cursor.fetchall() 
        boat_list=[i[0] for i in results]

        # free resources
        cursor.close()
        connection.close()

        return boat_list


    def get_details(self,boat_list):
        
        """
        Queries the Lok_lat, Lok_long and Watt_hour values for each boat.
        Returns a dictionary 

        output example:
        {
        'boat1': 
            {
            'Latitude': 33.0, 
            'Longitude': -144.0, 
            'Watt': 2.3, 
            'Last updated': datetime.datetime(2024, 5, 6, 14, 2, 46), 
            'Batteries':   {
                            'bat11': {'Voltage': 12.0, 'Temperature': 21.0}, 
                            'bat12': {'Voltage': 12.0, 'Temperature': 21.0}, 
                            'bat13': {'Voltage': 12.0, 'Temperature': 21.0}, 
                            'bat14': {'Voltage': 12.0, 'Temperature': 21.0}, 
                            'bat15': {'Voltage': 12.0, 'Temperature': 21.0}, 
                            'bat16': {'Voltage': 12.0, 'Temperature': 21.0}, 
                            'bat17': {'Voltage': 12.0, 'Temperature': 21.0}, 
                            'bat18': {'Voltage': 12.0, 'Temperature': 21.0}
                            }
            }
        }
        """

        details_boats = {}
        
        
        try:
            connection = mariadb.connect(user = self.user, password = self.password,host = self.host,port = self.port, database = self.database)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
       

        for boat_ID in boat_list:
            # Get Cursor
            cursor = connection.cursor()

        
            #cursor selects most recent row from the data_boat table for the desired boat.
            cursor.execute(
                f"""SELECT lok_lat, lok_long, watt, data_time FROM goboatv2.boat_log 
                WHERE boat_ID = '{boat_ID}' ORDER BY Data_time DESC LIMIT 1""", 
            )



            # getting results from cursor and storing them in dictionary
            boat_data = cursor.fetchall() 

            for row in boat_data:
                lok_lat, lok_long, watt, data_time = row
                details_boats[boat_ID]= {'Latitude': lok_lat, 'Longitude': lok_long, 'Watt': watt, 'Last updated': data_time, 'Batteries':{}}
            
           
            # gets battery data for the relevant boat at the relevant time to add to the dictionary. This info is not displayed in current version of the GUI.
            cursor.execute(
                f"""SELECT bat_ID, voltage, temperature FROM goboatv2.boat_log 
                INNER JOIN battery_log ON goboatv2.boat_log.data_ID=goboatv2.battery_log.data_ID
                WHERE data_time = '{data_time}' AND boat_ID = '{boat_ID}'""", 
            )

            battery_data = cursor.fetchall() 
            for row in battery_data:
                bat_ID, voltage, temperature = row
                
                details_boats[boat_ID]['Batteries'][bat_ID]= {'Voltage': voltage, 'Temperature': temperature}

            
               
        
        # Close connection to free the server.
        cursor.close()
        connection.close()

        return details_boats
        




#GUI app class is defined
class BoatGUI(App):
    """
    BoatGUI(boat_list, boat_list, dict_boats)

    The BoatGUI class contains the main window for the user interface. The methods included are dedicated to building and formatting the gui window. 
    """
    def __init__(self, boat_list, dict_boats, **kwargs):
        super().__init__(**kwargs)
        self.boat_list = boat_list
        self.dict_boats = dict_boats


    def build(self):
        """
        Builds the gui. 
        Uses the boat list to create a button for each individual boat, displaying that boats data. 
        """
        layout = BoxLayout(orientation='vertical')
        

        for boat in self.boat_list:
            
            #get colour
            colour= self.set_colour(boat)     

            # create button
            button = BoatButton(self.dict_boats,boat,colour,
                                 size_hint_y=None, height=100)
            layout.add_widget(button)

        return layout
    

    def set_colour(self, boat):
        #set button color according to data. values are placeholders
        try:
            avrg_temp_and_volt= self.get_average_temp_and_volt(boat) #[0]=avrg_temp, [1]=avrg_volt
            
            
            #makes button red in certain error states. Current error state is if watt is less than two. More error states can be added
            if avrg_temp_and_volt[0]>80 or self.dict_boats[boat]['Watt']<2:
                colour = (1, 0, 0, 1)  # Red


            elif  avrg_temp_and_volt[1]<6: #temp greater than 80 or if voltage is less than six
                colour = (1, 1, 0, 1)  # Yellow                
            
            
            #no issues: button is greeen
            else:
                colour = (0, 1, 0, 1)  # Green

        except:
            #error in getting boat data
            colour = (0, 1, 3, 0.5)  # blue
            pass 

        return colour


    def get_average_temp_and_volt(self,boat):
        """
        calculates the average temperature and voltage across the boats batteries.
        """
        total_voltage = 0.0
        total_temperature= 0.0
        num_batteries = 0

        
        for battery_info in self.dict_boats[boat]['Batteries'].values():
            total_voltage += battery_info['Voltage']
            total_temperature += battery_info['Temperature']
            num_batteries += 1
            
            if num_batteries == 0:
                print('No batteries')  # Avoid division by zero
                
            avrg_temp = total_temperature / num_batteries
            avrg_volt = total_voltage / num_batteries
        
        return [avrg_temp, avrg_volt]
    




class BoatButton(Button):
    """
    BoatButton(dict_boats,boat, colour)
    Defines the buttons in the gui. Takes a dictionary, a boat ID and colour values as inputs.
    """

    def __init__(self, dict_boats, boat, colour, **kwargs):
        super().__init__(**kwargs)
        self.dict_boats = dict_boats
        self.background_color=colour
        self.text = f"{boat}"
        self.bind(on_press=lambda instance: self.show_details(boat)) #binds the show_details() function to the button.


    def show_details(self,boat):
        """
        Takes  
        Creates a popup when a button is clicked.
        Popup contains info on the selected boat.
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=5)
        try:
            for key, value in self.dict_boats[boat].items():
                if key != 'Batteries':
                    label_text = f"{key.capitalize()}: {value}"
                    label = Label(text=label_text)
                    content.add_widget(label)

            for key, value in self.dict_boats[boat]['Batteries'].items():
                label_text = f"{key.capitalize()}: {value}"
                label = Label(text=label_text)
                content.add_widget(label)

            
            popup = Popup(title='Boat Details',
                        content=content,
                        size_hint=(None, None), size=(1000, 800))
            popup.open()
        
            
        except:
            label_text = "no boat data found"
            label = Label(text=label_text)
            content.add_widget(label)
    
            popup = Popup(title='error',
                        content=content,
                        size_hint=(None, None), size=(400, 300))
            popup.open()



def update_gui(dt):
    global ui
    boat_list = Goboat.get_boats()
    boat_dict = Goboat.get_details(boat_list)
    ui.root.clear_widgets()
    ui.root.add_widget(BoatGUI(boat_list, boat_dict).build())





if __name__ == '__main__':
    # Testserver on own computer.change user and password input to connect to server.
    # Goboat = DatabaseConnection(user="root",password="zxcv1234",host="127.0.0.1")

    Goboat = DatabaseConnection(user="gui_user",password="password",host="192.168.1.10",database="goboatv2")

    boat_list = Goboat.get_boats()
    boat_dict = Goboat.get_details(boat_list)

    ui=BoatGUI(boat_list, boat_dict)
    Clock.schedule_interval(update_gui, 60) #Schedules the UI to update every 60 seconds. 
    ui.run()    





