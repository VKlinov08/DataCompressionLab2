from typing import List
import unicodedata


def write_list_to_file(int_list: List[int],
                       file_path: str,
                       bytes_per_int: int) -> int:
    """
    This function writes a list of integers to a binary file.
    :param int_list: List of integers
    :return: number of successfully written bytes
    """
    result = 0
    with open(file_path, 'wb') as bin_file:
        for i in int_list:
            int_bytes = bytes(i.to_bytes(bytes_per_int, 'big'))
            result += bin_file.write(int_bytes)
    return result


def read_bytes_to_ints(file_path: str, bytes_per_int: int) -> List[int]:
    """
    This function read a byte sequence to a list of integers.
    :param bytes_per_int: number of bytes representing each integer number
    :param file_path: path to a binary file
    :return: list of integer values
    """
    result = []
    with open(file_path, 'rb') as bin_file:
        int_bytes = bin_file.read(bytes_per_int)
        while int_bytes:
            number = int.from_bytes(int_bytes, 'big')
            result.append(number)
            int_bytes = bin_file.read(bytes_per_int)
    return result


def print_red(*args, sep=' '):
    output_text = '\033[91m'
    for arg in args[:-1]:
        output_text = output_text + f'{arg}' + sep
    output_text = output_text + f'{args[-1]}'
    output_text += '\033[00m'
    print(output_text)


def strip_accents(s):
    nfkd_form = ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('ASCII')