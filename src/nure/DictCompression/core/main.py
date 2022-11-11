import pathlib
from src.nure.DictCompression.core.classes.lzw import LZW
from src.nure.DictCompression.utils import *
from sys import getsizeof


path_depth = len(pathlib.Path('.').resolve().parents)
ROOT_PATH = pathlib.Path('.').resolve().parents[path_depth-4]
RESOURCE_PATH = ROOT_PATH / 'resources'
INPUT_TEXT_PATH1 = RESOURCE_PATH / 'The slopes of Blessure.txt'
OUTPUT_CODE_PATH1 = RESOURCE_PATH / 'The slopes of Blessure (code).bin'
INPUT_TEXT_PATH2 = RESOURCE_PATH / 'Mushoku tensei.txt'
OUTPUT_CODE_PATH2 = RESOURCE_PATH / 'Mushoku tensei (code).bin'
INPUT_TEXT_PATH3 = RESOURCE_PATH / 'Unicode HOWTO.txt'
OUTPUT_CODE_PATH3 = RESOURCE_PATH / 'Unicode HOWTO (code).bin'


if __name__ == '__main__':
    input_path_str = input("Input a path to a file (or just skip):\n>>> ")
    input_path = pathlib.Path(input_path_str) if input_path_str else INPUT_TEXT_PATH3
    output_path = pathlib.Path(input_path_str[:-4]+' (code).bin') if input_path_str else OUTPUT_CODE_PATH3
    try:
        dict_size = int(input("Input initial size of a dictionary (default=256):\n>>> "))
    except ValueError:
        dict_size = 256

    # Reading input information and print on the screen
    message = input_path.read_text(encoding='utf-8')
    print_red("Input message:")
    print(message, sep='\n')
    print_red("Input message has", len(message), "symbols")

    # Generate a compressor variable and compress the message
    compressor = LZW(dict_size)
    code = compressor.compress(message)
    print_red('LZW code for message:')
    print(code[:20], end='...\n')
    print_red("LZW code has", len(code), "symbols")

    # Save the code in a binary file and read it again
    write_list_to_file(code, str(output_path), 2)
    read_list = read_bytes_to_ints(output_path, 2)
    print_red("Bytes from the .bin file:")
    print(read_list[:20], end='...\n')

    # Decompress the message from the code and print on the screen
    decoded = compressor.decompress(read_list)
    print_red("Decoded message:")
    print(decoded, sep='\n')
    print_red(len(decoded), "symbols")
    print("GOOD FINISHED")

    print_red("Size of dictionary = ", getsizeof(compressor.encode_dictionary), 'bytes')
