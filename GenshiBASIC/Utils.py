import json, os, io, datetime


def get_timestamp():
    return str(datetime.datetime.now())

def log(msg, msgType="INFO", path=".\\log.txt", write_file=False, init=False, pref=""):
    msg = "[" + msgType.ljust(6) + get_timestamp() + "] " + pref + msg
    if init and os.path.exists(path):
        os.remove(path)
    if write_file:
        try:
            mode = 'a+' if os.path.exists(path) else 'w+'
            with open(path, mode) as f:
                f.write(msg + "\n")
        except Exception as e:
            print("[ERROR " + get_timestamp() + "] Could not write to log")
            print("[ERROR " + get_timestamp() + "] " + (" " * 3) + str(e))
    print(msg)

def read_file(file_path, throw_error=False):
    try:
        with open(file_path, 'r', encoding="utf8") as f:
            return f.readlines()
    except FileNotFoundError:
        if throw_error: raise FileNotFoundError
        log("File [" + file_path + "] could not be found.", "ERROR")
    return ""

def print_dict(d):
    for key, val in d.items():
        print(key + "  " + str(val))

def print_tokens(d):
    for line_num, tokens in d.items():
        print(line_num)
        for token in tokens:
            print("  " + str(token))

def split_and_filter(s, delim=" ", filt=None, is_strip=True):
    return list(filter(filt, (s.strip() if is_strip else s).split(delim)))