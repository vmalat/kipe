class Lang():
    ltext = {}
    ltext['en'] = {}
    ltext['cz'] = {}
    choice = 'en'
        
    @staticmethod
    def add(language, ident, text):
        Lang.ltext[language][ident] = text

    @staticmethod
    def setLang(lang):
        if lang in Lang.ltext:
            Lang.choice = lang

    @staticmethod
    def get(ident):

        if ident in Lang.ltext[Lang.choice]:
            return Lang.ltext[Lang.choice][ident]
        else:
            supported = Lang.ltext
            for ii in supported:
                if ident in Lang.ltext[ii]:
                    ret = Lang.ltext[ii][ident]
                    return ret
            return '<!!! no text defined for %s>!!!'%ident
        