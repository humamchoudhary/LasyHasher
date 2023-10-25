import binascii
import struct
import sys
import secrets
import gzip
sys.set_int_max_str_digits(999999999)

def pad(message):
    bin_message = binascii.hexlify(message.encode())
    bin_message = bin(int(bin_message, 16))[2:].zfill(8 * ((len(bin_message) + 1) // 2))
    bin_message += "1"
    while len(bin_message) % 512 != 448:
        bin_message += "0"
    bin_message += bin(struct.unpack(">Q", struct.pack(">q", len(message) * 8))[0])[2:].zfill(64)
    return bin_message

def chuckization(message,chucksize):
    if type(message) == str:
        return [int(message[i:i+chucksize]) for i in range(0, len(message), chucksize)]

    else:
        message = f"{message}"
        return [int(message[i:i+chucksize]) for i in range(0, len(message), chucksize)]

def rol(val, r_bits, max_bits):
  return (val << r_bits%max_bits) & (2**max_bits-1) | \
         ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

def ror(val, r_bits, max_bits):
  return ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
         (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def leftshift(x,n,i):
    return rol(x >> n*i,n,len(str(x)))

def rightshift(x,n,i):
    return rol(x << n*i,n,len(str(x)))

randomer = ['1011101111001000000110011011100000011',
 '11000101000100000100110100001001110111',
 '1000000010011100100000100001001000010',
 '10011101110011010010000000011101100010',
 '1001101011001100010010011000100011001',
 '10011000000000100000100010100100100100',
 '10100101000011100110100011000110101',
 '1010101000001010001011001001000100101',
 '1000100010110001101010010010000001000',
 '1100010011001010001000111010001000001',
 '11000001001001001100100011010001110001',
 '11100100100001000000001001010101110011',
 '100101100001100110000111000101100011',
 '1010100001000100101110000100110010011',
 '10010001010011011000110101011101001000',
 '10100001110000011101100011001000100001',
 '11011000100100001110000001000010000000',
 '1100010000010110011000010000000001',
 '11000000111001000100101001001111000',
 '1010000100110100010000001100110000111',
 '1100100100101000001111000001110001000',
 '10000101100010000001111000001000000110',
 '10011000010100100010001000000100000011',
 '11001001001000001000100010010110000000',
 '11100000110101001110010000010000000001',
 '100000000100010001000100100011101110100',
 '1001100100001101000111000001111000',
 '11000000100100000000111011000101000',
 '11101110000001001010101100110000011',
 '1001001001001000101010000000100100010',
 '1010101010101000010000001011010010010',
 '1100110010110000001100100100110000110',
 '10010101010100001000100000100010000010',
 '10100000100001100000110100001101001001',
 '10100101010010100110010110100000001000',
 '11001000010000001100010011011001110001',
 '11001100110110010101110001100010010001',
 '11010110000100010100101000011100010001',
 '100010011100100100110100110010011',
 '1100111000001001000001100010010101',
 '11001100110001100000111001000000101',
 '11101110011010100101001100100010010',
 '1001010010100011101010111001101110010',
 '1001110010110000110000010001010010001',
 '1011010010101000110000011011100000000',
 '1100110000110011001100001000001010001',
 '10000101110111000000100110001101010000',
 '10010001010110100101010110000000110111',
 '10011100110000010010000101100100100001',
 '10100000100000001100000010010000010001',
 '11001001011001011100110000100000000000',
 '11001101000101011101100100011101110001',
 '11010100010110000001100101100000010111',
 '11011000000000001101010010100000000100',
 '100000010010100010101110001100100001001',
 '1001110101010000100011001101000100',
 '10000110000001000100111011100110100',
 '10100000110100101001000011000010110',
 '11001011001000001100000010101010110',
 '100010000011100110010111100001110111',
 '100101011000000100111001010101110001',
 '1001100100010100000100010001000011000',
 '1010100110111000000000010000001100011',
 '1011101000111100001110011011101111001',
 '1100101010101010101100010001000100010',
 '10000000100100000100000100100000010101',
 '10001000100111011100110000010001010010',
 '10001101100001100001010010010000100100',
 '10010000101000010000110110010001110100',
 '10011101010110011100110100000110000111',
 '11001000000100000000110001010001111001',
 '11001100101001001100100101001010011000']

def choose(x,y,z):
    return (z ^ y) & x ^ y

def galosisFeild_mul(a,b):
    prim_poly = 0b100011101 
    result = 0
    for i in range(8):
        if (b & 1) != 0:
            result ^= a
        hi_bit_set = (a & 0x80) != 0
        a <<= 1
        if hi_bit_set:
            a ^= prim_poly        
        b >>= 1
    return result


def randomizer(message,salt):
    if salt != 0:
        message += salt
    message = bin(int(message) <<64  )[2:] 
    chunks = chuckization(message,64)
    
    out = ""
    for index,i in enumerate(chunks):
        x,y,z=i,i,i
        
        try:
            for j in range(int(str(i)[-3:-1],2)):

                x = rightshift(i,2,index) ^ rightshift(i,14,index) ^ rightshift(i,22,index)>> (index*2) 
                y = leftshift(i,2,index) ^ leftshift(i,14,index) ^ leftshift(i,22,index)>> (index*2) 
                z = rightshift(x,2,j) ^ leftshift(y,14,j) ^ leftshift(x,22,j)>> (index*2)
                x = choose(x,y,z)
        except:
            pass

        quarter = x & 0xFFFF    
        quarter = rol(quarter, 5, 16) 
        half = x & 0xFFFFFFFF  
        half = ror(half, 17, 32)

        x ^= (quarter | (half << 16))

        x = galosisFeild_mul(x,y)
        
        if(x==0):
            out += "0"*32+randomer[0]
        else:
            out += bin(x)[2:]+randomer[int(str(x)[-1])]
        
    return out

def compress(message,size):
    def basic_comp(message):
        chunks_1 = chuckization(message,2)
        
        for i in range(0, len(chunks_1), 2):
            try:
                chunks_1[i] = chunks_1[i] ^ chunks_1[i+1]
            except:
                pass
        return ''.join(map(str, chunks_1))
    
    while len(message) > size:
        message = basic_comp(message)
    while len(message) < size:
        message +=message[len(message)//2]
    return message

def eachLoop(message,salt="0"):
    message.replace(message[len(message)-len(message)//4:len(message)+len(message)//4],"")
    
        
    salt_bin= bin(int(salt,16))[2:]
    padded = pad(str(message))
    for i in range(5):
        rand = randomizer(padded,salt_bin)
        comp = compress(rand,len(rand)//4)
    return comp[:len(comp)//2]

def mainLoop(message,salt="0"):
    
        
    out = ""
    paddedmsg = pad(message)
    message_list = chuckization(paddedmsg,(len(paddedmsg)//1024 or 256))
    
    for i in message_list:
        out+=eachLoop(str(i),salt)

    salt_bin= bin(int(salt,16))[2:]
  
    res = ""
  
    for i in range(int(out[-3:-1],2)):

        rand = randomizer(out,salt_bin)
        comp = compress(rand,64)
        res+= comp
    comp = compress(rand,256)
    res = comp
    return ("%x" % int(res,2),salt)



def hash(data,salt="0"):
    if len(data) > 10240:
        data = str(gzip.compress(data.encode()))

    return mainLoop(data,salt)

if __name__ =="__main__":
    inp = input("Enter text: ")
    cond = int(input("Salt:\n1- Generate salt\n2-Input Salt\n3- No salt: "))
    if cond ==1:
        salt = secrets.token_hex(8)
    elif cond == 2:
        salt = input("Enter Salt: ")
    else:
        salt = "0" 
    print(hash(inp,salt))


