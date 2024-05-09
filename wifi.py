import numpy as np
import json

def decode_barker_code(data, barker_code, n_repeats):
    """ Декодировать данные с использованием кода Баркера. """
    code_length = len(barker_code)
    repeat_length = code_length * n_repeats
    decoded_bits = []

    for i in range(0, len(data), repeat_length):
        segment = data[i:i+repeat_length]
        if len(segment) != repeat_length:
            continue  # Игнорировать последний неполный сегмент
        avg_values = np.mean(segment.reshape(-1, n_repeats), axis=1)
        bit = 1 if np.correlate(avg_values, barker_code) > 0 else 0
        decoded_bits.append(bit)
    
    return np.array(decoded_bits)

def bits_to_string(bits):
    """ Преобразовать массив битов в строку ASCII. """
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            continue  # Игнорировать последний неполный байт
        char = chr(int(''.join(map(str, byte)), 2))
        chars.append(char)
    
    return ''.join(chars)

# Обновленный код Баркера
barker_code = np.array([1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1])

# Чтение данных из файла
with open('hello.dat', 'r') as file:
    data = np.array([float(line.strip()) for line in file])

# Декодирование данных
decoded_bits = decode_barker_code(data, barker_code, 5)

# Преобразование битов в ASCII строку
decoded_message = bits_to_string(decoded_bits)

# Запись результатов в JSON-файл
with open('wifi.json', 'w') as json_file:
    json.dump({"message": decoded_message}, json_file)

print("Декодирование завершено. Сообщение сохранено в файле 'wifi.json'.")
