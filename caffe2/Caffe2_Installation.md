<!-- TOC -->

- [`caffe2` Set-up](#caffe2-set-up)
    - [Building](#building)
        - [Issues](#issues)
            - [Multiple `libopencv`](#multiple-libopencv)
    - [Run](#run)
- [`Detectron` Set-up](#detectron-set-up)

<!-- /TOC -->

# `caffe2` Set-up

Use **python 2.7**

## Building

Assume `caffe` can be successfully built and Anaconda python is used.

For building caffe
```sh
# point /usr/bin/python to anaconda_python
# Add anaconda python's bin to PATH
conda install -c anaconda protobuf
conda install -c anaconda setuptools
```

### Issues

#### Multiple `libopencv`
**mixing Anaconda packages with system packages.**
It is possible that you have OpenCV installed as Anaconda package, but ALSO as system package. Then at link/load time when it tries to link/load OpenCV, it also tried to load libtiff.so and finds the system package instead of the Anaconda package.

The building script encounters `ld` errors with regard to `/usr/lib/x86_64-linux-gnu/libopencv`: ld tried to load libtiff installed in Anaconda instead of `/usr/lib/x86_64-linux-gnu`. The following forces `ld` to use `/usr/lib/x86_64-linux-gnu`

```sh
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
```

## Run

Add `<caffe2_root>/build` to `PYTHONPATH` if needed.

For running caffe2
```sh
conda install -c anaconda future
conda install -c conda-forge hypothesis
```

# `Detectron` Set-up

Use `python2` in its script.

Anaconda has `pip`
```sh
pip install opencv-python>=3.0 mock
```
