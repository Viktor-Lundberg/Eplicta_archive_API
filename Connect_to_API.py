import ssl
import urllib.request, urllib.parse, urllib.error, urllib
import xml.etree.ElementTree as ET
import json

# Laddar ner enstaka blob
def download_blob(url, blobname, sas):
    call = f'{url}/{blobname}{sas}'
    print(f'Downloading blob: {blobname}')
    return urllib.request.urlretrieve(call, blobname)

# Laddar ner blobar från en lista skapad från en fil
def download_blob_from_list(filename, url, sas):
    blobsum = 0
    blobfel = 0
    try:
        bloblist = open(filename)
    except:
        print("Kunde inte öppna filen")
    for blob in bloblist:
        blobname = blob.strip()
        try:
            download_blob(url,blobname,sas)
            blobsum +=1
        except:
            print(f'Failed to download {blobname}')
            blobfel +=1
    if blobfel > 0:
        print(f"ERROR! Kunde inte ladda hem {blobfel} blobar!")
    print(f"Laddade hem {blobsum} blobar!")
    return 'Done!'

# Hämtar namn på alla blobar
def get_blobnames(url, sas):
    calltypelist = '&restype=container&comp=list&include=metadata'
    call = url + sas + calltypelist
    request = urllib.request.urlopen(call, context=ctx)
    data = request.read()
    tree = ET.fromstring(data)
    return tree.findall('.//Name')

# Hämtar hem en xml-fil med uppgifter om alla blobar i azure
def get_bloblist_as_xml(url, sas):
    calltypelist = '&restype=container&comp=list&include=metadata'
    call = url + sas + calltypelist
    request = urllib.request.urlopen(call, context=ctx)
    data = request.read()
    xmlstring = ET.fromstring(data)
    parsed = ET.ElementTree(xmlstring)
    parsed.write('bloblist.xml', xml_declaration=True, encoding='utf-8')
    print('Outputfil "bloblist.xml" skapad')
    return 'Outputfil skapad'

# Hämtar hem uppgifter om alla blobarna i azure och returnerar dessa som en sträng
def get_bloblist_as_string(url, sas):
    calltypelist = '&restype=container&comp=list&include=metadata'
    call = url + sas + calltypelist
    request = urllib.request.urlopen(call, context=ctx)
    data = request.read()
    fromstring = ET.fromstring(data)
    return ET.tostring(fromstring)

# Deletar blob från azure
def delete_blob(url, blobname, sas):
    call = f'{url}/{blobname}{sas}'
    print(f'Delete blob: {blobname}')
    deleterequest = urllib.request.Request(call,headers= {'Content-Type':'application/zip'}, method="DELETE")
    try:
        response = urllib.request.urlopen(deleterequest)
        print("Lyckades: " + response.read().decode('utf8'))
    except urllib.error.URLError as error:
        print("Error... " + error.read().decode('utf8'))


# Hantera ev certifikatsproblem
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# URL och nycklar
jsonfile = open('H:\Pythonlekstuga\SocialamedierBLOB\keys.json')
key = json.load(jsonfile)

facebook_url = key['facebook_url']
facebook_sas = key['facebook_sas']
instagram_url = key['instagram_url']
instagram_sas = key['instagram_sas']

# Hämta BLOB-listan som XML
#get_bloblist_as_xml(facebook_url,facebook_sas)

download_blob_from_list('blobsfordownload.txt',facebook_url,facebook_sas)

