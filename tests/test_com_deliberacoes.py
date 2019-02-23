import requests as req

from novedejulho.ndj_toolbox.fetch import xml_df


def test_fetch_xml():
    global url
    url_base = 'https://www.al.sp.gov.br/repositorioDados/'
    url_file = 'processo_legislativo/comissoes_permanentes_deliberacoes.xml'
    url = url_base + url_file


def test_parse_xml():
    global dataset
    xml_data = req.get(url).content
    dataset = xml_df(xml_data).process_data()


def test_rename_columns():
    global dataset
    dataset = dataset[[
        'IdReuniao', 'IdDocumento', 'IdPauta', 'NrOrdem', 'DataInclusao',
        'DataSaida', 'Deliberacao', 'IdDeliberacao'
    ]]
    dataset = dataset.rename(columns={
        'IdReuniao': 'id_reuniao', 'IdDocumento': 'id_documento',
        'IdPauta': 'id_pauta', 'NrOrdem': 'nr_ordem',
        'DataInclusao': 'dt_inclusao', 'DataSaida': 'dt_saida',
        'Deliberacao': 'deliberacao', 'IdDeliberacao': 'id_deliberacao'
    })


def test_columns_names():
    assert list(dataset) == ['id_reuniao', 'id_documento', 'id_pauta',
                             'nr_ordem', 'dt_inclusao', 'dt_saida',
                             'deliberacao', 'id_deliberacao']


def test_columns_length():
    assert len(dataset['id_reuniao']) == len(dataset['id_documento'])


def test_null_values():
    for i in dataset['nr_ordem']:
        assert i != ''


def test_type():
    for j in dataset['deliberacao']:
        assert type(j) == str
