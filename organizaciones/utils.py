import base64

def xor_cipher(data, key):
    """
    Aplica un cifrado XOR simple con una clave.
    """
    result = bytearray()
    key_bytes = key.encode('utf-8')
    key_len = len(key_bytes)
    
    for i, char in enumerate(data):
        result.append(char ^ key_bytes[i % key_len])
    
    return bytes(result)

def decode_credentials():
    """
    Decodifica las credenciales encriptadas del superusuario.
    """
    # Clave para el cifrado XOR (no es la contraseña real)
    key = "AtHenEa2023"
    
    # Credenciales codificadas en base64 y cifradas con XOR
    # Estos valores son el resultado de: base64.b64encode(xor_cipher("valor".encode('utf-8'), key))
    encoded_email = "AAAgAAAgAHpIcQ=="  # AtheneaHxC
    encoded_password = "AAAgAAAgAAICAgFzRWZL"  # Athenea020221..
    encoded_name = "ABAlDAAsEkZCU1cuBg=="  # Administrador
    
    # Decodificar y descifrar las credenciales
    email_bytes = base64.b64decode(encoded_email)
    password_bytes = base64.b64decode(encoded_password)
    name_bytes = base64.b64decode(encoded_name)
    
    email = xor_cipher(email_bytes, key).decode('utf-8')
    password = xor_cipher(password_bytes, key).decode('utf-8')
    name = xor_cipher(name_bytes, key).decode('utf-8')
    
    return email, password, name