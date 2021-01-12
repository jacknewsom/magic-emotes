from .base_style import BaseStyle
import numpy as np
import cv2 as cv
import json
import os

class PepegaStyle(BaseStyle):
    def __init__(self, metadata_dir='./metadata/'):
        super(PepegaStyle, self).__init__()
        if metadata_dir[-1] != '/':
            metadata_dir += '/'

        self.metadata_dir = metadata_dir

    def content_is_supported(self, content):
        '''Content emote is supported if it exists
        '''
        filename = self.metadata_dir + f'{content}/src.png'
        return os.path.isfile(filename)

    def get_magic_emote(self, content, filename):
        '''We apply the Pepega transform by giving x positions an exponential bump
        '''
        if not self.content_is_supported(content):
            raise NotImplementedError(f'{content} is not supported for this style')

        content_emote = cv.imread(self.metadata_dir+f'{content}/src.png', cv.IMREAD_UNCHANGED)

        map_x = np.arange(content_emote[...,0].size).reshape(content_emote[...,0].shape).T // len(content_emote)
        map_x = map_x.astype(np.float32)
        map_y = np.arange(content_emote[...,0].size).reshape(content_emote[...,0].shape) // len(content_emote)
        map_y = map_y.astype(np.float32)

        height = map_y[-1, 0] + 1
        width = map_x[0, -1] + 1

        gaussian_pdf = lambda x, mu, std: np.exp(-np.square((x-mu)/std))
        map_exp = gaussian_pdf(map_y, mu=width*5//12, std=width//4)
        remap_x = map_x - width // 2 * map_exp + width // 6

        magic_emote = cv.remap(content_emote, remap_x, map_y, cv.INTER_LINEAR)

        cv.imwrite(filename, magic_emote)
        return filename