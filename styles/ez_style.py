from .base_style import BaseStyle
import numpy as np
import cv2 as cv
import json
import os

class EZStyle(BaseStyle):
    ez_glasses_filename = '/home/jack/project/meserver/styles/ez_glasses.png'
    ez_glasses_eyes = np.array([[540, 560], [540, 1430]])

    delta_ez = ez_glasses_eyes[1] - ez_glasses_eyes[0]
    theta_ez = np.arctan2(delta_ez[0], delta_ez[1])
    length_ez = np.sqrt(np.sum(np.square(delta_ez)))

    def __init__(self, metadata_dir='/home/jack/project/meserver/metadata/'):
        super(EZStyle, self).__init__()
        if metadata_dir[-1] != '/':
            metadata_dir += '/'

        self.metadata_dir = metadata_dir

    def content_is_supported(self, content):
        '''Content emote is supported if we know where its eyes are. Otherwise, we can't put glasses on it
        '''
        filename = self.metadata_dir + f'{content}/data.json'
        if not os.path.isfile(filename):
            # need to at least have a metadata file for emote
            return False

        with open(filename) as f:
            metadata = json.load(f)
        if 'eyes' not in metadata:
            return False
        
        eyes = metadata['eyes']
        # make sure we have at least two eyes
        if len(eyes) < 2:
            return False
        for eye in eyes:
            # each eye should look like [x, y] for int x, y
            if type(eye) != list:
                return False
            elif len(eye) != 2:
                return False
            elif type(eye[0]) != int or type(eye[1]) != int:
                return False
        return True

    def get_magic_emote(self, content, filename):
        '''We stretch EZ glasses to be as wide as eyes are, then add EZ glasses on top of content
        '''
        if not self.content_is_supported(content):
            raise NotImplementedError(f'{content} is not supported for this style')
        
        metadata_filename = self.metadata_dir + f'{content}/data.json'
        with open(metadata_filename) as f:
            metadata = json.load(f)
            eyes = metadata['eyes']
            eyes = np.array(eyes)
        left_eye, right_eye = eyes
        delta_content = right_eye - left_eye
        theta_content = np.arctan2(delta_content[0], delta_content[1])
        length_content = np.sqrt(np.sum(np.square(delta_content)))

        center = (0, 0)
        theta = theta_content - self.theta_ez
        scale = length_content / self.length_ez
        rotation_matrix = cv.getRotationMatrix2D(center, theta, scale)

        content_emote = cv.imread(self.metadata_dir+f'{content}/src.png', cv.IMREAD_UNCHANGED)

        ez_glasses = cv.imread(self.ez_glasses_filename, cv.IMREAD_UNCHANGED)
        ez_glasses = cv.warpAffine(ez_glasses, rotation_matrix, (ez_glasses.shape[1], ez_glasses.shape[0]))

        rescaled_ez_eyes = (self.ez_glasses_eyes @ rotation_matrix[:, :-1]) + rotation_matrix[:, -1]
        rescaled_ez_eyes = rescaled_ez_eyes.astype(np.int)

        ez_shift = eyes-rescaled_ez_eyes
        ez_shift = np.flip(ez_shift[0]).reshape(-1, 1)
        translation_matrix = np.hstack((np.eye(2), ez_shift))

        ez_glasses = cv.warpAffine(ez_glasses, translation_matrix, (content_emote.shape[1], content_emote.shape[0]))

        mask = ez_glasses[:, :, -1:] / 255.
        top_layer = ez_glasses[:, :, :-1]

        magic_emote = np.copy(content_emote)
        magic_emote[:, :, :-1] = (1. - mask) * magic_emote[:, :, :-1] + mask * top_layer

        cv.imwrite(filename, magic_emote)
        return filename