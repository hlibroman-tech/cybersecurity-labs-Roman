from PIL import Image
import os

def text_to_binary(text):
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

def binary_to_text(binary_data):
    byte_segments = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    text_bytes = bytearray(int(byte, 2) for byte in byte_segments)
    try:
        return text_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return

def hide_message(image_path, message, output_path):
    try:
        img = Image.open(image_path).convert('RGB')
        encoded_img = img.copy()
        width, height = img.size
        
        message_with_delimiter = message + "$$END$$"
        binary_message = text_to_binary(message_with_delimiter)
        
        message_length = len(binary_message)
        
        max_bytes = width * height * 3
        if message_length > max_bytes:
            raise ValueError("Повідомлення занадто велике для цього зображення!")
            
        data_index = 0
        
        for y in range(height):
            for x in range(width):
                pixel = list(img.getpixel((x, y)))
                
                for i in range(3):
                    if data_index < message_length:
                        channel_value = pixel[i]
                        message_bit = int(binary_message[data_index])
                        pixel[i] = (channel_value & ~1) | message_bit
                        data_index += 1
                
                encoded_img.putpixel((x, y), tuple(pixel))
                
                if data_index >= message_length:
                    encoded_img.save(output_path)
                    return f"Повідомлення успішно приховано в '{output_path}'"

        encoded_img.save(output_path)
        return f"Повідомлення успішно приховано в '{output_path}'"

    except FileNotFoundError:
        return f"Помилка: Файл '{image_path}' не знайдено."
    except Exception as e:
        return f"Сталася помилка: {e}"

def extract_message(image_path):
    try:
        img = Image.open(image_path).convert('RGB')
        width, height = img.size
        
        binary_data = ""
        delimiter = text_to_binary("$$END$$")
        
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                
                for channel_value in pixel[:3]:
                    binary_data += str(channel_value & 1)
                    if binary_data.endswith(delimiter):
                        message_binary = binary_data[:-len(delimiter)]
                        return binary_to_text(message_binary)
                        
        return

    except FileNotFoundError:
        return f"Помилка: Файл '{image_path}' не знайдено."
    except Exception as e:
        return f"Сталася помилка при вилученні: {e}"
def main():
    while True:
        print("\n--- Меню Стеганографії ---")
        print("1. Приховати повідомлення (зашифрувати)")
        print("2. Вилучити повідомлення (розшифрувати)")
        print("3. Вийти з програми")
        choice = input("Ваш вибір (1-3): ")

        if choice == '1':
            try:
                input_image = input("Введіть шлях до вхідного зображення (напр., image.jpg): ")
                output_image = input("Введіть ім'я файлу для збереження (напр., encoded.png): ")
                
                if not output_image.lower().endswith('.png'):
                    print("\n[ПОПЕРЕДЖЕННЯ] Для надійного збереження даних рекомендується формат PNG.")
                    print("Формати як-от JPG можуть пошкодити приховане повідомлення через стиснення.")
                    confirm = input(f"Все одно зберегти як '{output_image}'? (так/ні): ").lower()
                    if confirm not in ['так', 'yes']:
                        print("Операцію скасовано.")
                        continue
                
                message = input("Введіть повідомлення, яке потрібно приховати: ")
                
                result = hide_message(input_image, message, output_image)
                print(f"\n{result}")
            except Exception as e:
                print(f"Сталася помилка під час приховування: {e}")

        elif choice == '2':
            try:
                input_image = input("Введіть шлях до зображення з повідомленням: ")
                result = extract_message(input_image)
                print(f"\nВилучене повідомлення: '{result}'")
            except Exception as e:
                print(f"Сталася помилка під час вилучення: {e}")

        elif choice == '3':
            print("Завершення роботи.")
            break
        else:
            print("Невірний вибір. Будь ласка, введіть 1, 2 або 3.")

if __name__ == "__main__":
    main()

