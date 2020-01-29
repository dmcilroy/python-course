if __name__ == '__main__':
    print("My first_file is being run directly")

else:
    print("My first_file is being imported")


def do_sensitive_stuff():
    print("Executing function doing sensitive stuff")

def do_other_stuff():
    print("Executing function doing other stuff")


if __name__ == '__main__':
    print("My first_file is being run directly")
    do_sensitive_stuff()

else:
    print("My first_file is being imported")
    do_other_stuff()
