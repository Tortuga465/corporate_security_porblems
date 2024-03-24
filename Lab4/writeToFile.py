def writePrivateKey(filename, privateKey):
    f=open("serverPrivatekey.txt","w")
    for item in privateKey:
        f.write(str(item))
        f.write("\n")
    f.close()