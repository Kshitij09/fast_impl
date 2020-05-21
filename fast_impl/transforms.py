# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/preprocessing.ipynb (unless otherwise specified).

__all__ = ['min_max_scale', 'norm', 'GlobalContrastNorm', 'ZCAWhitenWrapper']

# Cell
from fastai2.vision.all import *

# Cell
def min_max_scale(x:Tensor,min=0,max=1):
  return min + ((x-x.min()) * (max-min)) / (x.max()-x.min())

# Cell
def norm(x:Tensor):
  "Borrowed from torchvision.utils"
  return x.add(-x.min()).div(x.max()-x.min()+1e-5)

# Cell
class GlobalContrastNorm(Transform):
  """prevents images from having varying contrast
  reference: Deep Learning book (section 12.2.1.1 pg.455)
  decodes used for `show_batch`, not to reverse the transform.
  """
  order=11 # Need to be applied after IntToFloatTensor
  def __init__(self,s=1,eps=1e-8,lmbda=0.):
    store_attr(self,'s,eps,lmbda')

  def encodes(self, x:TensorImage):
    no_batch = x.dim()<4
    grayscale = no_batch and x.shape[0]==1
    if grayscale: x = x[None,None]
    if no_batch: x = x[None]
    assert x.dim()==4,"ValueError: Invalid Tensor Dimensions"
    contrast = (x.var((1,2,3),keepdim=True)+self.lmbda).sqrt().clamp_(self.eps)
    return self.s * (x - x.mean((1,2,3),keepdim=True)) / contrast

  def decodes(self,x:TensorImage): return min_max_scale(x)

# Cell
import kornia

# Cell
class ZCAWhitenWrapper(Transform,GetAttr):
  "Wrapping kornia implementation"
  _default='_zca'
  @delegates(kornia.color.ZCAWhitening)
  def __init__(self,**kwargs):
    self._zca = ZCAWhitening(**kwargs)

  def setups(self,dl:DataLoader):
    if not self._zca.fitted:
      x,*_ = dl.one_batch()
      self._zca = self._zca.fit(x)

  def encodes(self,x:TensorImage): return self._zca(x)
  def decodes(self,x:TensorImage):
    if self._zca.compute_inv:
      x = self._zca.inverse_transform(x)
    return min_max_scale(x)