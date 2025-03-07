class TestObject:
    """
    A test class that takes an integer, a string, a bool, a list, a dictionary, a name, and another class object as parameters.
    All parameters are converted to instance variables.
    """

    def __init__(self, integer, string, boolean, list_param, dict_param, name, class_object):
        self._id = name
        self.integer = integer
        self.string = string
        self.boolean = boolean
        self.list_param = list_param
        self.dict_param = dict_param
        self.class_object = class_object


class TestProperty:
    """
    A test class that takes a string, an integer, and a class object as parameters.
    All parameters are converted to instance variables.
    """

    def __init__(self, string, integer, class_object):
        self.string = string
        self.integer = integer
        self.class_object = class_object


class TestSubproperty:
    """
    A test class that takes three integers as parameters.
    All parameters are converted to instance variables.
    """

    def __init__(self, int1, int2, int3):
        self.int1 = int1
        self.int2 = int2
        self.int3 = int3
