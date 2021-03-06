# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = ['get_module', 'arch_summary', 'min_max_scale', 'norm']

# Cell
from fastai2.vision.all import *

# Cell
def _is_sequential(o): return o.__class__.__name__=='Sequential'
def _is_fn(o): return isinstance(o,(types.FunctionType, functools.partial))

# Cell
def get_module(o,i):
    "Recursively get the module from list of indices"
    o = o(False) if _is_fn(o) else o
    if is_listy(i):
        m = get_module(o,i[0])
        if len(i)==1: return m
        return get_module(m,i[1:])
    assert i < len(list(o.children())), f"IndexError: {i} is out of bounds"
    return o[i] if is_listy(o) else list(o.children())[i]

# Cell
def arch_summary(arch,idx=None,verbose=False):
  "Short architecture summary, used for holistic understanding and deciding parameter groups"
  model = arch(False) if _is_fn(arch) else arch
  if idx is not None:
    model = get_module(model,idx)
  for i,(n,l) in enumerate(model.named_children()):
      n_layers = len(l if _is_sequential(l) else flatten_model(l))
      pre = f'[{n:<2}]' if n.isdigit() else f'[{i:<2}] {"("+n+")":<10}'
      print(f'{pre} {l.__class__.__name__:<17}: {n_layers:<3} layers')
      if verbose and l.has_children:
        layers = [x.__class__.__name__ for x in l.children()]
        for il in layers:
          print(" "*(5 + (15 if not n.isdigit() else 0)),il)

# Comes from 01_preprocessing.ipynb, cell
def min_max_scale(x:Tensor,min=0,max=1):
  return min + ((x-x.min()) * (max-min)) / (x.max()-x.min())

# Comes from 01_preprocessing.ipynb, cell
def norm(x:Tensor):
  "Borrowed from torchvision.utils"
  return x.add(-x.min()).div(x.max()-x.min()+1e-5)