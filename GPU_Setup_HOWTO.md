<!-- TOC -->

- [nVidia GPU Set-up](#nvidia-gpu-set-up)
    - [Find out what nVidia Driver and CUDA Toolkit have been installed](#find-out-what-nvidia-driver-and-cuda-toolkit-have-been-installed)
        - [Clean Uninstallation](#clean-uninstallation)
- [Example - 1080Ti on Ubuntu 16.04](#example---1080ti-on-ubuntu-1604)
    - [Directory Organization Guidelines](#directory-organization-guidelines)
        - [Installed Software](#installed-software)
    - [Software Installation Guides](#software-installation-guides)
        - [Install Anaconda](#install-anaconda)
            - [`lmdb`](#lmdb)
        - [Caffe's General Dependencies](#caffes-general-dependencies)
        - [CUDA Toolkit](#cuda-toolkit)
- [remove cuda](#remove-cuda)
- [This does NOT work](#this-does-not-work)
- [create /var/cuda-repo-9-1-local for apt-get to use](#create-varcuda-repo-9-1-local-for-apt-get-to-use)
- [add cuda public key](#add-cuda-public-key)
- [apt-get it](#apt-get-it)
- [to install patch](#to-install-patch)

<!-- /TOC -->

# nVidia GPU Set-up

1080 Ti works with the followings on Ubuntu 16.04:
- CUDA 8.0
- cuDNN 5.1
- Driver 384

## Find out what nVidia Driver and CUDA Toolkit have been installed

```sh
# list installed nvidia packages including driver
dpkg -l | grep nvidia
```

Example output on Ubuntu 16.04:
```sh
ii  nvidia-384                                 384.98-0ubuntu0~gpu16.04.1                   amd64        NVIDIA binary driver - version 384.98
ii  nvidia-opencl-icd-384                      384.98-0ubuntu0~gpu16.04.1                   amd64        NVIDIA OpenCL ICD
ii  nvidia-prime                               0.8.2                                        amd64        Tools to enable NVIDIA's Prime
ii  nvidia-settings                            387.22-0ubuntu0~gpu16.04.1                   amd64        Tool for configuring the NVIDIA graphics driver
```

### Clean Uninstallation

Use `dpkg --purge` to force a manual clean uninstallation. `apt` sometimes doesn't do clean uninstallation.

Use `/usr/local/cuda/bin/uninstall_cuda_toolkit_8.0.pl` if CUDA toolkit is not installed via dpkg/apt.

-----------------------------------------------------------------
I have successfully made the following downgrade on ipcva-linux-1:
- CUDA 9.1 -> 8.0
- cuDNN 7.0 -> 5.1
- Driver 384

It took me some time as my machine was quite messed up due to various factors:
- It has both Driver 384 and 387 (probably installed by IT)
- I use apt to uninstall CUDA and driver, but somehow apt doesn’t do clean uninstallation.

Once I used “dpkg --purge" to do a manual clean uninstallation,  following [steps to install CUDA without driver](https://laylatadjpour.wordpress.com/2017/05/29/installing-gtx-1080-ti-drivers-cuda-8-0-on-ubuntu-16-04/) will successfully downgrade it.
> It is OK to install multiple CUDA's. The only environment variables that matter are PATH and LD_LIBRARY_PATH. 

# Example - 1080Ti on Ubuntu 16.04

**NOTE:** if you reboot the system, please make sure you **hit enter**. It pauses because it is asking for a fan for the RAM modules you installed. If you need one, you will need to order it. Or you can use it as is. Just make sure to hit enter if it ever reboots

## Directory Organization Guidelines
There are two hard disks in the system. The guideline is (use **links** if necessary):

| local disk | Usage
|------------|---------------------
|`/local/mnt2/workspace2/`| data
|`/local/mnt/workspace/`| Executables and their related data

### Installed Software
| Software | Location
|------------|---------------------
|Anaconda 3| `/local/mnt/workspace/Apps/anaconda3`<br> `anaconda2` is a link to `anaconda3` for some compatibility reason
|Anaconda 2| Installed as `py27` environment inside `Anaconda 3`. <br> Use `bash; source activate py27` to use it.
|Eclipse | `/local/mnt/workspace/Apps/eclipse`. <br> Installed Java OpenJDK8 at `/usr/lib/jvm`?
|gitkraken |sudo apt install ./gitkraken-amd64.deb


## Software Installation Guides
[Caffe Wiki: Ubuntu 16.04 or 15.10 Installation Guide](https://github.com/BVLC/caffe/wiki/Ubuntu-16.04-or-15.10-Installation-Guide)

### Install Anaconda

Install Anaconda Python **2.7** on Ubuntu 16.04 that use Python 2.7 as default. This would save unexpected headaches, e.g., `apt -get libboost-all-dev` will use `/usr/bin/pycompiler` that imports `ConfigParser`, but `ConfigParser`has been renamed to `configparser` in Python 3.x for PEP8 compliance

``` shell
# Needed for installing libboost-python
conda install -c anaconda configparser
```
#### `lmdb`

```shell
conda install -c conda-forge python-lmdb
conda install -c conda-forge lmdb   # this alone is not enough. What is the difference?
```

### Caffe's General Dependencies

```shell
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
sudo apt-get install --no-install-recommends libboost-all-dev

sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev
```

### CUDA Toolkit

Caffe requires **CUDA 8** on Ubuntu 16.04. [Old CUDA Toolkits available here](https://developer.nvidia.com/cuda-toolkit-archive). However, CUDA 8.0 comes with a driver version (375.26) that doesn't support the GTX 1080 Ti. See the followings
on how to install 1080 Ti with CUDA 8.0 on Ubuntu 16.06:
- https://blog.nelsonliu.me/2017/04/29/installing-and-updating-gtx-1080-ti-cuda-drivers-on-ubuntu/
- https://laylatadjpour.wordpress.com/2017/05/29/installing-gtx-1080-ti-drivers-cuda-8-0-on-ubuntu-16-04/

```prime-select nvidia```

Info: the current GL alternatives in use are: ['nvidia-384', 'nvidia-384']
Info: the current EGL alternatives in use are: ['nvidia-384', 'nvidia-384']

```shell
# remove cuda
sudo apt-get autoremove --purge cuda
```
see [here to remove apt repo](https://unix.stackexchange.com/questions/219341/how-to-apt-delete-repository)
```
# This does NOT work
sudo add-apt-repository -r file:/var/cuda-repo-9-1-local
```

#### Steps
[Instructions on how to install CUDA patch](https://askubuntu.com/questions/944219/how-to-complete-a-dpkg-cublas-patch-update-to-cuda-8-installation-in-16-04)
```shell
# create /var/cuda-repo-9-1-local for apt-get to use
sudo dpkg -i cuda-repo-ubuntu1604-9-1-local_9.1.85-1_amd64.deb
# add cuda public key
sudo apt-key add /var/cuda-repo-9-1-local/7fa2af80.pub
# apt-get it
sudo apt-get update
sudo apt-get install cuda

# to install patch
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-cublas-performance-update_8.0.61-1_amd64.deb
sudo apt-get update  
sudo apt-get upgrade cuda
```

#### Post-Installtion

CUDA is installed into `/usr/local/cuda-9.1` pointered by `/usr/local/cuda`:
- Add `/usr/local/cuda/bin` to **PATH**
- '/usr/local/cuda/lib64' should be auto added to **LD_LIBRARY_PATH** by `apt-get`

More [details](http://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#post-installation-actions).

##### Samples

CUDA 8.0 samples have some build errors: can not find **-lnvcuvid**. Do the following string sub to fix this
```shell
find . -type f -execdir sed -i 's/UBUNTU_PKG_NAME = "nvidia-367"/UBUNTU_PKG_NAME = "nvidia-384"/g' '{}' \;
```

### cuDNN

According to [this](https://github.com/jcjohnson/cnn-benchmarks), ** always use cuDNN **.

cnDNN 5.1.5 works. According to [this](https://github.com/BVLC/caffe/issues/5490), cuDNN 6.0 is slower than 5.1.

[see here ](https://askubuntu.com/questions/767269/how-can-i-install-cudnn-on-ubuntu-16-04)

Register an nvidia developer account and (download cnDNN here)[https://developer.nvidia.com/cudnn]

According to Caffe, "cuDNN is sometimes but not always faster than Caffe’s GPU acceleration."

### Other Stuffs Required by Caffe

```
 sudo apt-get install libatlas-base-dev
```