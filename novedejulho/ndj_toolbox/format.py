# Precisa documentar essas funções!


def remove_break_line(text):
    try:
        return text.replace('\n', '')
    except:  # 'Bare except' não está de acordo com PEP 8 (E722)
        return text


def sanitize_float(item):
    return float(item.get_text().strip().replace('.', '').replace(',', '.'))
