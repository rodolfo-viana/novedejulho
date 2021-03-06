from utils.parse_xml import ParseXml
from utils.funcs import type_cols, save
import requests as r

url_base = 'https://www.al.sp.gov.br/repositorioDados/administracao/'
url_file = 'funcionarios_cargos.xml'


def main():
    dataset = ParseXml(r.get(url_base + url_file).content).process()
    dataset = type_cols(dataset, 'config/servs_geral.json')
    save(dataset, 'servs_geral')


if __name__ == '__main__':
    main()
