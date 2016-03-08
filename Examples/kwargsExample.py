class kwargsExample:

    def __init__(self, **kwargs):
        self.arg1 = kwargs.get("arg1", "no arg1 passed")
        self.arg2 = kwargs.get("arg2", "no arg2 passed")
        self._arg3 = kwargs.get("arg3", "no arg3 passed")

    @property
    def arg1(self):
        return self._arg1

    @property
    def arg2(self):
        return self._arg2

    @property
    def arg3(self):
        return self._arg3

test1 = kwargsExample(arg1="1", arg2="two")
print test1.arg1, test1.arg2, test1.arg3

dict = {"arg1": "one", "arg3": 3, "arg2": "something"}
test2 = kwargsExample(**dict)
print test2.arg1, test2.arg2, test2.arg3