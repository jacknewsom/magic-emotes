from .base_style import BaseStyle
import numpy as np
import cv2 as cv
import json
import os

class PepegaStyle(BaseStyle):
    def __init__(self, metadata_dir='/home/jack/project/meserver/metadata/'):
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
        '''We apply the Pepega transform by remapping x pixels like this
            x -> width*cos(pi(y/height - 1/2))
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

        map_sin = np.sin(-np.pi*map_y / height)
        map_sin = width * ((1-map_x/width) * map_sin)
        remap_x = map_sin + map_x

        magic_emote = cv.remap(content_emote, remap_x, map_y, cv.INTER_LINEAR)

        cv.imwrite(filename, magic_emote)
        return filename