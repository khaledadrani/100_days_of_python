
def binary_to_decimal(nb):
    nb = list(str(nb))[::-1]
    nb = sum([int(nb[i])*2**i for i in range(len(nb))])
    return nb

def decimal_to_binary(nb):
    o = ""
    while nb>0:
        rest = nb % 2
        nb = nb // 2
        o += str(rest)
    return o[::-1]


def test_binary_to_decimal(func):

    assert func(10) == 2
    assert func(1010) == 10
    assert func(111111) == 63

def all_tests():
    try:
        test_binary_to_decimal(func=binary_to_decimal)
        print("all tests are passed")
    except Exception as err:
        print("Failed test: ",err)



if __name__ == "__main__":
    #print(binary_to_decimal(nb=11101))
    #all_tests()
    print(decimal_to_binary(nb=29))
