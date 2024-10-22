import re
from const import TO_REMOVE


class Cleaner:

    @classmethod
    def clean(cls, lines: list[str]) -> list[str]:
        retval = list()
        for line in lines:
            cleaned = cls.remove_html_tags(line)
            if len(cleaned) == 0:
                continue
            cleaned = cls.remove_bullets(cleaned)
            if len(cleaned) == 0:
                continue
            cleaned = cls.remove_urls(cleaned)
            if len(cleaned) == 0:
                continue
            cleaned = cls.remove_inline(cleaned)
            if len(cleaned) == 0:
                continue
            cleaned = cls.remove_short_lines(cleaned)
            if len(cleaned) == 0:
                continue
            retval.append(cleaned)
        return retval

    @staticmethod
    def remove_html_tags(line: str) -> str:
        line = line.strip()
        cleaned = re.sub(r"<.*?>", "", line).strip()
        if len(cleaned) < len(line):
            return cleaned
        return line

    @staticmethod
    def remove_bullets(line: str) -> str:
        line = line.strip()
        # remove non-alphanumeric character at the beginning
        cleaned = re.sub(r"^\W+", "", line).strip()
        if len(cleaned) < len(line):
            return cleaned
        # remove number followed by dot
        cleaned = re.sub(r"^\d+\.", "", line).strip()
        if len(cleaned) < len(line):
            return cleaned
        # remove number followed by closing bracket
        # remove alpha character followed by dot
        # remove alpha character followed by closing bracket
        return line

    @staticmethod
    def remove_urls(line: str) -> str:
        line = line.strip()
        cleaned = re.sub(r"http\S+", "", line).strip()
        if len(cleaned) < len(line):
            return cleaned
        return line

    @staticmethod
    def remove_short_lines(line: str) -> str:
        test = line.split()
        if len(test) < 4:
            return ""
        return line

    @staticmethod
    def remove_inline(line: str) -> str:
        line = line.strip()
        for pattern in TO_REMOVE:
            cleaned = re.sub(pattern, "", line).strip()
            if len(cleaned) < len(line):
                return cleaned
        return line
