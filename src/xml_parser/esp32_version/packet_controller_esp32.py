#Version 1.00 | Encoding UTF-8
#Created 22-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 13-05-2024

from lxml import etree
class PacketController():
    """
    The class PacketController is used to validate the XML file against the XSD file\n
    """
    def __init__(self):
        pass

    def validate(self, xsd_path: str, xml_input: str) -> bool:
        xmlschema_doc = etree.parse(xsd_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        
        xml_doc= etree.fromstring(xml_input)
        result = xmlschema.validate(xml_doc)

        return result
