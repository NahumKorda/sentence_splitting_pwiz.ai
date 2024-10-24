import re
import ftfy
import mwparserfromhell
from bs4 import BeautifulSoup
from urlextract import URLExtract
from urllib.parse import urlparse
from const import TO_REMOVE
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")


class Cleaner:

    def __init__(self):
        self.__extractor = URLExtract()

    def clean(self, lines: list[str]) -> list[str]:
        retval = list()
        for line in lines:

            # Assuming that MS Windows text was encoded using UTF-8
            # (instead of Windows-1252), so that all printable
            # characters between ASCII 127 and 255 were erroneously
            # converted, we roll back the errors to pure UTF-8.
            cleaned = self.__fix_unicode(line)

            # Text could be provided with HTML tags and HTML entities, which we remove.
            cleaned = self.__remove_html_tags(cleaned)
            if len(cleaned) == 0:
                continue

            # Text could be provided with the Wiki Markup, which we remove.
            cleaned = self.__remove_wiki_markup(cleaned)
            if len(cleaned) == 0:
                continue

            # Handle URLs
            if self.__extractor.has_urls(cleaned):
                cleaned = self.remove_urls(cleaned)
                if len(cleaned) == 0:
                    continue

            cleaned = self.__remove_bullets(cleaned)
            if len(cleaned) == 0:
                continue

            cleaned = self.remove_inline(cleaned)
            if len(cleaned) == 0:
                continue

            cleaned = self.remove_short_lines(cleaned)
            if len(cleaned) == 0:
                continue

            retval.append(cleaned)

        return retval

    @staticmethod
    def __fix_unicode(line: str) -> str:
        return ftfy.fix_text(line)

    @staticmethod
    def __remove_html_tags(line: str) -> str:
        line = line.strip()
        soup = BeautifulSoup(line, 'lxml')
        return soup.get_text()

    @staticmethod
    def __remove_wiki_markup(line: str) -> str:
        wiki_code = mwparserfromhell.parse(line)
        return wiki_code.strip_code()

    def __remove_bullets(self, line: str) -> str:
        line = self.__remove_simple_bullets(line)
        line = self.__remove_enumerated_bullets(line)
        return line

    @staticmethod
    def __remove_simple_bullets(line: str) -> str:
        line = line.strip()
        bullet_pattern = r"^[•–—*+-]"
        return re.sub(bullet_pattern, "", line)

    @staticmethod
    def __remove_enumerated_bullets(line: str) -> str:
        line = line.strip()
        bullet_pattern = r"^\s*[0-9a-zA-Z]+[.)]\s+"
        match = re.search(bullet_pattern, line)
        while match:
            line = re.sub(bullet_pattern, "", line)
            line = line.strip()
            match = re.search(bullet_pattern, line)
        return line

    def remove_urls(self, line: str) -> str:

        line = line.strip()

        # extract urls with corresponding indices
        urls = self.__extractor.find_urls(line, get_indices=True)

        retval = list()
        # Iterate from the end to preserve the indices from
        # the beginning when shortening the input text.
        for url, indices in reversed(urls):
            # URLExtract is python class for extracting URLs
            # from given text based on locating TLD retrieved
            # from IANA.org. Therefore, it could err and extract
            # snippets which are not URLs. Accordingly, extractions
            # must be verified.
            if self.__is_valid_url(url):
                start = indices[0]
                end = indices[1]
                # Temporarily preserve the end of the line that follows the rightmost URL.
                retval.append(line[end:])
                # Shorten the line to exclude the URL and everything that follows.
                line = line[:start]

        if len(line) > 0:
            retval.append(line)

        return "".join(reversed(retval)).strip()

    @staticmethod
    def __is_valid_url(url):
        try:
            result = urlparse(url)
            return True
        except:
            return False

    @staticmethod
    def remove_inline(line: str) -> str:
        line = line.strip()
        for pattern in TO_REMOVE:
            line = re.sub(re.escape(pattern), "", line, flags=re.IGNORECASE)
        return line

    @staticmethod
    def remove_short_lines(line: str) -> str:
        test = line.split()
        if len(test) < 4:
            return ""
        return line
