#!/usr/bin/python
"""
This script uses $caffe_root/scripts/create_annoset.py to create LMDB from a VOC like structure
    VOCdevkit/
    |-- WIDER_train/
    |   |-- Annotations/
    |   |-- ImageSets/
    |   |   `-- Main/
    |   |       `-- WIDER_train.txt
    |   `-- JPEGImages/
    `-- WIDER_val/
        |-- Annotations/
        |-- ImageSets/
        |   `-- Main/
        |       `-- WIDER_train.txt
        `-- JPEGImages/

ASSUMPTIONS:
  - all images files have 'jpg" suffix
"""

from __future__ import print_function
import os.path
from os import remove
from random import shuffle

def create_img_voc_xml_mapping_list( l_img_list_file):
    '''
    :param l_img_list_file:
    :return:
        - img_voc_xml_mapping_list: the path in the list is relative to "data_root_dir" returned below
        - data_root_dir
    '''
    img_voc_xml_mapping_list = []
    data_root_dir = None
    for img_list_file in l_img_list_file:
        ml, drd = create_img_voc_xml_mapping_list_single(img_list_file)
        if data_root_dir is None:
            data_root_dir = drd
        elif data_root_dir != drd:
            print('ERROR: all the image list files should be in the same data root dir with VOC like structure')
            import sys; sys.exit(-1)

        img_voc_xml_mapping_list += ml

    return img_voc_xml_mapping_list, data_root_dir

def parent_at_level(path, level):
    for l in xrange(level):
        path = os.path.dirname(path)
    return path

def create_img_voc_xml_mapping_list_single( img_list_file):
    fullpath = os.path.realpath(img_list_file)
    dataset_name = parent_at_level(fullpath, 3)
    data_root_dir = parent_at_level(dataset_name, 1)
    dataset_name = os.path.basename(dataset_name)

    try:
        img_voc_xml_mapping_list = []
        with open(fullpath) as ilf:
            for line in ilf:
                image_name = line.strip()
                if len(image_name) <= 0:
                    continue
                img_voc_xml_mapping_list.append(
                    "{} {}".format(
                        os.path.join(dataset_name, 'JPEGImages', image_name + '.jpg'),
                        os.path.join(dataset_name, 'Annotations', image_name + '.xml')
                    )
                )
        return img_voc_xml_mapping_list, data_root_dir

    except IOError:
        print('FAILED to open ', img_list_file)
        import sys; sys.exit(-1)

if __name__ == '__main__':
    label_map_file = '/local/mnt/workspace/qgao/Github/caffe-ssd/data/WIDER/label_map_face.prototxt'
    type = 'train' # 'val'
    l_img_list_file = [
        '/local/mnt2/workspace2/DataSets/VOCData/VOCdevkit/WIDER_{}/ImageSets/Main/WIDER_{}.txt'.format(type, type)
        #'/local/mnt2/workspace2/DataSets/VOCData/VOCdevkit/WIDER_train/ImageSets/Main/WIDER_train.txt'
    ]

    print('Loading ', l_img_list_file)
    mapping_list, data_root_dir = create_img_voc_xml_mapping_list(l_img_list_file)
    lmdb_loc = os.path.join(data_root_dir, 'WIDER_{}/lmdb/WIDER_{}_lmdb'.format(type, type))

    print('The data root dir: ' + data_root_dir)
    tmp_mapping_list_file = 'tmp_mapping_list_file.txt'
    if os.path.exists(tmp_mapping_list_file):
        print('ERROR: {} already exists. Please remove it!'.format(tmp_mapping_list_file))
        import sys; sys.exit(-1)

    arg_list = [
        '--anno-type='       + 'detection',
        '--label-map-file='  + label_map_file,
        '--shuffle',

        '--check-label --encode-type=jpg --encoded',
        '--min-dim='         + '0',
        '--max-dim='         + '0',
        '--resize-width='    + '0',
        '--resize-height='   + '0',
        data_root_dir,
        tmp_mapping_list_file,
        lmdb_loc,
        '/local/mnt/workspace/qgao/Github/caffe-ssd/examples/WIDER'   # location to create symbolic link
    ]
    arg_str = ' '.join(arg_list)
    print('lmdb creation arguments:')
    for a in arg_list:  print(a)

    import shlex
    l_args = shlex.split(arg_str)

    import create_annoset
    ap = create_annoset.create_argparser()
    args = ap.parse_args(l_args)

    print('Saving image to VOC XML mapping to temp file ' + tmp_mapping_list_file)
    try:
        with open(tmp_mapping_list_file, 'w') as mlf:
            for line in mapping_list:
                print(line, file = mlf)

    except IOError:
        print('FAILED to create ' + tmp_mapping_list_file)
        import sys; sys.exit(-1)


    create_annoset.main(args)

    print('Remove ' + tmp_mapping_list_file)
    try:
        remove(tmp_mapping_list_file)
    except OSError:
        print('WARNING: can not remove ' + tmp_mapping_list_file)