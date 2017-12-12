# Caffe Use Cases

## SSD Object Detection

### Build

- Go to https://github.com/weiliu89/caffe/tree/ssd to download ssd code and follow the steps to compile and make demo work. If cloning https://github.com/weiliu89/caffe.git, make sure checkout **ssd** branch.

- Add conv\_dw\_layer related files (in the folder `DepthwiseLayers`)
```shell
cd $CAFFE_ROOT
cp path/to/conv_dw_layer.cpp src/caffe/layers/
cp path/to/conv_dw_layer.cu src/caffe/layers/
cp path/to/conv_dw_layer.hpp include/caffe/layers/
```

- Regular caffe build process. Someone uses `cmake`
```shell
mkdir build
cd build
cmake ..
make all
make install
make runtest
```

### Data Preparation

#### Datasets

Data layout
```shell
VOCData/VOCdevkit/
├── COCO_val2014/
│   ├── Annotations/
│   ├── ImageSets/
│   ├── JPEGImages -> /local/mnt/workspace/qgao/COCO/images/val2014//
│   ├── lmdb/
├── VOC0712/
│   └── lmdb/
├── VOC2007/
│   ├── Annotations/
│   ├── ImageSets/
│   ├── JPEGImages/
└── VOC2012/
    ├── Annotations/
    ├── ImageSets/
    ├── JPEGImages/
```
```
caffe-ssd/examples/
├── COCO/
│   └── valminusminival2014_lmdb -> /local/mnt/workspace/qgao/VOCData/VOCdevkit//COCO_val2014/lmdb/valminusminival2014_lmdb/
├── VOC0712/
│   ├── VOC0712_test_lmdb -> /local/mnt/workspace/qgao/VOCData/VOCdevkit//VOC0712/lmdb/VOC0712_test_lmdb/
│   └── VOC0712_trainval_lmdb -> /local/mnt/workspace/qgao/VOCData/VOCdevkit//VOC0712/lmdb/VOC0712_trainval_lmdb/
```
```
caffe-ssd/data/
├── coco/
│   ├── create_data.sh*
│   ├── create_list_coco.sh*
│   ├── create_list.py
│   ├── labelmap_voc.prototxt
│   └── valminusminival2014.txt
└── VOC0712/
    ├── create_data.sh*
    ├── create_list.sh*
    ├── labelmap_voc.prototxt
    ├── test_name_size.txt
    ├── test.txt
    └── trainval.txt
```

##### VOC
```shell
├── VOC0712/
│   └── lmdb/
├── VOC2007/
│   ├── Annotations/
│   ├── ImageSets/
│   ├── JPEGImages/
└── VOC2012/
    ├── Annotations/
    ├── ImageSets/
    ├── JPEGImages/
```

##### COCO

```shell
# tree -F -L 2  # -F = format(add / for folder), -L = level
├── annotations/
│   ├── instances_minival2014.json
│   ├── instances_train2014.json
│   ├── instances_val2014.json
│   ├── instances_valminusminival2014.json
├── cocoapi/
└── images/
    ├── train2014/
    └── val2014/
```
#### Create File Info List
`data/VOC0712/create_list.sh`: 
**INPUTS:**
>`$voc_root_dir/$name/$sub_dir/$dataset.txt` (e.g., VOCdevkit/VOC2007/ImageSets/Main)

**OUTPUTS:**
- `<script_folder>/$dataset.txt`
an example line in `$dataset.txt` (note **`JPEGImages`** and **'Annotatopms'** are hard-coded):
 `VOC2007/JPEGImages/000001.jpg VOC2007/Annotations/000001.xml`
- `<script_folder>/test_name_size.txt` **if $dataset == 'test'** with example line below
>`000001 500 353  #(Height Width) found by get_image_size.cpp`

**NOTE:**
 - if `$dataset == 'trainval`', `<script_folder>/trainval.txt` is **shuffled**!


#### Create lmdb

`data/VOC0712/create_data.sh`:
**INPUTS:**
 - `$root_dir/data/$dataset_name/labelmap_voc.prototxt`
 - `$root_dir/data/$dataset_name/$subset.txt`

**OUTPUTS:**
 - `$data_root_dir/$dataset_name/lmdb/$dataset_name"_"$subset"_"lmdb`
 - symbolic links to lmdb in `'examples/$dataset_name'`

