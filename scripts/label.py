import os
import cv2
import shutil

DATADIR = './balls'
IMAGEDIR = './images'
CATEGORIES = ['white', 'red', 'yellow', 'green', 'brown', 'blue', 'pink', 'black']

TEXT = '''
<annotation>
	<folder>balls</folder>
	<filename>{}</filename>
	<path>{}</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>{}</width>
		<height>{}</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name>{}</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>0</xmin>
			<ymin>0</ymin>
			<xmax>{}</xmax>
			<ymax>{}</ymax>
		</bndbox>
	</object>
</annotation>
'''


for category in CATEGORIES:
    path = os.path.join(DATADIR, category)
    i = 0
    for img_name in os.listdir(path):
        try:
            i += 1
            img = cv2.imread(os.path.join(path, img_name))
            label = TEXT.format(
                        img_name,
                        os.path.abspath(os.path.join(IMAGEDIR, img_name)),
                        img.shape[1],
                        img.shape[0],
                        category,
                        img.shape[1],
                        img.shape[0],
                )
            test_train = 'test' if i % 5 == 0 else 'train' # 20% test, 80% train

            shutil.copyfile(os.path.join(path, img_name), os.path.join(IMAGEDIR, test_train, img_name))
            
            f = open(os.path.join(IMAGEDIR, test_train, img_name.split('.')[0] + '.xml'), "a")
            f.write(label)
            f.close()
        except Exception as e:
            print(e)
