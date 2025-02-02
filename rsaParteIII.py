import base64
import hashlib
import rsa
from rsaParteI import is_prime, gen_prime, gen_d

# Função para decodificar a mensagem em Base64
def decode_base64(encoded_message):
    try:
        decoded_message = base64.b64decode(encoded_message)
        return decoded_message
    except Exception as e:
        print(f"Erro na decodificação: {e}")
        return None

# Função para verificar a assinatura (usando a chave pública RSA)
def verify_signature(message, signature, public_key):
    try:
        # Hash da mensagem
        message_hash = hashlib.sha256(message).digest()

        # Verificar a assinatura usando a chave pública RSA
        # Aqui estamos usando o método de verificação com RSA e SHA256
        try:
            rsa.verify(message_hash, signature, public_key)
            return True
        except rsa.VerificationError:
            return False
    except Exception as e:
        print(f"Erro na verificação da assinatura: {e}")
        return False

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de documento com Base64 (substitua por um valor real)
    signed_document_base64 = "350533777483426794236289282208048435"
    
    # 1. Decodificar a mensagem
    decoded_message = decode_base64(signed_document_base64)
    
    if decoded_message:
        print(f"Mensagem decodificada: {decoded_message}")
        
        # 2. Verificação de assinatura (exemplo)
        # A chave pública seria carregada de um arquivo ou banco de dados
        public_key_pem = b"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7c3A"
        
        # Carregar a chave pública RSA
        public_key = rsa.PublicKey.load_pkcs1_pem(public_key_pem)

        # Vamos supor que a assinatura é um valor em bytes
        signature = b"AssinaturaEmBytes"

        # Verificar a assinatura
        is_valid = verify_signature(decoded_message, signature, public_key)
        if is_valid:
            print("Assinatura verificada com sucesso!")
        else:
            print("Assinatura inválida.")
