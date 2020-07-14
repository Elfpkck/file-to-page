"""Project constants. Some may be taken from a environment variables."""

import os

from pathlib import Path

FILE_ABSPATH_STR = os.environ.get('FILE_PATH_STR')
FILE_PATH = Path(FILE_ABSPATH_STR or Path(__file__).parent / 'file_storage')
FILE_NUMBER = len(list(FILE_PATH.glob('*')))
FILE_DEFAULT = os.environ.get('FILE_DEFAULT') or 'file1.txt'

URL_QUERY_START = os.environ.get('QUERY_START', 'start')
URL_QUERY_STOP = os.environ.get('QUERY_STOP', 'stop')

WEB_SERVER_DEBUG = os.environ.get('WEB_SERVER_DEBUG', False)
