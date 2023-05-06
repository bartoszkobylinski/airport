
def create_string():
    print("i"*20000)
    return "I" * 10000

a = create_string()

def count_string(string_x):
    print(len(string_x))

count_string(a)