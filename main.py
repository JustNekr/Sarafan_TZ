def get_numbers(count: int) -> str:
    result_list = []
    for digit in range(1, count+1):
        digit_count: int = min(count, digit)
        count = count - digit_count
        result_list += [str(digit)] * digit_count
        if count <= 0:
            return "".join(result_list)


if __name__ == '__main__':
    print(get_numbers(int(input('?:'))))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
