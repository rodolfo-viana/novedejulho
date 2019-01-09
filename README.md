# __Nove de Julho__

Nove de Julho é um projeto open-source de ativismo cívico com foco na Assembleia Legislativa do Estado de São Paulo.

Seu objetivo é agregar e formatar conjuntos de dados da Alesp, como gastos na cota parlamentar, proposições apresentadas, leis aprovadas, presenças em sessões, andamento de comissões, lista de funcionários, salários, entre outros.

Com desenvolvimento iniciado em janeiro de 2019, Nove de Julho é fortemente inspirado na [Operação Serenata de Amor](https://serenata.ai/).

### Fonte dos dados

Os dados são coletados diretamente da Alesp por meio do [Portal dos Dados Abertos](https://www.al.sp.gov.br/dados-abertos/).

Em breve serão incluidos no Nove de Julho scripts para coletar dados que não estão no portal, por meio de raspagem do site da Alesp.

### Roadmap

__Versão 0.0.1__<br>
__Foco:__ dados de deputados<br>
__Previsão de conclusão:__ segunda quinzena de jan.2019<br>

- [x] Funções e classes em `toolbox.py` para suportar `gasto_cota.py`
- [x] Script de aquisição de dados de gastos na cota (`gasto_cota.py`)
- [ ] Funções e classes em `formatting.py` para formatar dados obtidos com `gasto_cota.py`
- [ ] Funções e classes em `toolbox.py` para suportar `deputados.py`
- [ ] Script de aquisição de dados de deputados (`deputados.py`)
- [ ] Funções e classes em `formatting.py` para formatar dados obtidos com `deputados.py`
- [ ] Funções e classes em `toolbox.py` para suportar `atuacao.py`
- [ ] Script de aquisição de dados da área de atuação dos deputados (`atuacao.py`)
- [ ] Funções e classes em `formatting.py` para formatar dados obtidos com `atuacao.py`
- [ ] Funções e classes em `toolbox.py` para suportar `base_eleitoral.py`
- [ ] Script de aquisição de dados da área de atuação dos deputados (`base_eleitoral.py`)
- [ ] Funções e classes em `formatting.py` para formatar dados obtidos com `base_eleitoral.py`

__Versão 0.0.2__<br>
__Foco:__ dados de proposições<br>
__Previsão de conclusão:__ primeira quinzena de fev.2019<br>

### Licença MIT

Copyright (c) 2019 Rodolfo Viana

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
