import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/palavras_chave.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[['IdPalavra', 'Palavra', 'PalavraSemAcento']]
    dataset = dataset.rename(columns={
        'IdPalavra': 'id_palavra', 'Palavra': 'termo',
        'PalavraSemAcento': 'termo_sem_acento'
    })
    save_files(dataset, 'indice_proposicoes_palavras-chave')


if __name__ == '__main__':
    main()
