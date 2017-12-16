#!/usr/bin/python
from __future__ import print_function

from pycocotools.coco import COCO
import textwrap
import os.path

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
    templateFixed = '''\
      <annotation>
        <folder>{}</folder>
        <filename>{}</filename> 
        <source>
            <database>The COCO Database</database>
            <annotation>COCO</annotation>
            <image>flickr</image>
            <flickrid>TBD</flickrid>
        </source>
        <owner>
            <flickrid>TBD</flickrid>
            <name>TBD</name>
        </owner>
        <size>
            <width>{}</width>
            <height>{}</height>
            <depth>3</depth>
        </size>
        <segmented>0</segmented>   
    '''  # folder filename, width, height
    templateObj = '''\
        <object>
            <name>{}</name>
            <pose>Left</pose>
            <truncated>1</truncated>
            <difficult>0</difficult>
            <bndbox>
                <xmin>{}</xmin>
                <ymin>{}</ymin>
                <xmax>{}</xmax>
                <ymax>{}</ymax>
            </bndbox>
        </object>    
    '''  # name xmin ymin xmax ymax

    def __init__(self):
        self.d_CocoLabel2VocLabel = {}
        for k, v in Coco2VocGTConveter.d_VocLabel2CocoLabel.items():
            self.d_CocoLabel2VocLabel[v] = k

    def ConvertFile(self, cocoJsonFile, vocXmlDir, imgListFile):
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

                vocXml = self.PerImgConvert(ii, anns)
                if vocXml is None:  continue
                d_includedImgNms[imgFileNm] = True
                xmlFileNm = vocXmlDir + '/' +  os.path.splitext(imgFileNm)[0] + '.xml'
                print("{} => {}".format(imgFileNm, xmlFileNm))
                try:
                    with open(xmlFileNm, 'w') as f:
                        f.write(vocXml)
                    numXmlFiles+= 1
                except IOError:
                    print('Failed to open {} for writing'.format(numXmlFiles))

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

        xmlObj = ''
        for a in cocoAnno:
            catNm = self.d_catId2Name[a['category_id']]
            if catNm in self.d_CocoLabel2VocLabel:
                vocCatNm = self.d_CocoLabel2VocLabel[catNm]
            else:
                vocCatNm = catNm
            if vocCatNm not in Coco2VocGTConveter.d_voc_labels:
                continue
            if a['iscrowd']:
                self.numIsCrowd += 1
                continue
            xmin = float(a['bbox'][0])
            ymin = float(a['bbox'][1])
            xmax = float(a['bbox'][2]) + xmin
            ymax = float(a['bbox'][3]) + ymin
            xmlObj += Coco2VocGTConveter.templateObj.format(
                vocCatNm,
                int(xmin + 0.5), int(ymin + 0.5), int(xmax + 0.5), int(ymax + 0.5)
            )
        if xmlObj == '':
            return None
        xmlFixed = Coco2VocGTConveter.templateFixed.format('COCO35k',  # folder
                                                           cocoImgInfo['file_name'],  # image file name
                                                           cocoImgInfo['width'],  # image width
                                                           cocoImgInfo['height']  # image height
                                                           )

        return textwrap.dedent(xmlFixed + xmlObj) + '</annotation>\n'

if __name__ == '__main__':
    c = Coco2VocGTConveter()

    # cocoGtFile = '/local/mnt/workspace/qgao/COCO/annotations/instances_train2014.json'
    # c.ConvertFile(cocoGtFile, '/local/mnt/workspace/qgao/VOCData/VOCdevkit/COCO_train2014/Annotations',
    #               '/local/mnt/workspace/qgao/VOCData/VOCdevkit/COCO_train2014/ImageSets/Main/trainl2014.txt'
    # )

    #cocoGtFile = '/local/mnt/workspace/qgao/COCO/annotations/instances_minival2014.json'
    #cocoGtFile = '/local/mnt/workspace/qgao/COCO/annotations/instances_valminusminival2014.json'
    cocoGtFile = '/local/mnt/workspace/qgao/COCO/annotations/instances_val2014.json'
    c.ConvertFile(cocoGtFile, '/local/mnt/workspace/qgao/VOCData/VOCdevkit/COCO_val2014/Annotations',
                  '/local/mnt/workspace/qgao/VOCData/VOCdevkit/COCO_val2014/ImageSets/Main/val2014.txt'
    )