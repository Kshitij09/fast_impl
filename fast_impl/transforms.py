# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_preprocessing.ipynb (unless otherwise specified).

__all__ = ['GlobalContrastNorm', 'to_grayscale']

# Cell
from fastai2.vision.all import *
import kornia
from kornia.color import ZCAWhitening

# Cell
class GlobalContrastNorm(Transform):
  """prevents images from having varying contrast
  reference: Deep Learning book (section 12.2.1.1 pg.455)
  decodes used for `show_batch`, not to reverse the transform.
  """
  order=104 # Need to be applied after Normalize
  def __init__(self,s=1,eps=1e-8,lmbda=0.,decode_norm=True):
    store_attr(self,'s,eps,lmbda,decode_norm')

  def encodes(self, x:TensorImage):
    no_batch = x.dim()<4
    grayscale = no_batch and x.shape[0]==1
    if grayscale: x = x[None,None]
    if no_batch: x = x[None]
    assert x.dim()==4,"ValueError: Invalid Tensor Dimensions"
    contrast = (x.var((1,2,3),keepdim=True)+self.lmbda).sqrt().clamp_(self.eps)
    return self.s * (x - x.mean((1,2,3),keepdim=True)) / contrast

  def decodes(self,x:TensorImage):
    if self.decode_norm: return norm(x)
    return x

# Comes from 07_visualize.grad_cam.ipynb, cell
def to_grayscale(im_tensor):
  gray_tensor = im_tensor.sum(0)
  im_max = np.percentile(gray_tensor.cpu().numpy(),99)
  im_min = gray_tensor.min()
  return torch.clamp((gray_tensor-im_min)/(im_max-im_min),0,1)[None]