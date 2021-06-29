import os
import cv2
import shutil

DATADIR = './workspace/training_demo/images'
FOLDERS = ['train', 'test']

TEXT = '	<path>{}</path>'

for folder in FOLDERS:
    path = os.path.join(DATADIR, folder)
    for xml_name in os.listdir(path):
        if (xml_name.endswith('.xml')):
            XML_PATH = os.path.join(path, xml_name)
            try:
                lines = open(XML_PATH).read().splitlines()
                lines[4] = TEXT.format('{}/{}/{}'.format(DATADIR, folder, xml_name))
                lines = lines[1:]
                open(XML_PATH,'w').write('\n'.join(lines))
            except Exception as e:
                print(e)