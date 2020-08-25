class Dict:
    def __init__(self, filepath):
        self._entries = {}

        if filepath is not None:
            self._entries = self._load_dict(filepath)


    @staticmethod
    def _load_dict(filepath):
        raise NotImplementedError


    def __iter__(self):
        return iter(self._entries.keys())


    def __getitem__(self, item):
        return self._entries[item]


    def __len__(self):
        return len(self._entries)


    def convert_word(self, *args, **kwargs):
        raise NotImplementedError


    def convert_text(self, *args, **kwargs):
        raise NotImplementedError