from lxml import etree as ET
import os
import time

cwd = os.getcwd()

# Ändra till de värden som motsvarar kanal och tidspann som ska arkiveras
channel_key = 'boras_stad-17841401875662925'
usertime = '2021-01-01'
inputtime = time.strptime(usertime, '%Y-%m-%d')

document = open('bloblist.xml', encoding="utf8")
tree = ET.parse(document)


blobs = tree.findall('Blobs/Blob')

outputfile = open('blobsfordownload.txt', 'w')

for blob in blobs:
    xml_channel_key = blob.find('Metadata/channelKey').text
    xml_blobtype = blob.find('Metadata/blobType').text
    if (xml_channel_key == channel_key) and (xml_blobtype == 'Document'):
        publish_time = blob.find('Metadata/publishDate').text
        publish_date = time.strptime(publish_time.split('T')[0], '%Y-%m-%d')
        if inputtime <= publish_date:
            blobname = blob.find('Name').text
            outputfile.write(f'{blobname}\n')
            print(blobname)
            print(publish_time)

