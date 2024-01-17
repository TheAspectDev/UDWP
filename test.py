def Command(func: callable):

    def inner():
        print(func.__name__)
    
    inner()

    return inner

@Command
def ordinary():
    print("I am ordinary")