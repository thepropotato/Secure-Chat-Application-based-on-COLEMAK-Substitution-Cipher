import test as secret

char_set = ['q', 'w', 'f', 'p', 'g', 'j', 'l', 'u', 'y', 'a', 'r', 's', 't',
            'd', 'h', 'n', 'e', 'i', 'o', 'z', 'x', 'c', 'v', 'b', 'k', 'm',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            '!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

def encrypt(text, key) :
    
    crypt = ''
    l1 = len(text)
    l2 = len(key)
    key = key * (int(l1/l2) + (l1%l2)) + key[0 : (l1%l2)]
        
    for i in range (len(text)) :
        if text[i] == ' ' :
            crypt = crypt + " "
        
        elif text[i].lower() in char_set :
            num = char_set.index(key[i].lower())
            index = char_set.index(text[i].lower())
            if num != 0 :
                crypt = crypt + char_set[(index + num) % len(char_set)]
            else :
                crypt = crypt + char_set[(index + 4) % len(char_set)]
        elif text[i] not in char_set :
            crypt = crypt + text[i]
            
    crypt = decase(crypt, case(text))
           
    return crypt


def decrypt(crypt, key):
    
    text = ''
    l1 = len(crypt)
    l2 = len(key)
    key = key * (int(l1/l2) + (l1%l2)) + key[0 : (l1%l2)]
        
    for i in range (len(crypt)) :
        if crypt[i] == ' ' :
            text = text + " "
            
        elif crypt[i].lower() in char_set :
            num = - char_set.index(key[i].lower())
            index = char_set.index(crypt[i].lower())
            if num != 0 :
                text = text + char_set[(index + num) % len(char_set)]
            else :
                text = text + char_set[(index - 4) % len(char_set)]
        elif crypt[i] not in char_set :
            text = text + crypt[i]
            
    text = decase(text, case(crypt))
           
    return text
        
def case (text) :
    bin = ""
    for i in text :
        if i == " " :
            bin = bin + " "
        elif i.isupper() :
            bin = bin + "1"
        else :
            bin = bin + "0"
    return bin

def decase (text, bin) :
    out = ""
    for i in range (len(text)) :
        if bin[i] == " " :
            out = out + " "
        elif bin[i] == "1" :
            out = out + text[i].upper()
        else :
            out = out + text[i].lower()
    return out