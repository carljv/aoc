from collections import deque, namedtuple

DecoderResults = namedtuple('DecoderResults', ['processed_tokens', 'marker'])

def decode_stream(fpath, marker_len):
    buffer = deque(maxlen = marker_len)
    processed_tokens = 0

    with open(fpath, 'rt') as f:
            while True:
                c = f.read(1)
                if not c:
                    return None
                else: 
                    processed_tokens += 1
                    buffer.append(c)
                    if len(set(buffer)) == marker_len:
                        marker = ''.join(buffer)
                        return DecoderResults(processed_tokens = processed_tokens, 
                                              marker = marker)


INPUT = 'day06_input.txt'

if __name__ == '__main__':
    print(decode_stream(INPUT, 4))  # 1,238 / zvpm
    print(decode_stream(INPUT, 14)) # 3,037 / qspgbzmjnlrdhv