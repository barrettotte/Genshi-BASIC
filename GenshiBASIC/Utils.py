import json, os, datetime


def getTimestamp():
    return str(datetime.datetime.now())

def log(msg, msgType="INFO", path=".\\log.txt", writeFile=False, init=False, pref=""):
    msg = "[" + msgType.ljust(6) + getTimestamp() + "] " + pref + msg
    if init and os.path.exists(path):
        os.remove(path)
    if writeFile:
        try:
            mode = 'a+' if os.path.exists(path) else 'w+'
            with open(path, mode) as f:
                f.write(msg + "\n")
        except Exception as e:
            print("[ERROR " + getTimestamp() + "] Could not write to log")
            print("[ERROR " + getTimestamp() + "] " + (" " * 3) + str(e))
    print(msg)

def read_file(file_path, throw_error=False):
    try:
        with open(file_path, 'r', encoding="utf8") as f:
            return f.readlines()
    except FileNotFoundError:
        if throw_error: raise FileNotFoundError
        log("File [" + file_path + "] could not be found.", "ERROR")
    return ""

def printDict(d):
    for key, val in d.items():
        print(key + " --- " + str(val))

def getElemByKey(target, key, collection):
    for elem in collection:
        if elem[key] == target:
            return elem
    return None