from io import StringIO

class LZW(object):
    __slots__ = ['encode_size', 'decode_size', 'encode_dictionary', 'decode_dictionary']
    encode_size: int
    decode_size: int
    encode_dictionary: dict
    decode_dictionary: dict

    def __init__(self, dict_size=256):
        self.encode_size = dict_size
        self.decode_size = dict_size
        self.encode_dictionary = {chr(i): i for i in range(dict_size)}
        self.decode_dictionary = {i: chr(i) for i in range(dict_size)}

    def compress(self, uncompressed):
        """Compress a string to a list of output symbols."""

        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in self.encode_dictionary:
                w = wc
            else:
                try:
                    result.append(self.encode_dictionary[w])
                except KeyError:
                    print(f"Unexpected symbol {w}")

                # Add wc to the dictionary.
                self.encode_dictionary[wc] = self.encode_size
                self.encode_size += 1
                w = c

        # Output the code for w.
        if w:
            result.append(self.encode_dictionary[w])
        return result

    def decompress(self, compressed):
        """Decompress a list of output ks to a string."""

        result = StringIO( )
        w = chr(compressed.pop(0))
        result.write(w)
        for k in compressed:
            if k in self.decode_dictionary:
                entry = self.decode_dictionary[k]
            elif k == self.decode_size:
                entry = w + w[0]
            else:
                raise ValueError(f'Dictionary is incomplete. Unknown symbol. Bad compressed k {chr(k)}: {k}')
            result.write(entry)

            # Add w+entry[0] to the dictionary.
            self.decode_dictionary[self.decode_size] = w + entry[0]
            self.decode_size += 1

            w = entry
        return result.getvalue()
