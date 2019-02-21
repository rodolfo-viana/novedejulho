import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)
from ndj_toolbox.format import clean_expenses_categories

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'deputados/despesas_gabinetes.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'Deputado', 'Matricula', 'Ano', 'Mes', 'Tipo', 'Fornecedor',
        'CNPJ', 'Valor'
    ]]
    dataset = dataset.rename(columns={
        'Deputado': 'nm_deputado', 'Matricula': 'nr_matricula',
        'Ano': 'ano', 'Mes': 'mes', 'Tipo': 'tp_categoria',
        'Fornecedor': 'nm_fornecedor', 'CNPJ': 'nr_cnpj', 'Valor': 'valor'
    })
    clean_expenses_categories(dataset)
    save_files(dataset, 'deputados_gastos_cota')


if __name__ == '__main__':
    main()
