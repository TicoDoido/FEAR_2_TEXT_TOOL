input_file_path = 'Loki.strdb'
output_file_path = 'Loki.strdb.txt'
total_texts = 5913  # Total de textos que você deseja extrair

# Definindo o marcador de fim de texto e a substituição
end_marker = b'\x00\x00'
replacement_bytes = b'\x00\x5B\x00\x46\x00\x49\x00\x4D\x00\x5D\x00\x0A'
bom = b'\xfe\xff'

# Abrindo o arquivo binário em modo de leitura binária
with open(input_file_path, 'rb') as file, open(output_file_path, 'wb') as output_file:
    # Escrevendo o BOM no início do arquivo de saída
    output_file.write(bom)
    
    # Posicionando o cursor no início do bloco de textos
    file.seek(99912)

    texts_extracted = 0
    current_text = b''

    while texts_extracted < total_texts:
        # Lendo 2 bytes (caractere em UTF-16BE)
        char_bytes = file.read(2)

        # Se não houver mais bytes para ler, termina
        if not char_bytes:
            break

        # Verifica se encontrou o marcador de fim de texto (00 00)
        if char_bytes == end_marker:
            # Gravando o texto atual e o marcador substituído no arquivo de saída
            output_file.write(current_text + replacement_bytes)
            current_text = b''
            texts_extracted += 1
        else:
            current_text += char_bytes

print(f'{texts_extracted} textos extraídos e salvos em "{output_file_path}"')
