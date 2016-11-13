"""
Deletes elements with "action"="delete" from an OpenStreetMap file
"""

import xml.etree.cElementTree as etree

doc = etree.parse("filename.osm")
osm = doc.getroot()

elementsToRemove = []

for e in osm:
    if "action" in e.attrib:
        if e.attrib["action"] == "delete":
            elementsToRemove.append(e)
        del e.attrib["action"]

for e in elementsToRemove:
    osm.remove(e)

doc.write("filename_fixed.osm", encoding="utf8")
