#!/usr/bin/python
from __future__ import print_function

from pycocotools.coco import COCO
import os.path

from VocUtil import *
from math import ceil as ceil

class Coco2VocGTConveter:
    d_VocLabel2CocoLabel = {
        "aeroplane": "airplane",
        "diningtable": "dining table",
        "pottedplant": "potted plant",
        "tvmonitor": "tv",
        "motorbike": "motorcycle",
        "sofa": "couch"
    }
    d_voc_labels = {
        'aeroplane': 1, 'bicycle': 1,
        'bird': 1, 'boat': 1,
        'bottle': 1, 'bus': 1,
        'car': 1, 'cat': 1,
        'chair': 1, 'cow': 1,
        'diningtable': 1, 'dog': 1,
        'horse': 1, 'motorbike': 1,
        'person': 1, 'pottedplant': 1,
        'sheep': 1, 'sofa': 1,
        'train': 1, 'tvmonitor': 1
    }

    def __init__(self):
        self.d_CocoLabel2VocLabel = {}
        for k, v in Coco2VocGTConveter.d_VocLabel2CocoLabel.items():
            self.d_CocoLabel2VocLabel[v] = k

    def ConvertFile(self, cocoJsonFile, imgDir, vocXmlDir, imgListFile):
        # load Json
        print('Loading COCO GT {} ...'.format(cocoJsonFile))
        coco_gt = COCO(cocoJsonFile)

        catIds = coco_gt.getCatIds()  # a list of IDs 1-90
        cats = coco_gt.loadCats(catIds)  # a list of cats
        # Each cat is a dict:
        #     supercategory  vehicle
        #     id             2
        #     name           bicycle
        self.d_catId2Name = {}
        for c in cats:
            self.d_catId2Name[c['id']] = c['name']

        d_includedImgNms = {}
        numXmlFiles = 0
        self.numIsCrowd = 0
        for vocCatNms in Coco2VocGTConveter.d_voc_labels.keys():
            if vocCatNms in Coco2VocGTConveter.d_VocLabel2CocoLabel:
                cocoCatNms = Coco2VocGTConveter.d_VocLabel2CocoLabel[vocCatNms]
            else:
                cocoCatNms = vocCatNms

            catIds = coco_gt.getCatIds(catNms=[cocoCatNms]);
            imgIds = coco_gt.getImgIds(catIds=catIds);

            imgInfos = coco_gt.loadImgs(imgIds)  # return a list matching the imgIds provided

            for ii in imgInfos:
                #annIds = coco_gt.getAnnIds(imgIds=ii['id'], iscrowd=False)  # catIds=catIds,
                annIds = coco_gt.getAnnIds(imgIds=ii['id'], iscrowd=None)  # catIds=catIds,
                anns = coco_gt.loadAnns(annIds)  # return a list
                imgFileNm = ii['file_name']
                if imgFileNm in d_includedImgNms:  continue

                _, _, ii['depth'] = GetImageDimension(os.path.join(imgDir, imgFileNm))
                if ii['depth'] is None:
                    print('FAILED to open {} in {}'.format(imgFileNm, imgDir))
                    import sys; sys.exit(-1)

                ii['depth'] = ceil(ii['depth'] / 8) # from bits to # channels
                if ii['depth'] <= 0:    ii['depth'] = 1

                if ii['depth'] != 3:
                    print(imgFileNm, ii['depth'])

                vocXml = self.PerImgConvert(ii, anns)
                if vocXml is None:  continue
                d_includedImgNms[imgFileNm] = True
                xmlFileNm = vocXmlDir + '/' +  os.path.splitext(imgFileNm)[0] + '.xml'
                #print("{} => {}".format(imgFileNm, xmlFileNm))
                try:
                    with open(xmlFileNm, 'w') as f:
                        f.write(vocXml)
                    numXmlFiles+= 1
                except IOError:
                    print('Failed to open {} for writing'.format(xmlFileNm))

        print('\nCreating image list file {} ...'.format(imgListFile))
        with open(imgListFile, 'w') as f:
            for k in sorted(d_includedImgNms.keys()):
                f.write(os.path.splitext(imgFileNm)[0] + '\n')

        print('\nTotal {} VOC XML files are generated: numIsCrowd={}'.format(numXmlFiles, self.numIsCrowd))

    def PerImgConvert(self, cocoImgInfo, cocoAnno):
        '''
        cocoImgInfo:
        ------------
        license          1
        url              http://farm3.staticflickr.com/2510/4227189174_b89c0a56d6_z.jpg
        file_name        COCO_val2014_000000240434.jpg
        height           427
        width            640
        date_captured    2013-11-22 01:04:35
        id               240434

        cocoAnno is a list of annotations with each element like below:
        -----------
        segmentation   [[333.98, 253.95, 361.48, 255.05, 364.23]]
        area           947.61635
        iscrowd        0
        image_id       240434
        bbox           [332.61, 223.7, 31.62, 31.35]
        category_id    72
        id             28385
        '''

        anno = []
        for a in cocoAnno:
            if a['iscrowd']:
                self.numIsCrowd += 1
                continue

            catNm = self.d_catId2Name[a['category_id']]
            if catNm in self.d_CocoLabel2VocLabel:
                vocCatNm = self.d_CocoLabel2VocLabel[catNm]
            else:
                vocCatNm = catNm
            if vocCatNm not in Coco2VocGTConveter.d_voc_labels:
                continue
            xmin = float(a['bbox'][0])
            ymin = float(a['bbox'][1])
            xmax = int(float(a['bbox'][2]) + xmin + 0.5)
            ymax = int(float(a['bbox'][3]) + ymin + 0.5)
            xmin = int(xmin + 0.5)
            ymin = int(ymin + 0.5)

            anno.append(
                {   "category_name" : vocCatNm,
                    "bbox"          : [xmin, ymin, xmax, ymax]
                }
            )

        if len(anno) <= 0:
            return None

        return VocGtWriter.GenGtXml( 'COCO35k', cocoImgInfo, anno)

if __name__ == '__main__':
    c = Coco2VocGTConveter()

    # cocoGtFile = '/local/mnt/workspace/qgao/COCO/annotations/instances_train2014.json'
    # c.ConvertFile(cocoGtFile, '/local/mnt/workspace/qgao/VOCData/VOCdevkit/COCO_train2014/Annotations',
    #               '/local/mnt/workspace/qgao/VOCData/VOCdevkit/COCO_train2014/ImageSets/Main/trainl2014.txt'
    # )

    #cocoGtFile = '/local/mnt/workspace/qgao/COCO/annotations/instances_minival2014.json'
    #cocoGtFile = '/local/mnt/workspace/qgao/COCO/annotations/instances_valminusminival2014.json'
    cocoGtFile = '/local/mnt/workspace/qgao/COCO/annotations/instances_val2014.json'
    imgDir = '/local/mnt/workspace/qgao/COCO/images/val2014'
    # c.ConvertFile(cocoGtFile, '/local/mnt/workspace/qgao/VOCData/VOCdevkit/COCO_val2014/Annotations',
    #               '/local/mnt/workspace/qgao/VOCData/VOCdevkit/COCO_val2014/ImageSets/Main/val2014.txt'
    # )

    c.ConvertFile(cocoGtFile, imgDir, 'tmp', 't.txt')