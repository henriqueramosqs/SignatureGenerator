import hashlib
import base64
from rsaParteI import *

def calcular_hash(mensagem):
    # biblioteca padrão do Python para hash, sha3_256() gera um valor de hash de 256 bits (32 bytes)
    # digest() retorna o valor do hash calculado como uma sequência de bytes
    return hashlib.sha3_256(mensagem.encode('utf-8')).digest()

    
def assinatura_mensagem(mensagem, chave_privada):
    hash_mensagem = calcular_hash(mensagem)
    assinatura =rsa_encrypt(hash_mensagem,chave_privada)
    # chr(b) converte o byte de volta para o caractere correspondente.
    assinatura_base64 = ''.join([chr(b) for b in base64.b64encode(assinatura)]) 
    return assinatura_base64
