import numpy as np
import torch
from PIL import Image


def load_image(filename, size=None, is_content=False):
    img = Image.open(filename).convert('RGB')
    if is_content:
        size2 = int(size * 1.0 / img.size[0] * img.size[1])
        img = img.resize((size, size2), Image.ANTIALIAS)
    else:
        img = img.resize((size, size), Image.ANTIALIAS)
    img = np.array(img).transpose(2, 0, 1)
    img = torch.from_numpy(img).float().unsqueeze(0)
    img = img.transpose(0, 1)
    (r, g, b) = torch.chunk(img, 3)
    img = torch.cat((b, g, r))
    img = img.transpose(0, 1)
    return img


def save_image(tensor, filename):
    (b, g, r) = torch.chunk(tensor, 3)
    tensor = torch.cat((r, g, b))
    img = tensor.clone().clamp(0, 255).numpy()
    img = img.transpose(1, 2, 0).astype('uint8')
    img = Image.fromarray(img)
    img.save(filename)
