from typing import List, Optional, Union
from .tokenizer import Tokenizer
from .text_preprocessor import TextPreprocessor


class WordTokenizer(Tokenizer):
    def __init__(self, corpus: Optional[Union[List[str], str]] = None):
        super().__init__(corpus)
        self.word_tokens = {}

    def train(self, *args, **kwargs) -> None:
        i = 0
        for sent in self.corpus:
            for word in sent.split():
                if word not in self.word_tokens.keys():
                    self.word_tokens[word] = i
                    i += 1

    def tokenize(
        self,
        text: Union[List[str], str],
        padding: bool = False,
        max_length: Optional[int] = None,
    ) -> List[List[Optional[Union[int, str]]]]:
        text = TextPreprocessor.preprocess(text)
        tokenized_text = []

        for sent in text:
            tokenized_sent = []
            for word in sent.split():
                if word in self.word_tokens.keys():
                    tokenized_sent.append(self.word_tokens[word])
                else:
                    tokenized_sent.append("[UNK]")
            tokenized_text.append(tokenized_sent)

        if padding:
            max_len = max(len(sent) for sent in tokenized_text)
            for i in range(len(tokenized_text)):
                tokenized_text[i].extend([0] * (max_len - len(tokenized_text[i])))

        if max_length:
            for i in range(len(tokenized_text)):
                tokenized_text[i] = tokenized_text[i][:max_length]

        return tokenized_text
