#Version 0.2 | Encoding UTF-8
#Created 22-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 23-04-2024

from lxml import etree
        
def validate(xsd_path: str, xml_path: str) -> bool:
    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    try:
            xml_doc = etree.parse(xml_path)
    except:
        # if xml-path is not a file, it will read the xml-file as a string instead
        xml_doc= etree.fromstring(xml_path)
    result = xmlschema.validate(xml_doc)

    return result
