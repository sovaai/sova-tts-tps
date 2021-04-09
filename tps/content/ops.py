import os
import sys
import hashlib
from urllib.request import urlopen
from math import ceil

from loguru import logger
from tqdm import tqdm
from nltk.internals import is_writable


path_list = []

_paths_from_env = os.environ.get("TPS_DATA", str("")).split(os.pathsep)
path_list += [d for d in _paths_from_env if d]

if sys.platform.startswith("win"):
    # Common locations on Windows:
    path_list += [
        os.path.join(os.environ.get(str("APPDATA"), str("C:\\")), str("tps_data"))
    ]
else:
    # Common locations on UNIX & OS X:
    path_list += [
        str("/usr/share/tps_data"),
        str("/usr/local/share/tps_data"),
        str("/usr/lib/tps_data"),
        str("/usr/local/lib/tps_data"),
    ]

_content_info = {
    "stress.dict": ("http://dataset.sova.ai/SOVA-TTS/tps_data/stress.dict", "99aedabdfe82d5bf9c2d428b498221a1"),
    "yo.dict": ("http://dataset.sova.ai/SOVA-TTS/tps_data/yo.dict", "22704929ffd1f8bf3a4e0d9cce0cdb5f"),
    "e.dict": ("http://dataset.sova.ai/SOVA-TTS/tps_data/e.dict", "3b1aa9ac0e79f6322ece7c4834fecab9")
}


def calc_checksum(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_checksum(name):
    try:
        _, checksum = _content_info[name]
        return checksum
    except KeyError:
        logger.warning("There is no file named {} in content dictionary, None will be returned. Possible names: {}".
                       format(name, list(_content_info.keys())))
        return


def find(name, data_dir=None, raise_exception=False, checksum=None):
    """
    Performs searching for a 'name' file.

    :param name: str
        Name of the file that needs to be found.
    :param data_dir: Optional[str]
        If provided, it's appended to a list of paths to be searched.
    :param raise_exception: bool
        If True and no file is found a FileNotFoundError exception will be raised.

    :return: Optional[str]
        Returns path to the file, if file was found. Returns None, if no file was found
        and raise_exception == False.
    """
    data_dir = [] if data_dir is None else [data_dir]
    _path_list = data_dir + [os.path.join(os.path.expanduser('~'), '.tps')] + path_list

    for path in _path_list:
        filepath = os.path.join(path, name)
        if os.path.exists(filepath):
            if checksum is None:
                return filepath
            elif calc_checksum(filepath) == checksum:
                return filepath
            else:
                logger.warning("File named {} exists, but its checksum is not correct. Try ro redownload it.".
                               format(name))
                return

    msg = "There is no file named {file} in any data directory, " \
          "try to download it: tps.download('{file}')".format(file=name)

    if raise_exception:
        raise FileNotFoundError(msg)
    else:
        logger.warning(msg)

    return


def download(name, destination=None, chunksize=4096, force=False):
    """
    Checks if there is an actual version of the specified file on the device,
    and if not, downloads it from servers.
    Files, theirs checksums and links to them must be specified
    in the tps.downloader._content dictionary.

    :param name: str
        Name of the file.
    :param destination: Optional[str]
        See get_download_dir:data_dir
    :param chunksize: int
        What chunksize is used while downloading the file.

    :return: str
        Path to the file.
    """

    try:
        url, checksum = _content_info[name]
    except KeyError:
        logger.warning("There is no file named {} in content dictionary, None will be returned. Possible names: {}".
                       format(name, list(_content_info.keys())))
        return

    if not force:
        filepath = find(name, destination, False, checksum)
        if filepath is not None:
            return filepath

    destination = get_download_dir(destination)
    if destination is None:
        logger.warning("Can not download file due to access permissions.")
        return

    filepath = os.path.join(destination, name)
    if os.path.exists(filepath) and checksum == calc_checksum(filepath):
        logger.info("The actual version of the file is already downloaded and can be found along the path: {}"
              .format(filepath))
        return filepath

    try:
        infile = urlopen(url)
        length = infile.length
        chunk_n = ceil(length / chunksize)

        with open(filepath, "wb") as outfile:
            for _ in tqdm(range(chunk_n)):
                chunk = infile.read(chunksize)
                outfile.write(chunk)

                if not chunk:
                    break
        infile.close()
    except IOError as e:
        logger.error("Error downloading {} from {}:\n{}".format(name, url, e))
        return

    return filepath


def get_download_dir(data_dir=None):
    """
    Checks which directory is writeable and returns path to it.
    Firstly checks data_dir, secondly user's home directory and only after that
    checks other OS dependent directories listed in tps.data.path_cfg.path_list

    :param data_dir: Optional[str]
        If specified, it is considered as the first folder that needs to be checked.

    :return: Optional[str]
    """
    if data_dir is not None:
        try:
            os.makedirs(data_dir, exist_ok=True)
        except OSError:
            pass

        if not is_writable(data_dir):
            logger.warning("Permission denied: it's not possible to write in {} folder. Checking other defaults...".
                           format(data_dir))
    else:
        data_dir = os.path.join(os.path.expanduser('~'), '.tps')
        try:
            os.makedirs(data_dir, exist_ok=True)
        except OSError:
            pass

        if not is_writable(data_dir):
            logger.warning("Permission denied: it's not possible to write in {} folder. Checking other defaults...".
                           format(data_dir))

            for _data_dir in path_list:
                if os.path.exists(_data_dir) and is_writable(_data_dir):
                    return _data_dir

            logger.warning("Can not get access to any data directory. Try to check permissions.")
            return

    return data_dir