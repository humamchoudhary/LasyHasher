import binascii
inp = input("Enter text to hash: ")
size = 32

def biniz(val):
    hex_str = binascii.hexlify(val.encode())
    bin_int =  bin(int(hex_str, 16))[2:].zfill(8 * ((len(hex_str) + 1) // 2))
    return bin_int

def phase1(val):
    chunks = [val[i:i+size] for i in range(0, len(val), size)]
    ints = [int(c, 2) for c in chunks]
    result = 0
    for i in ints: 
        result +=i
    # print(result)
    return result

def phase2(val):
    sqr = str(val*val)
   
    return int(sqr[1:len(sqr)-1])

def mainLoop(inp,size):
    inp_bin = biniz(inp)
    chunks = [inp_bin[i:i+size] for i in range(0, len(inp_bin), size)]
    val = ""
    for chunk in chunks:
        p1 = phase1(chunk)
        val+=str(phase2(p1))
   
    return val
x = mainLoop(inp,size)
print(hex(int(x)))