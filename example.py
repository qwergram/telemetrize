
class ExampleClass:

    def __init__(self, arg: int, sumn: str, *args, **kwargs):
        self.arg = arg
        self.sumn = sumn
        self.args = args
        self.kwargs = kwargs

    def method1(self, arg2: int = 45):
        return self.arg + arg2

    @property
    def some_method(self):
        return sumn

from telemetrize import telemetrize

@telemetrize
def add(a, b):
    return a + b



