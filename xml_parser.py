import xmltodict, json

def parseXML(code):
    data = xmltodict.parse(xml_input=code)
    return json.dumps(data)

def parseJSON(code):
    data = json.loads(code)
    return xmltodict.unparse(data)

def parseFile(file):
    extentsion = file.rsplit('.',1)[1].lower()
    print(extentsion)
    if extentsion == 'xml':
        with open(file, 'rb') as xmlfile:
            data = xmltodict.parse(xmlfile)
            with open('upload/converted.json', 'w') as jsonfile:
                jsonfile.write(json.dumps(data))
        return 'converted.json'
    elif extentsion == 'json':
        with open(file, 'r', encoding='utf-8') as jsonfile:
            data = json.loads(jsonfile.read())
            with open('upload/converted.xml', 'w') as xmlfile:
                xmlfile.write(xmltodict.unparse(data))
        return 'converted.xml'
