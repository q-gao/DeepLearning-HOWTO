http://torch.ch/docs/getting-started.html#_

# Issues

## Make it work with `libcudnn.so.7`

https://github.com/soumith/cudnn.torch/issues/383

```sh
git clone https://github.com/soumith/cudnn.torch.git -b R7 && cd cudnn.torch && luarocks make cudnn-scm-1.rockspec

export CUDNN_PATH="/usr/local/cuda-9.0/lib64/libcudnn.so.7"
```