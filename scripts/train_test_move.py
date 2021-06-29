import os
import shutil

DATADIR = './balls'
CATEGORIES = ['white', 'red', 'yellow', 'green', 'brown', 'blue', 'pink', 'black']

for category in CATEGORIES:
	path = os.path.join(DATADIR, category)
	i = 0
	for tt in ['test', 'train']:
		for img_name in os.listdir(os.path.join(path, tt)):
			try:
				new_path = os.path.join(DATADIR, tt, category)
				shutil.move(os.path.join(path, tt, img_name), new_path)
			except Exception as e:
				print(e)
