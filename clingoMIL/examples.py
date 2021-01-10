import clingo


class Examples:
    def __init__(self):
        self.examples = []

    def _add_load(self, add=None, load=None):
        if add is None and load is None:
            return

        control = clingo.Control()
        if add is not None:
            control.add("base", [], add)
        if load is not None:
            control.load(load)
        control.ground([("base", [])])

        model = []
        result = control.solve(on_model=lambda m: model.extend(m.symbols(shown=True)))

        if not result.satisfiable:
            raise RuntimeError("added or loaded examples were unsatisfiable")

        self._extend_examples(model)

    def _extend_examples(self, model):
        for symbol in model:
            if symbol.match("pos_ex", 3) or symbol.match("neg_ex", 3):
                self.examples.append(symbol)

    def add(self, program):
        self._add_load(add=program)
        return self

    def load(self, filename):
        self._add_load(load=filename)
        return self

    def __iter__(self):
        yield from self.examples

    def positive(self):
        for example in self.examples:
            if example.match("pos_ex", 3):
                yield example

    def negative(self):
        for example in self.examples:
            if example.match("neg_ex", 3):
                yield example
