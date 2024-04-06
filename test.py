import re

# Mở file và đọc nội dung.
with open('./text_trans/chapter_1.txt.txt', 'r', encoding="utf-8") as f:
    text = f.read()

# Sử dụng re.sub() để ngắt dòng ở mỗi dấu ngắt câu không theo sau là dấu cách.

# Nó sẽ tìm tất cả các dấu ngắt câu (., !, ?, ;) không theo sau là dấu cách và thêm một dòng mới sau chúng.
# text = re.sub(r'(\.”\)([^ \n]))', r'\1\n\2', text)
text = re.sub(r'”', '”\n', text)
text = re.sub(r'([.!?;])([^ \n])', r'\1\n\2', text)

# Ghi nội dung đã được ngắt dòng vào file.
with open('./text_trans/chapter_1.txt.txt', 'w', encoding="utf-8") as f:
    f.write(text)