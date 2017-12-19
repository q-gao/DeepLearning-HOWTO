#!/usr/bin/python
from __future__ import print_function

import sys
import os
import cv2
import numpy as np

rootDir = '/local/mnt2/workspace2/DataSets/VOCData/VOCdevkit/COCO_val2014/'
img_list_dir = rootDir + 'ImageSets/Main/'
img_dir      = rootDir + 'JPEGImages/'
img_list_file = img_list_dir + 'valminusminival2014_3ch.txt'

ch_mean = np.zeros((3,), dtype=np.uint64)
pixel_cnt = np.uint64(0)
img_cnt = 0
with open(img_list_file) as ilf:
	for line in ilf:
		img_file = img_dir + line.strip() + '.jpg'
		if not os.path.isfile(img_file):
			print('Not find ' + img_file)
			continue

		img = cv2.imread(img_file)
		if len(img.shape) < 3 or img.shape[2] != 3:
			print('Not 3 channel image: ' + img_file)
			continue

		if img_cnt % 100 == 0:
			print(img_cnt, end='\r')
			sys.stdout.flush()
		img_cnt += 1

		s = np.sum( np.sum(img, axis=0, dtype=np.uint32), axis = 0, dtype=np.uint32)
		pixel_cnt += np.uint64(img.shape[0] * img.shape[1])
		ch_mean += s.astype(np.uint64)

ch_mean /= pixel_cnt
print('Channel means of {} images'.format(img_cnt))
print(ch_mean)

