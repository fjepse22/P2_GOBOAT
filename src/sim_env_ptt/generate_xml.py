import xml.etree.ElementTree as ET
class GenerateXML:
    """
    This class is used to generate XML strings from dictionaries.\n
    """
    def __init__(self):
        """
        Constructor for GenerateXML class.\n
        """
        pass
    
    def generateXML(self, unit_dict, voltage_dict, temp_dict):
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