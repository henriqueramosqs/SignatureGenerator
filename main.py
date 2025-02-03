from rsaParteI import *
from rsaParteIII import *
from rsaParteII import *

if __name__ == "__main__":

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
    label = b""


    print("Mensagem original:",mensagem)
    #Pause
    # input()

    encoded = oaep_encode(mensagem, k, label)

    print("Mensagem depois do padding:",encoded)
    #Pause
    # input()

    cipher = rsa_encrypt(encoded, chave_publica)

    print("Mensagem após encriptação por RSA: ",cipher)
    #Pause
    # input()

    decrypted = rsa_decrypt(cipher, chave_privada)

    print("Mensagem após decriptação por RSA: ",decrypted)
    #Pause
    # input()

    decoded_message = oaep_decode(decrypted, k,label)

    print("Mensagem após desfeito padding",mensagem)
    # Pause
    # input()

    print("Mensagem original:", mensagem)
    print("Mensagem decodificada:", str(decoded_message, 'UTF-8'))

    # Parte II

    mensagem = "Gato"
    assinatura = assinatura_mensagem(mensagem, chave_privada)
    print("Mensagem Original 1: ", mensagem)
    print("Assinatura (Base64) 1: ", assinatura)

    #Pause
    # input()

    mensagem = "Gado"
    assinatura = assinatura_mensagem(mensagem, chave_privada)
    print("Mensagem Original 2: ", mensagem)
    print("Assinatura (Base64) 2:", assinatura)


    # Parte III