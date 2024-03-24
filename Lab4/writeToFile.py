def writeKey(filename, key):
    f=open(filename,"w")
    for item in key:
        f.write(str(item))
        f.write("\n")
    f.close()