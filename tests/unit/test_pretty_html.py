"""Web application's tests. PEP-8 is violated for better reading."""

from codecs import (BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE,
                    BOM_UTF8)
from io import BytesIO
from textwrap import dedent
from typing import Optional, TYPE_CHECKING, Tuple
from unittest.mock import mock_open, patch

import pytest

from file_to_page.pretty_html import PrettyHTML

if TYPE_CHECKING:
    from file_to_page.pretty_html import BomsT

READ_DATA_DIRTY = '''
    \ufeff<h2> 1. “咏鹅 (YǑNG É)” – AN ODE TO THE GOOSE </h2>

    <i>“An Ode to the Goose” is a short poem from the Tang Dynasty, and is often the first poem that Chinese children are taught due to its simplicity. </i>

    It was written during the Tang Dynasty by child prodigy poet 骆宾王 (Luò bīn wáng), who penned this poem when he was only seven years old. 骆宾王 would go on to become one of the most famous poets of the Tang Dynasty, and later served as a secretary of the country government of Chang’an.

    鹅、鹅、鹅，
    (é é é)
    '''
READ_DATA = bytes(dedent(READ_DATA_DIRTY).strip(), encoding='UTF-16-LE')
EXPECTED_FULL = dedent('''
    \ufeff<h2> 1. “咏鹅 (YǑNG É)” – AN ODE TO THE GOOSE </h2><br />
    <br />
    <i>“An Ode to the Goose” is a short poem from the Tang Dynasty, and is often the first poem that Chinese children are taught due to its simplicity. </i><br />
    <br />
    It was written during the Tang Dynasty by child prodigy poet 骆宾王 (Luò bīn wáng), who penned this poem when he was only seven years old. 骆宾王 would go on to become one of the most famous poets of the Tang Dynasty, and later served as a secretary of the country government of Chang’an.<br />
    <br />
    鹅、鹅、鹅，<br />
    (é é é)
    ''').strip()


@pytest.fixture(scope='module')
def pretty_html() -> 'PrettyHTML':
    return PrettyHTML()


@pytest.mark.parametrize(
    argnames='read_data, expected, start, stop',
    argvalues=[
        (READ_DATA, EXPECTED_FULL, None, None),
        (READ_DATA,
         dedent('''
            It was written during the Tang Dynasty by child prodigy poet 骆宾王 (Luò bīn wáng), who penned this poem when he was only seven years old. 骆宾王 would go on to become one of the most famous poets of the Tang Dynasty, and later served as a secretary of the country government of Chang’an.<br />
            <br />
            鹅、鹅、鹅，
            ''').strip(),
         4,
         7),
    ],
    ids=[
        'without_slice',
        'with_slice',
    ],
)
def test_get_html(pretty_html: 'PrettyHTML', read_data: bytes, expected: str,
                  start: Optional[str], stop: Optional[str]):
    """open() and read() are mocked to have clean and fast unittests."""
    with patch("builtins.open", mock_open(read_data=read_data)):
        assert pretty_html.get_html('', start, stop) == expected


@pytest.fixture(scope='function')
def files() -> 'BomsT':
    """Returns files with different BOMs at the beginning."""
    return (
        (BytesIO(BOM_UTF8).read(), 'UTF-8'),
        (BytesIO(BOM_UTF32_BE).read(), 'UTF-32-BE'),
        (BytesIO(BOM_UTF32_LE).read(), 'UTF-32-LE'),
        (BytesIO(BOM_UTF16_BE).read(), 'UTF-16-BE'),
        (BytesIO(BOM_UTF16_LE).read(), 'UTF-16-LE'),
    )


def test_get_encoding(pretty_html: 'PrettyHTML',
                      files: Tuple[Tuple[bytes, str]]):
    for data, encoding in files:
        assert pretty_html.get_encoding(data, PrettyHTML.BOMS) == encoding
