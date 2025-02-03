from rsaParteI import *
from rsaParteIII import *
from rsaParteII import *

if __name__ == "__main__":

    # Parte I

    p = gen_prime()
    q = gen_prime()
    n = p*q
    fi_n= (p-1)*(q-1)
    chave_privada = gen_d(fi_n)
    chave_publica = mod_inv(chave_privada, fi_n)
    k = (n.bit_length() + 7) // 8

    mensagem = b"banana pau torto"
    label = b"Label"

    encoded = oaep_encode(mensagem, k, label)
    cipher = rsa_encrypt(encoded, chave_publica, n)
    decrypted = rsa_decrypt(cipher, chave_privada, n)
    decoded_message = oaep_decode(decrypted, k,label)

    print("Mensagem original:", mensagem)
    print("Mensagem decodificada:", str(decoded_message, 'UTF-8'))

    # Parte II

    mock_chave_privada = (123456789, 987654321987654321987654321987654321)
    mensagem = "Testando assinatura"
    assinatura = assinatura_mensagem(mensagem, mock_chave_privada)
    print("Mensagem Original:", mensagem)
    print("Assinatura (Base64):", assinatura)

    # Parte III