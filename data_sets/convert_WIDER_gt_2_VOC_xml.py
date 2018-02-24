#!/usr/bin/python

from __future__ import print_function
import re
import os.path
from os import makedirs
import VocUtil

def parse_wider_gt_file(gt_file):
    """
    :param gt_file:
    :return:
    """
    try:
        with open(gt_file) as gtf:
            dict_gt = {}
            parse_st = 0
            for line in gtf:
                if parse_st == 0:
                    fnm = line.strip()
                    if len(fnm) > 0:
                        parse_st = 1
                        dict_gt[fnm] = []
                elif parse_st == 1:
                    m = re.search(r'(\d+)', line)
                    if m:
                        num_bbox = int(m.group(1))
                        parse_st = 2
                        cnt_bbox = 0
                elif parse_st == 2:
                    w = line.split()
                    if len(w) == 10:
                        cnt_bbox += 1
                        if cnt_bbox > num_bbox:
                            print('ERROR in {}: found bbox number {} is larger than the specified number {}'.format(
                                fnm, cnt_bbox, num_bbox
                            ))
                        elif cnt_bbox == num_bbox:
                            parse_st = 0
                        x, y = int(w[0]), int(w[1])
                        dict_gt[fnm].append(
                            {
                                "category_name": "face",
                                "bbox": [x, y, x + int(w[2]) - 1, y + int(w[3]) - 1]
                            }
                        )
        return dict_gt

    except IOError:
        print('FAILED to open ', gt_file)
        return None

def get_wider_image_dimension(wider_gt, img_root):
    dict_img_info = {}
    for f in wider_gt.keys():
        img_file = os.path.join(img_root, f)
        dict_img_info[f] = {'file_name': f}
        dict_img_info[f]['width'], dict_img_info[f]['height'], dict_img_info[f]['depth'] = \
            VocUtil.GetImageDimension(img_file)

    return dict_img_info

def gen_voc_gt_xml(dataset_name, wider_gt, dict_img_info, voc_xml_root):
    for f in wider_gt.keys():
        xml_file = os.path.join(voc_xml_root,
                                os.path.splitext(f)[0] + '.xml'
                                )
        path = os.path.dirname(xml_file)
        if not os.path.exists(path):
            os.makedirs(path)

        try:
            with open(xml_file, 'wt') as xmlf:
                print(xml_file)
                xml = VocUtil.VocGtWriter.GenGtXml(
                    dataset_name, dict_img_info[f], wider_gt[f]
                )
                print(xml, file=xmlf)

        except IOError:
            print('ERROR: failed to create ', xml_file)
            import sys; sys.exit(-1)

# def create_dir_along_path(path):
#     list_dir = [path]
#     while(1):
#         p = os.path.dirname(path)
#         if p == path:
#             break
#         list_dir.append(p)
#         path = p
#
#     for i in xrange(len(list_dir)-1,-1, -1 ):
#         p = list_dir[i]
#         if not os.path.exists(p):


def main(args):
    wgt = parse_wider_gt_file(args.wider_gt_file)
    if wgt is None:
        import sys; sys.exit(-1)
    dict_img_info = get_wider_image_dimension(wgt, args.img_root)
    gen_voc_gt_xml('WIDER_val', wgt, dict_img_info, args.voc_xml_root)

if __name__ == '__main__':
    args = type('', (), {})
    type = 'train'
    args.wider_gt_file = '/local/mnt2/workspace2/DataSets/WIDER/wider_face_split/wider_face_{}_bbx_gt.txt'.format(type)
    args.img_root      = '/local/mnt2/workspace2/DataSets/WIDER/WIDER_{}/images'.format(type)
    args.voc_xml_root = '/local/mnt2/workspace2/DataSets/VOCData/VOCdevkit/WIDER_{}/Annotations'.format(type)
    main(args)