import cv2
import numpy as np
import random
import os
import copy

from shapely.geometry import Polygon, Point

DATA_DIR = './images'

CATEGORIES = ['white', 'red', 'yellow', 'green', 'brown', 'blue', 'pink', 'black']
BG_IMG = cv2.imread("./background.png")

ANNOTATION_TEXT = '''<annotation>
	<folder>images</folder>
	<filename>{}</filename>
	<path>{}</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<WIDTH>{}</WIDTH>
		<HEIGHT>{}</HEIGHT>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
{}
</annotation>
'''

OBJECT_TEXT = '''   <object>
        <name>{}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{}</xmin>
            <ymin>{}</ymin>
            <xmax>{}</xmax>
            <ymax>{}</ymax>
        </bndbox>
    </object>'''

HEIGHT, WIDTH, CHANNELS = BG_IMG.shape

FIELD = Polygon([
    (WIDTH * 0.3, HEIGHT * 0.175), 
    (WIDTH * 0.7, HEIGHT * 0.175), 
    (WIDTH * 0.2, HEIGHT * 0.825),
    (WIDTH * 0.8, HEIGHT * 0.825)]
)

def add_random_ball(bg_img, img, poly):
    min_x, min_y, max_x, max_y = poly.bounds

    while True:
        pos = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if (pos.within(poly)):
            bg_img[int(pos.y):int(pos.y)+img.shape[0], int(pos.x):int(pos.x)+img.shape[1]] = img
            return bg_img, pos

def ball_annotation(img, category, pos):
    label = OBJECT_TEXT.format(
        category,
        int(pos.x),
        int(pos.y),
        int(pos.x + img.shape[0]),
        int(pos.y + img.shape[1]),
    )
    return label

def image_annotation(img, name, objects):
    annotation = ANNOTATION_TEXT.format(
        name,
        './workspace/training_demo/images/{}'.format(name),
        img.shape[0],
        img.shape[1],
        '\n'.join(objects)
    )
    return annotation

def create_image_with_balls():
    this_img = copy.copy(BG_IMG)
    annotations = []

    for category in CATEGORIES:
        amount = 1
        if category == 'red':
            amount = random.randint(1, 15)
        
        for b in range(amount):
            path = os.path.join('./test', category)
            ball_name = random.choice(os.listdir(path))
            ball_img = cv2.imread(os.path.join(path, ball_name))
            this_img, ball_pos = add_random_ball(this_img, ball_img, FIELD)
            annotations.append(ball_annotation(ball_img, category, ball_pos))

    return this_img, annotations

for i in range(1, 101):
    img, annotations = create_image_with_balls()
    img_name = 'image_{}.jpg'.format(i)
    cv2.imwrite(os.path.join(DATA_DIR, img_name), img)
    img_annotation = image_annotation(img, img_name, annotations)
    f = open(os.path.join(DATA_DIR, img_name.split('.')[0] + '.xml'), "w")
    f.write(img_annotation)
    f.close()