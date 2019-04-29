import xmltodict

with open('template1.xml') as fd:
    doc = xmltodict.parse(fd.read())

list = []
print(doc)
print("\n\n")
print(doc['root'])
print("\n\n")
print(doc['root'][0]['microservice'])
print("\n\n")
print(doc['root'][0]['microservice']['image'])
print("\n\n")
print(doc['root'])

print(len(doc))
print("\n\n")
print(len(doc['root']))
print("\n\n")

# print("\n\n")
# print(doc['data'])

# print("\n\n")
# print(doc['data']['items'])

# print("\n\n")
# print(doc['data']['items']['item'])
# a = doc['data']['items']['item']

# print("\n\n")
# print(doc['data'])

# print("\n\n")
# print(doc['data'])

# print("\n\n\n")
# print(a[0]['#text'])
# for i in a:
#     print(i)




