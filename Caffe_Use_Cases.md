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
`data/VOC0712/create_list.sh` will create 3 files:
- `data/VOC0712/trainval.txt`:  16551 files = 5011 VOC07 + 11540 VOC12
>`VOC2012/JPEGImages/2008_002422.jpg VOC2012/Annotations/2008_002422.xml`

- `data/VOC0712/test.txt`: same format as above
- `data/VOC0712/test_name_size.txt`: example line below
>`000001 500 353  #(Height Width) found by get_image_size.cpp`


#### Create lmdb
`data/VOC0712/create_data.sh` will lmdb files
