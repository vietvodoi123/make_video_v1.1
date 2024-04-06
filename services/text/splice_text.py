import re

def convert_to_bmp(text):
    bmp_text = ""
    for char in text:
        if ord(char) > 0xFFFF:
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

def cut_string(text, max_length=9500):
    text_convert = convert_to_bmp(text)
    if len(text_convert) <= max_length:
        return [text_convert]

    nearest_punctuation_index = find_nearest_punctuation_index(text_convert, 0, max_length)
    cut_parts = [text_convert[:nearest_punctuation_index + 1].strip()]

    while nearest_punctuation_index < len(text_convert):
        start_index = nearest_punctuation_index + 1
        nearest_punctuation_index = find_nearest_punctuation_index(text_convert, start_index, start_index + max_length)
        if nearest_punctuation_index < len(text_convert):
            cut_parts.append(text_convert[start_index:nearest_punctuation_index + 1].strip())

    return cut_parts

# def translate_text_parts(text_parts):
#     translated_parts = []
#     for part in text_parts:
#         translated_part = GoogleTranslator(source='auto', target='vietnamese').translate(part)
#         translated_parts.append(translated_part)
#     return translated_parts