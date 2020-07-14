"""Business logic. Implements HTML prettifiers."""

from codecs import (BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE,
                    BOM_UTF8)
from functools import lru_cache
from typing import List, Optional, Tuple

import const

BomsT = Tuple[Tuple[bytes, str], ...]


class PrettyHTML:
    """Responsible for accurately converting an HTML file to an HTML string."""
    DEFAULT_ENCODING = 'UTF-8'
    BOMS: 'BomsT' = (
        (BOM_UTF8, 'UTF-8'),
        (BOM_UTF32_BE, 'UTF-32-BE'),
        (BOM_UTF32_LE, 'UTF-32-LE'),
        (BOM_UTF16_BE, 'UTF-16-BE'),
        (BOM_UTF16_LE, 'UTF-16-LE'),
    )

    def get_html(self,
                 file_path: str,
                 start: Optional[int] = None,
                 stop: Optional[int] = None) -> str:
        """In accordance with the encoding of the contents of the file,
        prettifies it.

        :param file_path: a path to a file
        :param start: slice start line
        :param stop: slice end line
        :return: prettified content of the file
        """
        return '<br />\n'.join(self._get_file_lines(file_path)[start:stop])

    @lru_cache(maxsize=const.FILE_NUMBER)
    def _get_file_lines(self, file_path: str) -> List[str]:
        with open(file_path, 'rb') as f:
            file_content = f.read()
            encoding = (self.get_encoding(file_content, self.BOMS) or
                        self.DEFAULT_ENCODING)
            return str(file_content, encoding=encoding).split('\n')

    @staticmethod
    def get_encoding(data: bytes, boms: 'BomsT') -> Optional[str]:
        """Defines an encoding of the data.

        :param data: data with the unknown encoding (at least the beginning)
        :param boms: markers of the encodings
        :return: found encoding or None
        """
        for bom, encoding in boms:
            if data.startswith(bom):
                return encoding
