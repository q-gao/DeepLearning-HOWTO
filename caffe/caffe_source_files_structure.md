

```shell
|-- include    # c++ and cuda header files
|-- python     # pycaffe
|-- scripts
|-- src        # caffe source c++ and cu codes
`-- tools
```

## `src/`

```shell
src
|-- caffe/
|   |-- layers/
|   |-- proto/
|   |   `-- caffe.proto  # prototxt message def. generated c++ files in build/src/caffe/proto/
|   |-- solvers/
|   |-- test/
|   |-- util/
|   |-- blob.cpp
|   |-- CMakeLists.txt
|   |-- common.cpp
|   |-- data_reader.cpp
|   |-- data_transformer.cpp
|   |-- internal_thread.cpp
|   |-- layer.cpp
|   |-- layer_factory.cpp
|   |-- net.cpp
|   |-- parallel.cpp
|   |-- solver.cpp
|   `-- syncedmem.cpp
`-- gtest/
```