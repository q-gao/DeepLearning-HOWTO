# torch class structure

[Great lua script to generate HTML showing class structure](https://github.com/bshillingford/lua_classviz)

**Define a new class *
```lua
-- torch.class(name, [parentName])
-- https://github.com/torch/nn/blob/master/Sequential.lua
local Sequential, _ = torch.class('nn.Sequential', 'nn.Container')
```

## Example: `nn.Sequential`

Class inheritance:
 - `root`
 - [`nn.Module`](https://github.com/torch/nn/blob/master/doc/module.md): [code](https://github.com/torch/nn/blob/master/Module.lua)
 - [`nn.Container`](https://github.com/torch/nn/blob/master/doc/containers.md): [code](https://github.com/torch/nn/blob/master/Container.lua)
 - `nn.Sequential`: [code](https://github.com/torch/nn/blob/master/Sequential.lua)

