import re
from typing import List, Optional, Union
from .tokenizer import Tokenizer
from .text_preprocessor import TextPreprocessor


class BPETokenizer(Tokenizer):
    def __init__(self, corpus: Optional[Union[List[str], str]] = None):
        super().__init__(corpus)

        self.word_freqs = {}
        self.vocab = {}
        self.alphabet = []
        self.splits = {}

    def compute_word_freqs(self) -> None:
        for sent in self.corpus:
            for word in sent.split():
                if word in self.word_freqs:
                    self.word_freqs[word] += 1
                else:
                    self.word_freqs[word] = 1

        for word in self.word_freqs.keys():
            for letter in word:
                if letter not in self.alphabet:
                    self.alphabet.append(letter)

        self.splits = {word: [c for c in word] for word in self.word_freqs.keys()}

    def get_stats(self) -> None:
        for word, freq in self.word_freqs.items():
            split = self.splits[word]

            for i in range(len(split) - 1):
                pair = (split[i], split[i + 1])

                if pair in self.vocab:
                    self.vocab[pair] += freq
                else:
                    self.vocab[pair] = freq

    def merge_vocab(self, pair: tuple[str, str]) -> None:
        for word in self.word_freqs.keys():
            split = self.splits[word]
            i = 0

            while i < len(split) - 2:
                if split[i] == pair[0] and split[i + 1] == pair[1]:
                    if i == 0:
                        if pair in self.vocab.keys():
                            self.vocab[pair] += self.word_freqs[word]
                        else:
                            self.vocab[pair] = self.word_freqs[word]
                        self.vocab[(split[i + 1], split[i + 2])] -= self.word_freqs[word]
                        split = [[pair[0] + pair[1]], split[i + 2 :]]

                    elif i > 0 and i < len(split) - 2:
                        if pair in self.vocab.keys():
                            self.vocab[pair] += self.word_freqs[word]
                        else:
                            self.vocab[pair] = self.word_freqs[word]
                        self.vocab[(split[i - 1], split[i])] -= self.word_freqs[word]
                        self.vocab[(split[i + 1], split[i + 2])] -= self.word_freqs[word]
                        split = [split[:i], [pair[0] + pair[1]], split[i + 2 :]]

                    else:
                        if pair in self.vocab.keys():
                            self.vocab[pair] += self.word_freqs[word]
                        else:
                            self.vocab[pair] = self.word_freqs[word]
                        self.vocab[(split[i - 1], split[i])] -= self.word_freqs[word]
                        split = [split[:i], pair[0] + pair[1]]
                else:
                    i += 1

            self.splits[word] = split

    def train(self, n_iter: int) -> None:
        self.compute_word_freqs()
        self.get_stats()

        for _ in range(n_iter):
            if not self.vocab:
                break

            max_freq = max(self.vocab.values())
            best = [k for k, v in self.vocab.items() if v == max_freq]
            self.merge_vocab((best[0][0], best[0][1]))
            self.alphabet.append(best[0][0] + best[0][1])

    def find_token(self, raw_word: str) -> tuple[str, str]:
        for token in reversed(self.alphabet):
            if token in raw_word:
                new_tok = token
                sub_tok = raw_word - token
                return new_tok, sub_tok

    def token_id(self, token: str) -> int:
        return self.alphabet.index(token) + 1

    def tokenize(
        self,
        text: Union[List[str], str],
        padding: bool = False,
        max_length: Optional[int] = None,
    ) -> List[List[int]]:
        text = TextPreprocessor.preprocess(text)
        tokenized_text = []

        for sent in text:
            tokenized_sent = []

            for word in sent.split():
                if word in self.splits.keys():
                    for token in len(self.splits[word]):
                        tokenized_sent.append(self.token_id(token))
                else:
                    while word == "":
                        new_token, new_word = self.find_token(word)
                        word = new_word
                        tokenized_sent.append(self.token_id(new_token))

            tokenized_text.append(tokenized_sent)

        if padding:
            max_len = max(len(sent) for sent in tokenized_text)
            for i in range(len(tokenized_text)):
                tokenized_text[i].extend([0] * (max_len - len(tokenized_text[i])))

        if max_length:
            for i in range(len(tokenized_text)):
                tokenized_text[i] = tokenized_text[i][:max_length]

        return tokenized_text
