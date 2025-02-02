import hashlib
import base64

def calcular_hash(mensagem):
    # biblioteca padrão do Python para hash, sha3_256() gera um valor de hash de 256 bits (32 bytes)
    # digest() retorna o valor do hash calculado como uma sequência de bytes
    return hashlib.sha3_256(mensagem.encode('utf-8')).digest()

def cifrar_rsa(mensagem, chave_privada):
    d, n = chave_privada
    #from_bytes() converte uma sequência de bytes em um número inteiro.
    # 'big' = a ordem dos bytes é da mais significativa para a menos significativa (big-endian)
    mensagem_int = int.from_bytes(mensagem, 'big')
    # pow é uma biblioteca de exponenciação modular onde pow(mensagem_int, d, n) = (mensagem_int^d)modn.
    return pow(mensagem_int, d, n)
    
def assinatura_mensagem(mensagem, chave_privada):
    hash_mensagem = calcular_hash(mensagem)
    assinatura = cifrar_rsa(hash_mensagem, chave_privada)
    # adiciono uma margem de erro de 7 bits para ter certeza que terá espaço suficiente.
    # faço uma divisão por 8 (pego o inteiro) para saber o nº de bytes.
    tamanho_em_bytes = (assinatura.bit_length() + 7) // 8
    assinatura_bytes = assinatura.to_bytes(tamanho_em_bytes, byteorder='big')
    # base64.b64encode() recebe um valor em bytes e o codifica em base64.
    # chr(b) converte o byte de volta para o caractere correspondente.
    assinatura_base64 = ''.join([chr(b) for b in base64.b64encode(assinatura_bytes)]) 
    return assinatura_base64