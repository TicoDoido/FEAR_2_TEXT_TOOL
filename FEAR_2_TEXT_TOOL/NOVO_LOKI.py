import struct

input_file_path = 'Loki.strdb'
output_file_path = 'Loki.strdb_modified.strdb'
block_start_position = 99912  # Posição onde o bloco de bytes começa
offset_position = 20  # Posição onde o valor a ser lido e modificado está
subtract_value = 161532  # Valor a ser subtraído do valor lido
replacement_file_path = 'Loki.strdb.txt'  # Arquivo que contém o bloco de substituição

# Sequências de bytes a serem substituídas
old_bytes = b'\x00\x5B\x00\x46\x00\x49\x00\x4D\x00\x5D\x00\x0A'
new_bytes = b'\x00\x00'

# Abrindo o arquivo binário original para leitura
with open(input_file_path, 'rb') as file:
    # Lendo os bytes antes do bloco a ser substituído
    before_block = file.read(block_start_position)
    
    # Debug: Mostrar a posição atual do cursor antes de ler os bytes antes do bloco
    print(f'Posição atual do cursor antes de ler os bytes antes do bloco: {file.tell()}')
    
    # Posicionando no byte 20 para ler os 4 bytes big-endian e modificar o valor
    file.seek(offset_position)
    original_value_bytes = file.read(4)
    original_value = struct.unpack('>I', original_value_bytes)[0] - subtract_value
    
    # Debug: Mostrar a posição atual do cursor depois de posicionar em offset_position
    print(f'Posição atual do cursor depois de posicionar em offset_position: {file.tell()}')
    
    # Calculando o tamanho do bloco a ser substituído
    block_length = original_value
    
    # Debug: Mostrar o tamanho do bloco a ser substituído
    print(f'Tamanho do bloco a ser substituído: {block_length}')
    
    # Posicionando no início do bloco de bytes a ser substituído
    file.seek(block_start_position)
    
    # Debug: Mostrar a posição atual do cursor antes de ler os bytes antes do bloco
    print(f'Posição atual do cursor antes de ler o bloco a ser substituído: {file.tell()}')
    
    # Lendo os bytes após o bloco a ser substituído
    file.seek(block_start_position + block_length)
    after_block = file.read()

    # Debug: Mostrar a posição atual do cursor depois de ler o bloco a ser substituído
    print(f'Posição atual do cursor depois de ler o bloco a ser substituído: {file.tell()}')

    # Debug: Mostrar o comprimento de after_block lido
    print(f'Comprimento de after_block lido: {len(after_block)}')

# Lendo o bloco de substituição do arquivo Loki.strdb.txt
with open(replacement_file_path, 'rb') as replacement_file:
    replacement_file.seek(2)
    replacement_block = replacement_file.read()

# Substituindo os bytes no bloco de substituição
modified_replacement_block = replacement_block.replace(old_bytes, new_bytes)

# Calculando o novo valor a ser escrito em offset_position
new_value = len(modified_replacement_block) + 161532
new_value_bytes = struct.pack('>I', new_value)

# Abrindo um novo arquivo binário para escrita
with open(output_file_path, 'wb') as output_file:
    # Gravando os bytes antes do bloco
    output_file.write(before_block)
    # Gravando o bloco de substituição modificado
    output_file.write(modified_replacement_block)
    # Gravando os bytes após o bloco
    output_file.write(after_block)
    # Posicionando no byte 20 para escrever o novo valor em big-endian
    output_file.seek(offset_position)
    output_file.write(new_value_bytes)

print(f'Bloco de bytes substituído e salvo em "{output_file_path}"')
print(f'Novo valor {new_value} escrito na posição {offset_position} em formato big-endian')
