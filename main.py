# This is a sample Python script.
from itertools import repeat

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    str_ = "1df356fg567jg245gfdf67f42d4g7"
    result = ", ".join(filter(str.isdigit, str_))
    print(result)
    print(list(result))


def f(obj):
    if isinstance(obj, dict):
        return True
    else:
        return False

list_objects = ["str_", [1, 2, 3], 1, 1.5, {1: 1}, 2, 2.5, {"1": 1}]

result_2 = filter(f, list_objects)

print(type(result_2))
print(result_2)
print(list(result_2))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
