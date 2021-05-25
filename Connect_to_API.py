import ssl
import urllib.request, urllib.parse, urllib.error, urllib
import xml.etree.ElementTree as ET
import json


def download_blob(url, blobname, sas):
    call = f'{url}/{blobname}{sas}'
    print('downloaded Blob')
    return urllib.request.urlretrieve(call, blobname)


def get_blobnames(url, sas):
    calltypelist = '&restype=container&comp=list&include=metadata'
    call = url + sas + calltypelist
    request = urllib.request.urlopen(call, context=ctx)
    data = request.read()
    tree = ET.fromstring(data)
    return tree.findall('.//Name')


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


def get_bloblist_as_string(url, sas):
    calltypelist = '&restype=container&comp=list&include=metadata'
    call = url + sas + calltypelist
    request = urllib.request.urlopen(call, context=ctx)
    data = request.read()
    fromstring = ET.fromstring(data)
    return ET.tostring(fromstring)

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
get_bloblist_as_xml(facebook_url,facebook_sas)

'''
EXEMPEL TA HEM 20 RANDOM BLOBAR
blobnames = get_blobnames(url, sas)
bloblista = list()

for blob in blobnames:
    print(blob.text)
    bloblista.append(blob.text)

for value in bloblista[:20]:
    print(url+value+sas)
    downloadblob(url,value,sas)


EXEMPEL TA HEM ENSTAKA BLOBAR

#download_blob(facebook_url,'Channel_D88535118FE84D8DAEA7BCE6BDA05CD0.zip',facebook_sas)
#download_blob(instagram_url,'Channel_91901DE358844B67A824E9D5E933ED4A.zip', instagram_sas)




EXEMPEL TA HEM UTVALDA BLOBAR FRÅN FIL

file = open('blobsfordownload.txt')
blobllista = []

for text in file:
   blob = text.strip()
   blobllista.append(blob)

for blob in blobllista:
    print(blob)
    download_blob(instagram_url,blob,instagram_sas)

'''