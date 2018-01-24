# Caffe Installation Guide

## Important Notes

- Don't use `gcc 6` as CUDA doesn't support `gcc` later than 5
- Caffe uses OpenCV 2.4 by default (3.0 works?)

## Building Steps

```shell
# will create python scripts inside python/caffe folder
make pycaffe
````

## Post-building

Add `python/caffe` to environment variable `PYTHONPATH`

## Compiler/Lib Issues

### Use the Right `gcc`

Don't use `gcc 6` as CUDA doesn't support `gcc` later than 5.

#### [Install GCC 5 on 14.04](https://gist.github.com/beci/2a2091f282042ed20cda)

```shell
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-5 g++-5
	
#sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/g++ g++ /usr/bin/g++-5
# To set 1st priority to gcc-5
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 1
```

#### [How to use multiple instances of gcc?](https://askubuntu.com/questions/313288/how-to-use-multiple-instances-of-gcc)

```shell
#Assume the variable CXX used in Makefile(as caffe's makefile does).
#https://stackoverflow.com/questions/2969222/make-gnu-make-use-a-different-compiler
make CXX=my_compiler
```

### Conflict with `anaconda`'s .so libs

#### libtiff4

OpenCV 2.4 uses it

[How-to Install libtiff4 for Ubuntu 14.04 Trusty LTSLinux Easy Guide](https://tutorialforlinux.com/2014/06/16/how-to-install-libtiff4-for-ubuntu-14-04-trusty-lts-linux-easy-guide/)

**mixing Anaconda packages with system packages.**

It is possible that you have OpenCV installed as Anaconda package, but ALSO as system package. Then at link/load time when it tries to link/load OpenCV, it also tried to load libtiff.so and finds the system package instead of the Anaconda package.

If the building script encounters `ld` errors with regard to `/usr/lib/x86_64-linux-gnu/libopencv`: ld tried to load libtiff installed in Anaconda instead of `/usr/lib/x86_64-linux-gnu`. The following forces `ld` to use `/usr/lib/x86_64-linux-gnu`

```sh
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
```









