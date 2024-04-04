import re
def convert_to_bmp(text):
    bmp_text = ""
    for char in text:
        # Kiểm tra xem mã Unicode của ký tự có lớn hơn 0xFFFF không
        if ord(char) > 0xFFFF:
            # Nếu không có mã Unicode BMP tương ứng, thay thế bằng ký tự rỗng
             bmp_text += ''
        else:
            bmp_text += char
    return bmp_text
def find_nearest_punctuation_index(text, start_index, end_index):
    punctuation_indices = [m.start() for m in re.finditer(r'[.!?]', text[start_index:end_index])]
    if punctuation_indices:
        return start_index + max(punctuation_indices)
    else:
        return end_index

def cut_string(text, max_length=9300):
    text_convert = convert_to_bmp(text)
    # Nếu độ dài của chuỗi nhỏ hơn hoặc bằng max_length, trả về chuỗi ban đầu
    if len(text_convert) <= max_length:
        return [text_convert]

    # Tìm vị trí dấu câu gần nhất trước giới hạn max_length
    nearest_punctuation_index = find_nearest_punctuation_index(text_convert, 0, max_length)

    # Tạo danh sách các đoạn được cắt từ chuỗi
    cut_parts = [text_convert[:nearest_punctuation_index + 1].strip()]

    # Nếu chuỗi chưa được cắt hết, tiếp tục cắt cho đến khi hết
    while nearest_punctuation_index < len(text_convert):
        start_index = nearest_punctuation_index + 1
        nearest_punctuation_index = find_nearest_punctuation_index(text_convert, start_index, start_index + max_length)
        if nearest_punctuation_index < len(text_convert):
            cut_parts.append(text_convert[start_index:nearest_punctuation_index + 1].strip())

    return cut_parts