from utils.parse_xml import ParseXml
from utils.funcs import type_cols, save
import requests as r

url_base = 'https://www.al.sp.gov.br/repositorioDados/processo_legislativo/'
url_file = 'comissoes.xml'


def main():
    dataset = ParseXml(r.get(url_base + url_file).content).process()
    dataset = type_cols(dataset, 'config/coms_geral.json')
    save(dataset, 'coms_geral')


if __name__ == '__main__':
    main()
