import os
import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url = 'http://www.al.sp.gov.br/repositorioDados/deputados/despesas_gabinetes.xml'
arquivo = 'gastos_cota'
data_dir = 'data'


def create_dir():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def process_request():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['Deputado', 'Matricula', 'Ano', 'Mes',
                       'Tipo', 'Fornecedor', 'CNPJ', 'Valor']]
    dataset = dataset.rename(columns={
        'Deputado': 'deputado', 'Matricula': 'matricula',
        'Ano': 'ano', 'Mes': 'mes', 'Tipo': 'tipo',
        'Fornecedor': 'fornecedor', 'CNPJ': 'cnpj', 'Valor': 'valor'
    })
    save_files(dataset, data_dir, arquivo)


if __name__ == '__main__':
    create_dir()
    process_request()
