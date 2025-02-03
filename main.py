from rsaParteI import *
from rsaParteIII import *
from rsaParteII import *
import sys

if __name__ == "__main__":

    dist = ""
    if(len(sys.argv)>1):
        dist=sys.argv[1]
    # Parte I

    p = gen_prime()
    q = gen_prime()

    print("p:",p)
    print("q:",q)

    # Pause
    # input()
    
    n = p*q
    fi_n= (p-1)*(q-1)
    chave_privada = (gen_d(fi_n),n)
    chave_publica = (mod_inv(chave_privada[0], fi_n),n)
    
    print("Chave privada:",chave_privada)
    print("Chave pública:",chave_publica)
    
    #Pause
    # input()

    k = (n.bit_length() + 7) // 8


    mensagem = b"Banana, abacate, tamarindo"
    if(len(dist)):
        mensagem = bytes((open(dist, "r").read()),'utf-8')

    label = b""


    print("Mensagem original:",mensagem,"\n")
    #Pause
    # input()

    encoded = oaep_encode(mensagem, k, label)

    print("Mensagem depois do padding:",''.join([chr(b) for b in base64.b64encode(encoded)]) ,"\n")
    #Pause
    # input()

    cipher = rsa_encrypt(encoded, chave_publica)

    print("Mensagem após encriptação por RSA: ",''.join([chr(b) for b in base64.b64encode(cipher)]),"\n")
    #Pause
    # input()

    decrypted = rsa_decrypt(cipher, chave_privada)

    print("Mensagem após decriptação por RSA: ",''.join([chr(b) for b in base64.b64encode(decrypted)]),"\n")
    #Pause
    # input()

    decoded_message = oaep_decode(decrypted, k,label)

    print("Mensagem após desfeito padding",mensagem,"\n")
    # Pause
    # input()

    print("Mensagem original:", mensagem,"\n")
    print("Mensagem decodificada:", str(decoded_message, 'UTF-8'),"\n")

    # Parte II
    mensagem = str(mensagem)
    assinatura = assinatura_mensagem(mensagem, chave_privada)
    print("Mensagem Original 1: ", mensagem,"\n")
    print("Assinatura (Base64) 1: ", assinatura,"\n")

    #Pause
    # input()

    # Parte III