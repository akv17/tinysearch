import re

from .abstract import IPreprocessor


class IdentityPreprocessor(IPreprocessor):

    def run(self, text):
        return text


class AlphanumericPreprocessor(IPreprocessor):
    REGEXP = re.compile(r'\W', flags=re.DOTALL)

    def run(self, text):
        tokens = text.split()
        tokens = [self.REGEXP.sub('', t).lower().strip() for t in tokens]
        text = ' '.join(t for t in tokens)
        return text
