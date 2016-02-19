class LazyOperation:
    def __init__(self,old_fuction,args_a,kwargs_a):
        self._function = old_fuction
        self._args = args_a
        self._kwargs = kwargs_a

    def __eq__(self,other):
        retval = (self._args == other._args) and (self._kwargs == other._kwargs)
        retval = retval and (id(self._function) == id(other._function))
        return retval

    def eval(self):
        computedArgs = []
        computedKWArgs = []

        # positional args
        for a in self._args:
            if a.__class__.__name__ == "LazyOperation":
                computedArgs.append(a.eval())
            else:
                computedArgs.append(a)

        # keyword args
        for k,v in self._kwargs.items():
            if v.__class__.__name__ == "LazyOperation":
                computedArgs.append((k,v.eval()))
            else:
                computedArgs.append((k,v))
        return self._function(*tuple(computedArgs),**dict(computedKWArgs))

# this is the decorator
def lazy(old_fuction):
    def decorated_func(*args,**kwargs):
        return LazyOperation(old_fuction,args_a = args,kwargs_a = kwargs)
    return decorated_func

# raw functions
def add(a,b):
    return a+b
def mul(a,b):
    return a*b

# decorated functions
lazy_add = lazy(add)
lazy_mul = lazy(mul)

# print(id(lazy_add(1,2)))
# print(id(LazyOperation(add,args=[1,2],kwargs={})))
# print(lazy_add(1,2) == LazyOperation(add,args_a = (1,2),kwargs_a={}))
print(isinstance( lazy_add(1,2), LazyOperation ) == True)
print(lazy_add(lazy_mul(3,4),5).eval())
