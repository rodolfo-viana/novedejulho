import requests as req

from ndj_toolbox.fetch import (xml_df, save_files)

url_base = 'http://www.al.sp.gov.br/repositorioDados/'
url_file = 'processo_legislativo/comissoes_permanentes_reunioes.xml'
url = url_base + url_file


def main():
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()
    dataset = dataset[[
        'IdReuniao', 'IdComissao', 'IdPauta',
        'NrLegislatura', 'NrConvocacao', 'TipoConvocacao',
        'Data', 'CodSituacao', 'Situacao', 'Presidente'
    ]]
    dataset = dataset.rename(columns={
        'IdReuniao': 'id_reuniao',
        'IdComissao': 'id_comissao',
        'IdPauta': 'id_pauta',
        'NrLegislatura': 'nr_legislatura',
        'NrConvocacao': 'nr_convocacao',
        'TipoConvocacao': 'tp_convocacao',
        'Data': 'dt_reuniao',
        'CodSituacao': 'cd_situacao',
        'Situacao': 'ds_situacao',
        'Presidente': 'nm_presidente'
    })
    save_files(dataset, 'comissoes_reunioes')


if __name__ == '__main__':
    main()
