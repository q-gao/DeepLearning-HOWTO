# BLAS/LAPACK

Great explanation at http://markus-beuckelmann.de/blog/boosting-numpy-blas.html

BLAS/LAPACK are spec's. Their implementations:
- BLAS/LAPACK
- ATLAS
- OpenBlas
- MKL(Intel Math Lib)

According to [this overstock post](https://stackoverflow.com/questions/37224631/does-anaconda-4-0-2-already-runs-numpy-on-mkl)
> starting with Anaconda 2.5 MKL support is the default

[Just on Windows](https://groups.google.com/a/continuum.io/forum/#!topic/anaconda/8KMAd2O0a34)?
>  on Windows (unlike Unix, where Anaconda offers non-MKL alternatives) numpy and scipy are always linked against MKL.

However, I found the followings:
```
cd pkgs/numpy-1.13.3-py27hbcc08e0_0/lib/python2.7/site-packages/numpy/linalg
ldd lapack_lite.so
```