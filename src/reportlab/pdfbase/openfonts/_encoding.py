# Font encoding for OpenType fonts
# Extracted from ttfonts.py for the openfonts package.


class FontEncoding:
    """Encoding for OpenType fonts (always UTF-8).

    FontEncoding does not directly participate in PDF object creation, since
    we need a number of different 8-bit encodings for every generated font
    subset.  OpenTypeFont itself cares about that."""

    def __init__(self):
        self.name = "UTF-8"
