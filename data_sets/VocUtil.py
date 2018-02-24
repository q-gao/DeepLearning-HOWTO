#!/usr/bin/python
from __future__ import print_function

import textwrap

from PIL import Image
mode_to_bpp = {'1':1, 
                'L':8,   # grey (levels)
                'P':8,   # pesudo color?
                'RGB':24, 
                'RGBA':32, 
                'CMYK':32, 'YCbCr':24, 
                'I':32, 'F':32
}
def GetImageDimension(img_file):
    try:
        # open(.) should not load the whole image according to
        # https://stackoverflow.com/questions/15800704/get-image-size-without-loading-image-into-memory
        # for depth, see
        # https://stackoverflow.com/questions/1996577/how-can-i-get-the-depth-of-a-jpg-file
        with Image.open(img_file) as im:            
            return (im.size[0], im.size[1], mode_to_bpp[im.mode])
    except IOError:
        return (None, None, None)

class VocGtWriter:
    templateFixed = '''\
      <annotation>
        <folder>{}</folder>
        <filename>{}</filename> 
        <source>
            <database>TBD</database>
            <annotation>TBD</annotation>
            <image>TBD</image>
            <flickrid>TBD</flickrid>
        </source>
        <owner>
            <flickrid>TBD</flickrid>
            <name>TBD</name>
        </owner>
        <size>
            <width>{}</width>
            <height>{}</height>
            <depth>{}</depth>
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

    @staticmethod
    def GenGtXml(folder, imgInfo, imgAnnotation):
        xmlFixed = VocGtWriter.templateFixed.format(folder,  # folder
                               imgInfo['file_name'],  # image file name
                               imgInfo['width'],  # image width
                               imgInfo['height'],  # image height
                               imgInfo['depth']  # image height
        )

        xmlObj = ''
        for a in imgAnnotation:
            xmin = float(a['bbox'][0])
            ymin = float(a['bbox'][1])
            xmax = float(a['bbox'][2]) + xmin
            ymax = float(a['bbox'][3]) + ymin
            xmlObj += VocGtWriter.templateObj.format(
                a['category_name'],
                *a['bbox']  # xmin, ymin, xmax, ymax
            )
        if xmlObj == '':
            return None        

        return textwrap.dedent(xmlFixed + xmlObj) + '</annotation>\n'
