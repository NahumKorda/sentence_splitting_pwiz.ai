from const import SENTENCE_BREAKERS


class Splitter:

    def __init__(self, sentence_breakers: set[str] | None = None):
        self.__breakers: set[str] = SENTENCE_BREAKERS
        if sentence_breakers is not None:
            self.__breakers.update(sentence_breakers)

    def split(self, text: str) -> list[str] | None:
        if not isinstance(text, str):
            return None
        splits = text.split("\n")
        for breaker in self.__breakers:
            breaker += " "
            splits = self.__split(splits, breaker)
        return splits

    @staticmethod
    def __split(splits: list[str], split_break: str):
        retval = list()
        for split in splits:
            split = split.strip()
            if len(split) == 0:
                continue
            temp = split.split(split_break)
            if len(temp) == 1:
                # No split occurred
                retval.extend(temp)
            else:
                # Ensure that the punctuation is preserved.
                temp = [part if part.endswith(split_break.strip()) else part + split_break.strip() for part in temp]
                retval.extend(temp)
        return retval
