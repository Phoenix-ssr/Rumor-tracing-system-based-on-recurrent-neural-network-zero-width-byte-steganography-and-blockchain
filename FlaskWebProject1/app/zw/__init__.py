import re
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
#摩斯码表
morse_codes = ['.-','-...','-.-.','-..','.','..-.','--.','....','..','.---','-.-','.-..','--','-.','---','.--.','--.-','.-.','...','-','..-','...-','.--','-..-','-.--','--..','-----','.----','..---','...--','....-','.....','-....','--...','---..','----.','-...-']

encode_dict = dict(zip(chars.lower(), morse_codes))
decode_dict = dict(zip(morse_codes, chars.lower()))
print()
#将字符串转换成零宽字符
def string_2_nonezero(s):
    def char_2_morse(char):
        return encode_dict.get(char, "-...-")
    def string_2_nonezero(string):
        change_dict = dict(zip(["/", ".", "-"], ["&#8203;", "&#8204;", "&#8205;"]))
        return "".join([change_dict.get(s, " ") for s in string])
    morse = "/".join([char_2_morse(x) for x in s])
    return string_2_nonezero(morse)
#提取隐藏信息，返回提取信息，空则返回：""
def nonezero_2_string(s):
    #nonezero_string = re.match(r"(&#8203;|&#8204;|&#8205;|\u200B|\u200C|\u200D|&zwnj;|&zwj;)+", s)
    result = re.search(r"(&#8203;|&#8204;|&#8205;|\u200B|\u200C|\u200D|&zwnj;|&zwj;)+", s)
    if result == None:
        return ""
    idx = result.span()
    #print(re.search(r"(&#8203;|&#8204;|&#8205;|\u200B|\u200C|\u200D|&zwnj;|&zwj;)+", s).string)
    #print(result.string[idx[0]:idx[1]])
    nonezero_string = result.string[idx[0]:idx[1]]
    nonezero_string = re.sub(r"&#8203;|\u200B", "/", nonezero_string)
    nonezero_string = re.sub(r"&#8204;|\u200C|&zwnj;", ".", nonezero_string)
    nonezero_string = re.sub(r"&#8205;|\u200D|&zwj;", "-", nonezero_string)
    return "".join([decode_dict.get(x, " ") for x in nonezero_string.split("/")])

#检查是否存在隐写内容
def check_message(message):
    #返回2不进行操作
    #返回1已经进行隐藏操作
    #返回0未进行隐藏操作
    if(len(message)<=2):
        return 2
    if (nonezero_2_string(message)!=""):
        return 1
    return 0
#将user_information隐写到message中，对半取
def hide_message(message,user_information):
    new_message = message[:len(message)//2]+string_2_nonezero(user_information)+message[len(message)//2:]
    #(hash(message),user_information)
    return new_message
#对已经隐写的内容进行改变，记录传播链
def change_message(message,userid,n=6):# n是计数器位数长度,需要提取谣言id
    #增加传播次数
    data = nonezero_2_string(message)
    data=data[:-n] + str(int(data[-n:])+1).rjust(n, '0')
    rumorid,fromid,toid,c = get_hidemassage(data)
    fromid = toid
    toid = userid
    #去除隐藏的信息
    result = re.search(r"(&#8203;|&#8204;|&#8205;|\u200B|\u200C|\u200D|&zwnj;|&zwj;)+", message)
    idx = result.span()
    result.string[idx[0]:idx[1]]
    data = "id"+str(rumorid)+"from"+str(fromid)+"to"+str(toid)+"c"+str(c)
    print(data)
    return hide_message(result.string[:idx[0]]+result.string[idx[1]:],data),rumorid
#提取隐写信息
def get_hidemassage(data):
    #提取to
    toid = re.findall(r'to.*?c',data)[0]
    toid = toid[2:-1]
    print("toid",toid)   
    #提取from
    fromid = re.findall(r'from.*?to',data)[0]
    fromid = fromid[4:-2]
    print("fromid",fromid)  
    #提取rumorid
    rumorid = re.findall(r'id.*?from',data)[0]
    rumorid = rumorid[2:-4]
    print("rumorid:",rumorid)
    #提取couner
    c = re.findall(r'c.*?$',data)[0]
    c = c[1:]
    print("counter:",c)
    return rumorid,fromid,toid,c
