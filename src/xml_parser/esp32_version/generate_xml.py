#Version 1.00 | Encoding UTF-8
#Created 09-05-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Ib Leminen Mohr Nielsen
#Last modified 10-05-2024
import xml.etree.ElementTree as ET
import json
import pickle
from logger import log

class CreateXML():
    """
    The class CreateXML is used to generate an XML file from a dictionaries.\n

    List of class methods:\n
    - __init__(self, unit_dict, voltage_dict, temp_dict): Initialises the object\n

    - generateXML(self): Used to generate a XML string from the dictionaries unit_dict, voltage_dict, temp_dict\n
    """
    def __init__(self):
        pass
    
    def bytes_to_xml(self, data : bytes):
        """
        Converts the data from the XML file to a dictionary\n
        \n
        ------------
        PARAMETERS\n
        data: The data from the XML file\n
        ------------
        RETURNS\n
        \n
        Returns "data_dict"\n
        Return type is dictionary\n
        """  
        if type(data) != bytes:
            log.error(f"""The data is not in bytes""")
            return
        
        try:
            data_list=data.split(b'#')
            unit_dict=json.loads(data_list[0].decode('utf-8'))
            voltage_dict=json.loads(data_list[1].decode('utf-8'))
            temp_dict=json.loads(data_list[2].decode('utf-8'))
            
        
        except (Exception) as e:
                log.error(f"""File: generate_xml.py: {e}""")
                return
        
        log.debug(f"Data converted into original input")
        
        try:
            xml=self.generateXML(unit_dict, voltage_dict, temp_dict)
        except (Exception) as e:
            log.error(f"""File: generate_xml.py: {e}""")
            return
        
        return xml
    
    def generateXML(self, unit_dict : dict, voltage_dict : dict, temp_dict : dict):
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
        boat_data_ID.text = str(unit_dict["id"])
        
        boat_data_PositionLat = ET.SubElement(boat_data, "PositionLat")
        boat_data_PositionLat.text = str(unit_dict["pos_lat"]/100000)

        boat_data_PositionLon = ET.SubElement(boat_data, "PositionLon")
        boat_data_PositionLon.text = str(unit_dict["pos_lon"]/100000)

        boat_data_Time = ET.SubElement(boat_data, "Time")
        boat_data_Time.text = str(unit_dict["time"])

        # create batt_data elements
        batt_data = ET.Element("battData")
        for i in range(0,len(voltage_dict)):
            batt_data_Battery = ET.SubElement(batt_data, "Battery"+str(i+1))
            
            # Create Voltage elements
            batt_data_Voltage = ET.SubElement(batt_data_Battery, "Voltage")
            batt_data_Voltage.text = str(voltage_dict["batt_"+str(i+1)])

            # Create Temperature elements
            batt_data_Temperature = ET.SubElement(batt_data_Battery, "Temperature")
            batt_data_Temperature.text = str(temp_dict["batt_"+str(i+1)])

        root.append(batt_data)
        
        batt_data_Draw = ET.SubElement(batt_data, "Draw")
        batt_data_Draw.text = str(unit_dict["p_draw"])
        
        tree=ET.ElementTree(root)
        xml=ET.tostring(tree.getroot(), encoding='unicode')
        return xml         

if __name__ == "__main__":
    unit_dict = {"id" : 1, "pos_lat" : 3300000, "pos_lon" : -10400000, "time" : "14:12:10", "p_draw" : 0}
    voltage_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
    temp_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}

    byte_unit_dict=json.dumps(unit_dict).encode('utf-8')+b'#'
    byte_voltage_dict=json.dumps(voltage_dict).encode('utf-8')+b'#'
    byte_temp_dict=json.dumps(temp_dict).encode('utf-8')+b'#'
    data = byte_unit_dict+byte_voltage_dict+byte_temp_dict

    # converts the dictionaries to bytes and encodes it to utf-8, and adds a '#' to the end of the string, but using pickle instead of json.
    bud1=pickle.dumps(unit_dict)+b'#'
    bvd1=pickle.dumps(voltage_dict)+b'#'
    btd1=pickle.dumps(temp_dict)+b'#'
    invalid_byte_dic1 = bud1+bvd1+btd1

    # converts the dictionaries to bytes and encodes it to utf-8, and adds a '#' to the end of the string.
    bud2=bytes(str(unit_dict), "utf-8")+b'#'
    bvd2=bytes(str(voltage_dict), "utf-8")+b'#'
    btd2=bytes(str(temp_dict), "utf-8")+b'#'
    invalid_byte_dic2 = bud2+bvd2+btd2

    # converts the dictionaries to bytes and encodes it to utf-8, but doesn't add a '#' to the end of the string.
    bud3=json.dumps(unit_dict).encode('utf-8')
    bvd3=json.dumps(voltage_dict).encode('utf-8')
    btd3=json.dumps(temp_dict).encode('utf-8')
    invalid_byte_dic3 = bud3+bvd3+btd3

    # Test other kinds of data
    
    """input_list=["hello", 1, ["hello", "hello", "hello"], None, True, {"t":1}]
    for i in range(0,len(input_list)):
        invalid_data=(json.dumps(input_list[i]).encode('utf-8')+b'#')*3
        create_xml=CreateXML()
        print(create_xml.bytes_to_xml(invalid_data))"""
    



    create_xml=CreateXML()
    print(create_xml.bytes_to_xml(data))