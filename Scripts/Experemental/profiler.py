streams = []


def open_stream(file_path):
    res = open(file_path, 'w+')
    streams.append(res)
    return res


def close_streams():
    for stream in streams:
        stream.close()
