
class TranslatedPath:
    """Takes a raw path and breaks it into parts

    Attributes
    ----------
    path : str
        the explicit path of the resource
    queries : dict
        queries in {key:value} form if present
    anchor : str
        any anchor defined by #
    parts : list[str]
        a breakdown of the pieces of the path, top dir first
    topdir : str
        the top directory in the path
    resource : str
        the file or directory the path locates
    file
        a byte-like object loaded from file path

    """
    def __init__(self, raw: str):

        # remove root reference and don't deal with directory requests
        if raw.startswith('/'):
            raw = raw[1:]

        if raw.endswith('/'):
            raw = raw[:-1]

        self.path = raw
        self.queries = None
        self.anchor = None

        self._file = None

        queries = None
        if '?' in self.path:
            self.path, queries = raw.split('?', 1)
        if '#' in self.path:
            self.path, self.anchor = self.path.split('#', 1)

        if queries:
            self.queries = dict(x.split('=') for x in queries.split('&'))  # python is magical

        _path = self.path
        if _path.startswith('/'):
            _path = _path[1:]

        self.parts = _path.split('/')

    def update(self, path: str):
        if path.endswith('/'):
            path = path[:-1]

        self.path = path

        if path.startswith('/'):
            path = path[1:]

        self.parts = path.split('/')

    def __iadd__(self, other: str):
        if other.startswith('.'):
            self.update(self.path + other)
        else:
            self.update('{}/{}'.format(self.path, other))
        return self

    def __getitem__(self, item):
        return self.parts[item]

    def __len__(self):
        return len(self.parts)

    def __iter__(self):
        return self.parts.__iter__()

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.__str__()

    @property
    def topdir(self) -> str:
        """The first directory (or file) in the path"""
        return self.parts[0]

    @property
    def resource(self) -> str:
        """The file (or directory) the path locates"""
        return self.parts[-1]

    def get(self):
        try:
            return open(self.path, 'rb')
        except:
            return False

    def exists(self):
        return bool(self.get())

    @property
    def filename(self):
        return self.resource.split('.')[0]

    @property
    def filetype(self):
        if '.' in self.resource:
            return self.resource.split('.')[1]
        else:
            return 'html'

    @property
    def file(self):
        if not self._file:
            _file = self.get()
        return self._file

