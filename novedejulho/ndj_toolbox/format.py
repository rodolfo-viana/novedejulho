# Precisa documentar essas funções!


def remove_break_line(text):
    try:
        return text.replace('\n', '')
    except:  # 'Bare except' não está de acordo com PEP 8 (E722)
        return text


def sanitize_float(item):
    return float(item.get_text().strip().replace('.', '').replace(',', '.'))

def remove_dep(dataset):
    # função que exclui 'Deputado' e 'Deputada' da coluna nm_presidente
    dataset.loc[dataset['nm_presidente'].str[0:8] == 'Deputado',
                'nm_presidente'] = dataset['nm_presidente'].str[8:].str.strip()

    dataset.loc[dataset['nm_presidente'].str[0:8] == 'Deputada',
                'nm_presidente'] = dataset['nm_presidente'].str[8:].str.strip()

    return dataset