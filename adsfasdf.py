import torch

a = torch.ones([31, 62])
a[1][2] = 3
print(a)