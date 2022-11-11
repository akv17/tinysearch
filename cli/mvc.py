import time


class Model:

    def __init__(self, engine, k=5):
        self.engine = engine
        self.k = k

    def run(self, text):
        start = time.perf_counter()
        scores = self.engine.search(text=text, k=self.k)
        runtime = time.perf_counter() - start
        scores = [s for s in scores if s.score > 0]
        return scores, runtime


class View:

    def __init__(self, corpus, text_size=80):
        self.corpus = corpus
        self.text_size = text_size

    def run(self, scores, runtime):
        if not scores:
            print('\tNothing found...')
            return
        for i, score in enumerate(scores):
            doc = self.corpus[score.id]
            text = doc.text
            text_too_long = len(text) > self.text_size
            text = text[:self.text_size]
            text = text + '...' if text_too_long else text
            print(f'\t{i+1}. {repr(text)} [{score.score:.2f}]')
        print(f'time: {runtime:.4f} s.')


class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self._on_start()
        while True:
            query = self._prompt()
            if query is None:
                break
            scores, runtime = self.model.run(query)
            self.view.run(scores=scores, runtime=runtime)
        self._on_end()

    def _on_start(self):
        print('-> Interactive CLI session started.')
        print('-> Type query or \'q!\' to exit.')

    def _on_end(self):
        print('-> Exit.')

    def _prompt(self):
        text = input('---> ')
        text = text.strip()
        text = text if text != 'q!' else None
        return text


class Factory:

    def __init__(self, api, k=5):
        self.api = api
        self.k = k

    def create(self):
        model = Model(self.api.engine, k=self.k)
        view = View(self.api.corpus)
        controller = Controller(model=model, view=view)
        return controller
