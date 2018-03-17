# Install tensorflow

## from sources

Pre-built tensorflow may require CUDA newer than what is installed on the machine.  If upgrading is not possible, then you may still run TensorFlow with GPU support, but only if you do the following (see [here](https://www.tensorflow.org/install/install_linux#NVIDIARequirements)):
- Install TensorFlow from sources as documented in Installing TensorFlow from Sources.
- Install or upgrade to at least the following NVIDIA versions:
  - CUDA toolkit 7.0 or greater
  - cuDNN v3 or greater
  - GPU card with CUDA Compute Capability 3.0 or higher.

``` steps I performed on Ubuntu 16.04
# install google Bazel

#enables you to manage Python compressed packages in the wheel (.whl) format.
conda install -c anaconda wheel

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64 
```

# Install Google's tensorflow models

