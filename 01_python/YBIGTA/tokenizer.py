from typing import List, Optional, Union
from .text_preprocessor import TextPreprocessor


class Tokenizer:
    def __init__(self, corpus: Optional[Union[List[str], str]] = None):
        self.corpus = TextPreprocessor.preprocess(corpus)

    def add_corpus(self, corpus: Union[List[str], str]) -> None:
        self.corpus.extend(TextPreprocessor.preprocess(corpus))

    def tokenize(
        self,
        text: Union[List[str], str],
        padding: bool = False,
        max_length: Optional[int] = None,
    ) -> Union[List[List[int]], List[int]]:
        text = TextPreprocessor.preprocess(text)

    def __call__(self, text, padding, max_length) -> Union[List[List[int]], List[int]]:
        return self.tokenize(text, padding, max_length)
