import ssl
import urllib.request, urllib.parse, urllib.error, urllib
import xml.etree.ElementTree as ET
import json


def download_blob(url, blobname, sas):
    call = f'{url}/{blobname}{sas}'
    print(f'Downloading blob: {blobname}')
    return urllib.request.urlretrieve(call, blobname)


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
#get_bloblist_as_xml(facebook_url,facebook_sas)

download_blob_from_list('blobsfordownload.txt',facebook_url,facebook_sas)

