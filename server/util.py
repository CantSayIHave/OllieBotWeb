import io
import os
import time


class TranslatedPath:
    """Takes a raw path and breaks it into parts

    Supported Operations:

    +-----------+--------------------------------------+
    | Operation |             Description              |
    +===========+======================================+
    | x == y    | Checks if two paths are equal.       |
    +-----------+--------------------------------------+
    | x != y    | Checks if two paths are not equal.   |
    +-----------+--------------------------------------+
    | x += y    | Appends to a translated path         |
    +-----------+--------------------------------------+
    | str(x)    | Returns the translated path          |
    +-----------+--------------------------------------+
    | len(x)    | Returns the number of path scopes    |
    +-----------+--------------------------------------+
    | x[y]      | Returns a scope of the path          |
    +-----------+--------------------------------------+

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
    file : :class:`File`
        a `File` container for a file-like object defined by the path

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
            for q in self.queries:
                self.queries[q] = self.queries[q].replace('%20', ' ')

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
        """Returns a file-like object if it exists"""
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
        """Returns :class:`File` container for path-defined file"""
        if not self._file:
            f_obj = self.get()
            self._file = File(f_obj)
        return self._file

    @file.setter
    def file(self, thing):
        if not isinstance(thing, File):
            self._file = File(thing)
        else:
            self._file = thing

    def replace(self, old: str, new: str, count: int = -1):
        self.update(self.path.replace(old, new, count))
        return self.path


# Standardizes determination of file size
# Upon testing, `len(f.read())` is by far the fastest method
def get_file_size(buffer) -> int:
    """Find the size of a file object

    Parameters
    ----------
    buffer
        a file object

    Returns
    -------
    int
        a file size in bytes

    """
    if isinstance(buffer, (io.BytesIO, io.StringIO)):
        buffer.seek(0)
        size = len(buffer.read())
        buffer.seek(0)
        return size
    else:
        return os.path.getsize(buffer.fileno())


def get_file_time(buffer) -> int:
    """Find the modify time of a file object

    Parameters
    ----------
    buffer
        a file object

    Returns
    -------
    int
        a file 'last modified' time in seconds

    """
    if isinstance(buffer, (io.BytesIO, io.StringIO)):
        return int(time.time())
    else:
        return os.path.getmtime(buffer.fileno())


class File:
    def __init__(self, buffer, size=0, _time=0, name='', type=''):
        self.buffer = buffer
        self.size = size
        self.time = _time
        self.name = name
        self.type = type
        # and more

        if not name:
            try:
                self.name = buffer.name
            except:
                self.name = 'file'  # creative!

        if not size:
            self.size = get_file_size(buffer)

        if not _time:
            self.time = int(time.time())

        if not type and '.' in self.name:
            self.type = self.name.rsplit('.', 1)[-1]

    def __str__(self):
        return 'File(buffer={}, size={}, time={}, name={})'.format(self.buffer, self.size, self.time, self.name)

    def __repr__(self):
        return self.__str__()

    def get(self):
        return self.buffer

    def __bytes__(self):
        return self.buffer
