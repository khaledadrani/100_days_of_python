from day_1_binary_to_decimal import binary_to_decimal, decimal_to_binary

hex_dic = {
    'A':10,
    'B':11,
    'C':12,
    'D':13,
    'E':14,
    'F':15
}


def hex_to_decimal(nb):
    nb = list(str(nb))[::-1]
    ls = []
    print(nb)
    for i in range(len(nb)):
        digit = nb[i]
        if digit in hex_dic.keys():
            digit = hex_dic[digit]
        print(digit,type(digit))
        ls.append(int(digit)*16**i)
    return sum(ls)

def decimal_to_hex(nb):
    o = ""
    inverted_hex_dic = {v:k for k,v in hex_dic.items()}
    print(inverted_hex_dic)
    while nb>0:
        rest = nb % 16
        nb = nb // 16
        if rest in inverted_hex_dic.keys():
            rest = inverted_hex_dic[rest]
        o += str(rest)

    return o[::-1]

def hex_to_bin(nb):
    ls = []
    for n in list(nb)[::-1]:
        n = hex_dic.get(n,n)
        n = decimal_to_binary(n)
        ls.append(n)
    return "".join(ls)

def bin_to_hex(nb):

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    groups = list(chunks(list(nb)[::-1],4))

    print('groups ',groups)

    res = "".join([binary_to_decimal(int("".join(group))) for group in groups])

    return decimal_to_hex(res)

    
hexa = "AAAA"
decim = 43690



print(decim)
print(hexa)
print(decimal_to_binary(decim))
print(bin_to_hex("1010101010101010"))
#print(correct_res)


