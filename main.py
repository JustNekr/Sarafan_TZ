# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_numbers(count: int) -> str:
    result_list = []
    for digit in range(1, count+1):
        digit_count: int = min(count, digit)
        count = count - digit_count
        result_list += [str(digit)] * digit_count
        if count <= 0:
            return "".join(result_list)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print(get_numbers(int(input('?:'))))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
