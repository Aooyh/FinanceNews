def fun(temp_fun):
    def in_fun(*args, **kwargs):
        """kkk"""
        b = 1
        return temp_fun(*args, **kwargs)
    return in_fun


@fun
def test1():
    b = 2
    print(test1.__name__)
    return test1.__name__

@fun
def test2():
    return test2.__name__

print(test1())
print(test2())
