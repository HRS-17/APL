def dec(fun):
    def wrapper():
        print("times before explosion")
        fun()
        print("times after explosion")
    return wrapper

@dec
def hello():
    print("say_hello")
#@dec
def world():
    print("say_world")

hello()
world()
