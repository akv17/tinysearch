from abc import ABC, abstractmethod


class IPreprocessor:

    @abstractmethod
    def run(self, text): pass
