import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

'''
Documentação:
al.sp.gov.br/repositorioDados/docs/processo_legislativo/palavras_chave.pdf
'''

url_base = 'https://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
url_file = 'palavras_chave.xml'
url = url_base + url_file


def process_proposicoes_palavras():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['IdPalavra', 'Palavra', 'PalavraSemAcento']]
    dataset = dataset.rename(columns={
        'IdPalavra': 'id_palavra', 'Palavra': 'termo',
        'PalavraSemAcento': 'termo_sem_acento'
    })
    save_files(dataset, 'data', 'indice_proposicoes_palavras-chave')


if __name__ == '__main__':
    process_proposicoes_palavras()
