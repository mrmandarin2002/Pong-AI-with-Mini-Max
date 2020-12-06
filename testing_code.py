def header_length(length):
    temp = ""
    while(len(temp) != 16 - len(str(length))):
        temp += '0'
    return temp + str(length)


print(header_length(523))