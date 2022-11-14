import re

from ..interface import IPreprocessor


class Preprocessor(IPreprocessor):
    """
    Приводит строку в нижний регистр и удаляет всю пунктуацию
    """

    REGEXP = re.compile(r'\W', flags=re.DOTALL)

    def run(self, text):
        """
        Преобразует текст
        :param text: текст
        :return:
        """
        tokens = text.split()
        tokens = [self.REGEXP.sub('', t).lower().strip() for t in tokens]
        tokens = [t for t in tokens if t]
        text = ' '.join(tokens)
        return text
