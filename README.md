# __Nove de Julho__

[![Maintainability](https://img.shields.io/codeclimate/maintainability-percentage/rodolfo-viana/novedejulho.svg)](https://codeclimate.com/github/rodolfo-viana/novedejulho/maintainability)
![](https://img.shields.io/badge/made%20with-%3C3-red.svg)

Nove de Julho é um projeto open-source de ativismo cívico com foco na Assembleia Legislativa do Estado de São Paulo.

Seu objetivo é agregar e formatar conjuntos de dados da Alesp, como gastos na cota parlamentar, proposições apresentadas, leis aprovadas, presenças em sessões, andamento de comissões, lista de funcionários, salários, entre outros.

Com desenvolvimento iniciado em janeiro de 2019, Nove de Julho é desenvolvido por [rodolfo-viana](https://github.com/rodolfo-viana) e conta com a colaboração de [cuducos](https://github.com/cuducos), [jtemporal](https://github.com/jtemporal) e [Vnicius](https://github.com/Vnicius).

### Fonte dos dados

Os dados são coletados diretamente da Alesp por meio do [Portal dos Dados Abertos](https://www.al.sp.gov.br/dados-abertos/) ou, quando não disponíveis no portal, por meio de raspagem do site oficial da assembleia.

### Conteúdo

`novedejulho.py` aciona mais de duas dezenas de scripts que fazem o download de dados como gastos feitos via verba de gabinete, salários dos servidores, presenças dos deputados em comissões, projetos apresentados etc.

Esses dados são salvos em arquivos `.csv` (para ler em Excel ou LibreOffice Calc) e `.xz` (para usar com Pandas). Também são agregados em um banco de dados `.db` (para acessar com SQL).

![Screenshot](https://i.imgur.com/7uUSyEn.png)

Outros scripts estão em produção, como para baixar contratos e convênios firmados pela Alesp.

### Como usar

__Não é preciso ter experiência com qualquer linguagem de programação para usar os scripts.__ Basta seguir as instruções detalhadas [aqui](https://github.com/rodolfo-viana/novedejulho/blob/master/INSTRUCOES_DE_USO.md).

Caso você tenha experiência com Python, basta clonar este repositório...

`$ git clone https://github.com/rodolfo-viana/novedejulho.git`

...e instalar as bibliotecas necessárias na pasta do projeto.

```
$ cd novedejulho
$ pip install -r requirements.txt
```

### To-do

- [ ] Alterar a função `generate_db` para inferir os tipos de dados
- [ ] Mapear o que mais pode ser raspado do site
- [ ] Criar scripts para os demais conjuntos que chegam como `.zip`

### Licença MIT

Copyright (c) 2019 Rodolfo Viana

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
