# Diccionario personalizado de 32 caracteres (5 bits)
D = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ12345"

# Función para convertir un carácter a su índice en el diccionario
def char_to_index(char):
    return D.index(char)

# Función para convertir índice a carácter en el diccionario
def index_to_char(index):
    return D[index % len(D)]

# Función para convertir un número a su representación binaria de 5 bits
def to_binary_5bits(num):
    return format(num, '05b')

# Función para la inicialización de estado (KSA)
def KSA(key):
    key_length = len(key)
    S = list(range(32))  # Trabajamos con 32 en lugar de 256 por el diccionario de 5 bits
    j = 0
    for i in range(32):
        j = (j + S[i] + key[i % key_length]) % 32
        S[i], S[j] = S[j], S[i]  # Intercambiar
    return S

# Función para la generación de flujo de claves (PRGA)
def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 32
        j = (j + S[i]) % 32
        S[i], S[j] = S[j], S[i]  # Intercambiar
        K = S[(S[i] + S[j]) % 32]
        yield K

# Función para aplicar RC4 y mostrar todos los pasos
def RC4(key, message):
    # Convertir la clave a índices en el diccionario
    key = [char_to_index(c) for c in key]
    S = KSA(key)
    keystream = PRGA(S)

    print("\n--- Detalles del Proceso de Cifrado ---\n")

    # Convertir mensaje a índices
    message_indices = [char_to_index(c) for c in message]
    print("Mensaje original en índices:", message_indices)
    print("Mensaje original en binario de 5 bits:")
    print(' '.join([to_binary_5bits(i) for i in message_indices]))

    # Generar keystream y mostrar en binario
    keystream_indices = [next(keystream) for _ in range(len(message))]
    print("\nKeystream en índices:", keystream_indices)
    print("Keystream en binario de 5 bits:")
    print(' '.join([to_binary_5bits(k) for k in keystream_indices]))

    # Aplicar XOR al mensaje con el keystream
    xor_result = [(m ^ k) for m, k in zip(message_indices, keystream_indices)]
    print("\nResultado XOR en índices:", xor_result)
    print("Resultado XOR en binario de 5 bits:")
    print(' '.join([to_binary_5bits(x) for x in xor_result]))

    # Convertir resultado cifrado a caracteres del diccionario
    cipher_text = ''.join([index_to_char(i) for i in xor_result])
    print("\nMensaje cifrado en caracteres del diccionario:", cipher_text)

    return cipher_text

# Parámetros del problema
key = "CLAVE"  # Ejemplo de clave entre 4 y 16 caracteres
message = "MENSAJEDEPRUEBARC4PARACRIPTOLOGIA"

# Cifrar el mensaje
cipher_text = RC4(key, message)

