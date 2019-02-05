import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'https://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/comissoes_membros.xml'
url = url_base + url_file


def process_comissoes_membros():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'SiglaComissao', 'IdComissao', 'NomeMembro', 'IdMembro', 'Papel',
        'IdPapel', 'Efetivo', 'DataInicio', 'DataFim'
    ]]
    dataset = dataset.rename(columns={
        'SiglaComissao': 'sg_comissao', 'IdComissao': 'id_comissao',
        'NomeMembro': 'nm_membro', 'IdMembro': 'id_membro',
        'Papel': 'ds_papel', 'IdPapel': 'id_papel', 'Efetivo': 'efetivo',
        'DataInicio': 'dt_inicio', 'DataFim': 'dt_fim'
    })
    save_files(dataset, 'data', 'comissoes_membros')


if __name__ == '__main__':
    process_comissoes_membros()
