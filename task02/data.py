"""Here is the implementation of stuff related to data processing for ML."""

import gzip
import logging
import os
import shutil
import urllib.request as web

__all__ = ["maybe_mkdir", "maybe_download_and_extract"]

logger = logging.getLogger(__name__)


def maybe_mkdir(dir_name):
    """ Creates seq of dirs.

    :param dir_name: dir to create
    :type dir_name: str
    :return: flag if we actually make something
    :rtype: bool
    """

    # Split dir name into head and tail parts.
    dir_name = dir_name.strip()
    dir_name = dir_name + "/" if dir_name[-1] != '/' else dir_name
    name_head, name_tail = dir_name.split("/", 1)

    # Create head dir if absent.
    do_mk = False
    if not os.path.exists(name_head):
        os.mkdir(name_head)
        logger.info("Make dir \"%s\".", name_head)
        do_mk = True

    # Procced to tail part.
    if len(name_tail):
        os.chdir(name_head)
        logger.info("Chdir to \"%s\".", name_head)
        do_mk = do_mk or maybe_mkdir(name_tail)
        os.chdir("..")
        logger.info("Chdir to \"..\".")

    return do_mk


def maybe_download_and_extract(url, file_name=None):
    """ Do downloading and extracting file at web.

    :param url: url for file to download
    :type url: str
    :param file_name: name of file to save in
    :type file_name: str
    :return: flag if we actually download something
    :rtype: bool
    """

    # Retriving file names or use the one passed in args.
    url_file_name = url.split("/")[-1]
    do_extract = url_file_name[-3:] == ".gz" and len(url_file_name) > 3
    file_name = file_name or \
                (url_file_name[:-3] if do_extract else url_file_name)

    # If file already exists, then do nothing.
    if os.path.exists(file_name):
        return False

    # Creating dirs to file.
    file_name_dirs = file_name.rsplit("/", 1)[0]
    if len(file_name_dirs) and file_name_dirs != file_name:
        maybe_mkdir(file_name_dirs)

    # Retrive file from web and store its content at file_name.
    with web.urlopen(url) as response, open(url_file_name, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
        logger.info("Download file \"%s\" from \"%s\".", url_file_name, url)

    # Do the extracting.
    if do_extract:
        with gzip.open(url_file_name, "rb") as gz_file, \
                open(file_name, "wb") as out_file:
            shutil.copyfileobj(gz_file, out_file)
            logger.info("Extract file \"%s\" to \"%s\".",
                        url_file_name, file_name)
            os.remove(url_file_name)

    return True
