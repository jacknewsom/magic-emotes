class BaseStyle:
    def content_is_supported(self, content):
        '''Whether or not content emote `content` is supported for this style emote
        '''
        raise NotImplementedError

    def get_magic_emote(self, content, filename):
        '''Return magic emote corresponding to self applied to `content` if 
        `self.content_is_supported(content)` is True
        '''
        raise NotImplementedError