def remove_break_line(i):
    """Remove quebra de linha em série:

    >> remove_break_line(df[x])

    :param i: (serie / var) série ou variável onde há quebra de linha
    :return: (serie / var) série ou variável sem quebra de linha
    """
    try:
        return i.replace('\n', '')
    except:  # 'Bare except' não está de acordo com PEP 8 (E722)
        return i


def sanitize_float(i):
    """Altera vírgula por ponto para se adequar aos processadores:

    >> sanitize_float(x)
    'x = 10.99'

    :param i: (val) valor com vírgula
    :return: (val) valor com ponto
    """
    return float(i.get_text().strip().replace('.', '').replace(',', '.'))


def remove_dep(i):
    """Remove os termos 'Deputado' e 'Deputada' da coluna nm_presidente
    (referência: 'coms.py'):

    >> remove_dep(x)

    :param i: (var) variável do dataframe
    :return: (var) variável do dataframe com a alteração
    """
    i.loc[i['nm_presidente'].str[0:8] == 'Deputado',
          'nm_presidente'] = i['nm_presidente'].str[8:].str.strip()

    i.loc[i['nm_presidente'].str[0:8] == 'Deputada',
          'nm_presidente'] = i['nm_presidente'].str[8:].str.strip()

    return i
