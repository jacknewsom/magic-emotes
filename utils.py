from config import EMOTE_DIRECTORY, FILE_EXTENSION, SUPPORTED_CONTENT_EMOTES, SUPPORTED_STYLE_EMOTES
from styles import supported_styles
import os

def magic_emote_filename(content, style):
    return f'{EMOTE_DIRECTORY}{content}+{style}.{FILE_EXTENSION}'

def have_created_emote(content, style):
    filename = magic_emote_filename(content, style)
    return filename in os.listdir(EMOTE_DIRECTORY)

def magic_emote_supported(content, style):
    if style not in supported_styles:
        return False
    style = supported_styles[style]()
    if not style.content_is_supported(content):
        return False
    return True

def create_emote(filename, content, style):
    style = supported_styles[style]()
    style.get_magic_emote(content, filename)

def get_magic_emote_filename(content, style):
    '''Returns path to image for magic emote `content`+`style`

    args:
        content: string representing desired content emote
        style: string representing desired style emote

    return:
        filename: path to magic emote `content`+`style`
    '''
    if not magic_emote_supported(content, style):
        raise ValueError(f'Magic emote {content}+{style} is not supported')

    filename = magic_emote_filename(content, style)
    if not have_created_emote(content, style):
        # dispatch emote creator
        create_emote(filename, content, style)
        
    return filename