import re

from .abstract import IPreprocessor


class IdentityPreprocessor(IPreprocessor):

    def run(self, text):
        return text


class AlphanumericPreprocessor(IPreprocessor):
    REGEXP = re.compile(r'\W', flags=re.DOTALL)

    def run(self, text):
        text = self.REGEXP.sub('', text).lower().strip()
        return text
