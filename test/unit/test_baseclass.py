import pytest

from mercury.lib import BaseClass


class TestBaseClass():
    def test_subclass_instantiation(self):
        class SubClass(BaseClass):
            def __init__(self, arg1: str, *, arg2: bool):
                self.arg1 = arg1
                self.arg2 = arg2

        test_class = SubClass("foo", arg2=True)
        class_copy = eval(repr(test_class))
        assert class_copy.arg1 == test_class.arg1
        assert class_copy.arg2 == test_class.arg2

    # def test_complex_subclass_instantiation(self):
    #     class SubClass(BaseClass):
    #         def __init__(self, arg1: str, *, arg2: bool):
    #             self.arg3 = arg1
    #             self.arg4 = arg2

    #     test_class = SubClass("foo", arg2=True)
    #     class_copy = eval(repr(test_class))
    #     assert class_copy.arg3 == "foo"
    #     assert class_copy.arg4 is True
