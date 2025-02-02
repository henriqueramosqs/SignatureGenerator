import base64
import binascii
from rsaParteII import calcular_hash

# Função para decodificar a mensagem em Base64
def decode_base64(encoded_message):
    try:
        decoded_message = base64.b64decode(encoded_message)
        return decoded_message
    except Exception as e:
        print(f"Erro na decodificação: {e}")
        return None
    
def verify_signature(message, signature, public_key):
    
    message_hash = (message)

    try:
        if binascii.hexlify(signature) == binascii.hexlify(message_hash):
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro na verificação da assinatura: {e}")
        return False