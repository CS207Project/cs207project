
class LazyOperation:

    def __init__(self,old_fuction,*args,**kwargs):
        self._function = old_fuction
        self._args = args
        self._kwargs = kwargs
    '''
    def __eq__(self,other):
        print("in eq")
        print(type(self).__name__)
        print(type(other).__name__)
        return id(self) == id(other)
    '''
    def eval(self):
        return self._function(*self._args,**self._kwargs)

def lazy(old_fuction):
    def decorated_func(*args,**kwargs):
        return LazyOperation(old_fuction,*args,**kwargs)

    return decorated_func

@lazy
def lazy_add(a,b):
    return a+b

l = lazy_add(1,2)

print(id(l))
print(id(lazy_add(1,2)))
print(id(LazyOperation(lazy_add,args=[1,2],kwargs={})))

assert(lazy_add(1,2) == LazyOperation(lazy_add,args=[1,2],kwargs={}))
#ladd = lazy_add(1,2)
#print(ladd.eval())
