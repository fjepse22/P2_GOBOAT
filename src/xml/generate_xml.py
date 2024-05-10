import xml.etree.ElementTree as ET
#Version 1.00 | Encoding UTF-8
#Created 09-05-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Ib Leminen Mohr Nielsen
#Last modified 10-05-2024

class CreateXML():
    """
    The class CreateXML is used to generate an XML file from a dictionaries.\n

    List of class methods:\n
    - __init__(self, unit_dict, voltage_dict, temp_dict): Initialises the object\n

    - generateXML(self): Used to generate a XML string from the dictionaries unit_dict, voltage_dict, temp_dict\n
    """
    def __init__(self, unit_dict, voltage_dict, temp_dict):
        self.unit_dict = unit_dict
        self.voltage_dict = voltage_dict
        self.temp_dict = temp_dict

    def generateXML(self):
        """
        This method generates a XML string from dictionaries.\n
        \n
        ------------
        PARAMETERS\n

        self:\n
        ------------
        RETURNS\n
        \n
        Returns "xml"\n
        Return type str\n
        """
        root = ET.Element("status_data")

        # Create boat_data elements
        boat_data = ET.Element("boatData")
        root.append(boat_data)

        boat_data_ID = ET.SubElement(boat_data, "ID")
        boat_data_ID.text = str(self.unit_dict["id"])
        
        boat_data_PositionLat = ET.SubElement(boat_data, "PositionLat")
        boat_data_PositionLat.text = str(self.unit_dict["pos_lat"]/100000)

        boat_data_PositionLon = ET.SubElement(boat_data, "PositionLon")
        boat_data_PositionLon.text = str(self.unit_dict["pos_lon"]/100000)

        boat_data_Time = ET.SubElement(boat_data, "Time")
        boat_data_Time.text = str(self.unit_dict["time"])

        # create batt_data elements
        batt_data = ET.Element("battData")
        for i in range(0,len(self.voltage_dict)):
            batt_data_Battery = ET.SubElement(batt_data, "Battery"+str(i+1))
            
            # Create Voltage elements
            batt_data_Voltage = ET.SubElement(batt_data_Battery, "Voltage")
            batt_data_Voltage.text = str(self.voltage_dict["batt_"+str(i+1)])

            # Create Temperature elements
            batt_data_Temperature = ET.SubElement(batt_data_Battery, "Temperature")
            batt_data_Temperature.text = str(self.temp_dict["batt_"+str(i+1)])

        root.append(batt_data)
        
        batt_data_Draw = ET.SubElement(batt_data, "Draw")
        batt_data_Draw.text = str(self.unit_dict["p_draw"])
        
        tree=ET.ElementTree(root)
        xml=ET.tostring(tree.getroot(), encoding='unicode')
        return xml

if __name__ == "__main__":
    unit_dict = {"id" : 1, "pos_lat" : 3300000, "pos_lon" : -10400000, "time" : "14:12:10", "p_draw" : 0}
    voltage_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
    temp_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}

    create_xml=CreateXML(unit_dict, voltage_dict, temp_dict)
    print(create_xml.generateXML())