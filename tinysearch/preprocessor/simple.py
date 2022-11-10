import re


class Preprocessor:
    REGEXP = re.compile(r'\W', flags=re.DOTALL)

    def run(self, text):
        tokens = text.split()
        tokens = [self.REGEXP.sub('', t).lower().strip() for t in tokens]
        tokens = [t for t in tokens if t]
        text = ' '.join(tokens)
        return text