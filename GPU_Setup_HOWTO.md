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