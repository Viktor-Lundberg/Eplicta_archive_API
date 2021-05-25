from zipfile import ZipFile
import xml.etree.ElementTree as ET
import os


def xmlmedkommentar(document, kommentar):
    tree = ET.parse(document)
    root = tree.getroot()
    root.tag = 'post'
    tree2 = ET.parse(kommentar)
    root2 = tree2.getroot()
    xmlpath = root.find("*/file[@name='Content/comments.xml']")
    parent = root.find('resources')
    parent.remove(xmlpath)
    ET.Element.append(root, root2)
    return root


def xmlutankommentar(document):
    tree = ET.parse(document)
    root = tree.getroot()
    root.tag = 'post'
    return root


# OUTPUTFILEN
outputroot = ET.Element('document')
outputtree = ET.ElementTree(outputroot)

cwd = os.getcwd()

with os.scandir(cwd) as it:
    for entry in it:
        if entry.name.endswith('zip'):
            commentsxml = None
            with ZipFile(entry, 'r') as zip:
                print(f'JOBBAR MED {entry}')
                zip.extract('document.xml')
                try:
                    zip.extract('Content/comments.xml', path=cwd)
                    commentsxml = True
                except:
                    commentsxml = False
                zip.extractall() #OBS! ANVÄND VID SKARP KÖRNING!
            if commentsxml == True:
                root = xmlmedkommentar('document.xml', 'Content/comments.xml')
                ET.Element.append(outputroot, root)
            else:
                root = xmlutankommentar('document.xml')
                ET.Element.append(outputroot,root)
    print('klar!')
outputtree.write('arkiverad_kanal.xml', xml_declaration=True, encoding='utf-8')

# DELETE COMMENTS.XML I CONTENTMAPPEN
if os.path.exists(f'{cwd}/Content/comments.xml'):
    print('TAR BORT COMMENTS.XML')
    os.remove(f'{cwd}/Content/comments.xml')