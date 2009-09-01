def processLine(line):
    entries = line.split()
    if len(entries) < 3:
        return None
    try:
        sec = int(entries[0])
        microsec = int(entries[1])
        operation = entries[2]
        return (sec*1000000 + microsec, operation)
    except:
        return None

def parseFiles(path):
    for name in os.listdir(path):
        if "behavior" not in name:
            continue
        fullname = os.path.join(path, name)
        f = open(fullname, "r")
        for line in f:
            res = processLine(line)
            if not res: continue
            time, operation = processLine(line)
            yield (time, operation)
        f.close()
