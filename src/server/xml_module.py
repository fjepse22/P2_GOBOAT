import time 
class Xml():
    def __init__(self):
        pass
    def generate_time(self):
        boattime= time.ctime(time.time())
        return boattime[11:-5]
    
    def generate_xml(self, ID=1, PositionLat=33, PositionLon=-144, Draw=9):
        time=self.generate_time()
        xml=f"""<?xml version="1.0"?>

<!-- 	
		XML for Status data
		Version 1.0 | Encoding: UTF-8
		Created by: Maiken Hammer
		Date: 13/03-2024
		Modified by: -None-
		Date: -None-
-->

<status_data xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:noNamespaceSchemaLocation="sch_status_data.xsd">
	<boatData>
		<ID>{ID}</ID>
		<PositionLat>{PositionLat}</PositionLat>
		<PositionLon>{PositionLon}</PositionLon>
		<Time>{time}</Time>
	</boatData>
	<battData>
		<Battery1>
			<Voltage>12</Voltage>
			<Temperature>14</Temperature>
		</Battery1>
		<Battery2>
			<Voltage>12</Voltage>
			<Temperature>21</Temperature>
		</Battery2>
		<Battery3>
			<Voltage>12</Voltage>
			<Temperature>21</Temperature>
		</Battery3>
		<Battery4>
			<Voltage>12</Voltage>
			<Temperature>21</Temperature>
		</Battery4>
		<Battery5>
			<Voltage>12</Voltage>
			<Temperature>21</Temperature>
		</Battery5>
		<Battery6>
			<Voltage>12</Voltage>
			<Temperature>21</Temperature>
		</Battery6>
		<Battery7>
			<Voltage>12</Voltage>
			<Temperature>21</Temperature>
		</Battery7>
		<Battery8>
			<Voltage>12</Voltage>
			<Temperature>21</Temperature>
		</Battery8>
		<Draw>{Draw}</Draw>
	</battData>

</status_data>
"""
        return xml
if __name__ == "__main__":
    xml=Xml()
    print(xml.generate_xml())