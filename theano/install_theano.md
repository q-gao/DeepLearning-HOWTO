http://deeplearning.net/software/theano/install_ubuntu.html

theano works the best with Python 2.7

https://lasagne.readthedocs.io/en/latest/

 ```sh
conda install mkl mkl-service
conda install nose sphinx pydot-ng
pip install parameterized
# conda install theano pygpu # stable version
# bleading edge theano and pygpu
pip install git+https://github.com/Theano/Theano.git#egg=Theano
conda install -c mila-udem pygpu
# lasagne
pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
# To use MKL 2018 with Theano you MUST set **"MKL_THREADING_LAYER=GNU"** in
# your environement
 export MKL_THREADING_LAYER=GNU
 conda install -c conda-forge moviepy
 conda install -c anaconda cryptography
 ```

 ## Using **GPU**

 ### Use single GPU
 
 http://deeplearning.net/software/theano/tutorial/using_gpu.html

```shell
# device=cuda to require the use of the GPU. 
# device=cuda{0,1,...} to specify which GPU to use
THEANO_FLAGS=device=cuda0 python gpu_tutorial1.py
```

### Use Multiple GPU's

http://deeplearning.net/software/theano/tutorial/using_multi_gpu.html

Use GpuArray backend

theano provides high level of abstraction so that you do not refer to device names directly for multiple-gpu use
- You instead refer to what we call **context names**. 
- They are then mapped to a device using the theano configuration.

```
THEANO_FLAGS="contexts=dev0->cuda0;dev1->cuda1" python -c 'import theano'
```
BUT in the codes, you have to use **`target`** to **explicitly** specify which device to use!!. For example, 
```python
v01 = theano.shared(numpy.random.random((1024, 1024)).astype('float32'),
                    target='dev0')
v02 = theano.shared(numpy.random.random((1024, 1024)).astype('float32'),
                    target='dev0')
v11 = theano.shared(numpy.random.random((1024, 1024)).astype('float32'),
                    target='dev1')
v12 = theano.shared(numpy.random.random((1024, 1024)).astype('float32'),
                    target='dev1')
```

## Issues

### `WARNING (theano.tensor.blas): Using NumPy C-API based implementation for BLAS functions.`
  - Can not find mkl and use numpy instead that's slower
  https://github.com/Theano/Theano/issues/6532

**my fix on Ubuntu 16.04**

```sh
# MKL is a optimized version of BLAS
setenv MKL_THREADING_LAYER GNU
locate libmkl
# Add libmkl path
setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/local/mnt/workspace/Apps/anaconda2/lib
```
http://deeplearning.net/software/theano/troubleshooting.html#how-do-i-configure-test-my-blas-library



> It mean Theano can't find blas. So it call it indirectly via numpy. This
slow down computation for many technical reason.

>An easy fix as you use conda is to execute:

>"conda install mkl"

```sh
theano-cache clea  # inside anaconda2\bin
```