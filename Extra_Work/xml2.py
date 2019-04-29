
    
import ast
import copy
from pprint import pprint
keys1 = ["image","min","max","time","numberofrequests","port","network","prefixurl","environment","name"]
import xml.etree.ElementTree as ET
tree = ET.parse('template1.xml')
root = tree.getroot()
print(root)
print(root.tag)
print(len(root))

dict1 = dict((l,0) for l in keys1)

print(dict1)
global xml_d
global image_d
global network_d

xml_d=[]

l1 = [0]*len(root)

for i in range(len(root)):
    xml_d.append(copy.deepcopy(dict1))
# xml_d = dict1*len(root)
print(xml_d)
for i,child in enumerate(root):
    print(child.tag, child.attrib)
    # print("\n")
    print("I is ",i)
    for child1 in child:
        if(child1.tag in ["environment","port"]):
            # print(str(child1.text))
            xml_d[i][child1.tag]=ast.literal_eval(str(child1.text))
        elif (child1.tag in ["curr_container","max","min","numberOfHTTPRequests","numberOfRunningContainers","numberofrequests","time"]):
            xml_d[i][child1.tag] = int(child1.text)
        else:
            xml_d[i][child1.tag]=(str(child1.text))
        print(child1.tag, child1.text)
    print("\n")

print(xml_d)

print("\n\n")
for i in xml_d:
    print(i)


print("XML is \n\n")
print(xml_d)
for i in xml_d:
    i['numberOfHTTPRequests'] = 0
    i['curr_container'] = -1
    i['numberOfRunningContainers'] = copy.deepcopy(i['min'])



l2 = []
image_d = dict()
for i in xml_d:
    image_d[i['image']] = copy.deepcopy(i)
    # l2.append(temp_d)

network_d = dict()
for i in xml_d:
    network_d[i['prefixurl']] = copy.deepcopy(i)

print("\n\n") 
pprint(image_d)
print("\n\n")

pprint(network_d)
print("XML is \n\n")
pprint(list(xml_d[0]['port'].values())[0])
pprint(xml_d)

