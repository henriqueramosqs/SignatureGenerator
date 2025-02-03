import base64
from rsaParteI import gen_prime
from rsaParteII import calcular_hash

def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def gerar_chaves_rsa(bits=1024):
    p = gen_prime(bits)
    q = gen_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)
    return (e, n), (d, n)

def verificar_assinatura_rsa(mensagem, assinatura, chave_publica):
    e, n = chave_publica
    message_hash = calcular_hash(mensagem)
    assinatura_bytes = base64.b64decode(assinatura.encode('utf-8'))
    assinatura_int = int.from_bytes(assinatura_bytes, byteorder='big')
    decrypted_signature = mod_exp(assinatura_int, e, n)
    mensagem_hash_int = int.from_bytes(message_hash, byteorder='big')
    return decrypted_signature == mensagem_hash_int