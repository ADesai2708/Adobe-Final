import re
import unicodedata

def detect_script(text):
    for char in text:
        if char.strip():
            try:
                name = unicodedata.name(char)
                if "CJK" in name:
                    return "Chinese"
                elif "HIRAGANA" in name or "KATAKANA" in name:
                    return "Japanese"
                elif "HANGUL" in name:
                    return "Korean"
                elif "ARABIC" in name:
                    return "Arabic"
                elif "DEVANAGARI" in name:
                    return "Hindi"
                elif "CYRILLIC" in name:
                    return "Cyrillic"
                elif "LATIN" in name:
                    return "Latin"
            except ValueError:
                continue
    return "Unknown"

def is_multilingual_script(text):
    return detect_script(text)

def is_heading(text):
    if not text:
        return False

    if len(text.strip()) < 5 or len(text.split()) > 25:
        return False

    # Reject lines with too much repetition or only symbols
    if re.fullmatch(r"[\W_]+", text):
        return False

    if re.search(r"(\.{5,}|-{5,}|_{5,})", text):
        return False

    # Accept lines that start like section headings
    if re.match(r"^\d+(\.\d+)*\s+[A-Z]", text.strip()):
        return True

    if re.match(r"^[A-Z0-9][^\n]{0,100}$", text.strip()) and not text.strip().endswith("."):
        return True

    return False

def merge_lines(lines, y_tolerance=5):
    if not lines:
        return []

    lines.sort(key=lambda x: (x['page'], -x['font_size'], x['y0']))
    merged = []
    buffer = []
    last_y = None
    last_font = None
    last_page = None

    for line in lines:
        text = line['text'].strip()
        if not text:
            continue

        if (last_y is None or abs(line['y0'] - last_y) <= y_tolerance) and \
           (last_font is None or abs(line['font_size'] - last_font) <= 0.5) and \
           (last_page == line['page']):
            buffer.append(text)
        else:
            if buffer:
                merged.append((' '.join(buffer), last_font, last_page))
            buffer = [text]

        last_y = line['y0']
        last_font = line['font_size']
        last_page = line['page']

    if buffer:
        merged.append((' '.join(buffer), last_font, last_page))

    return merged
