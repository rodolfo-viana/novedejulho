# __Nove de Julho__

[![Maintainability](https://img.shields.io/codeclimate/maintainability-percentage/rodolfo-viana/novedejulho.svg)](https://codeclimate.com/github/rodolfo-viana/novedejulho/maintainability)
[![Build Status](https://travis-ci.org/rodolfo-viana/novedejulho.svg?branch=master)](https://travis-ci.org/rodolfo-viana/novedejulho)
![](https://img.shields.io/badge/made%20with-%3C3-red.svg)

> Criação de [rodolfo-viana](https://github.com/rodolfo-viana)<br>
> Colaborações de [cuducos](https://github.com/cuducos), [jtemporal](https://github.com/jtemporal) e [Vnicius](https://github.com/Vnicius)<br>
> Desenvolvimento desde janeiro de 2019

Nove de Julho é um projeto open-source de ativismo cívico com foco na Assembleia Legislativa do Estado de São Paulo.

Seu objetivo é agregar e formatar conjuntos de dados da Alesp, como gastos na cota parlamentar, proposições apresentadas, leis aprovadas, presenças em sessões, andamento de comissões, lista de funcionários, salários, entre outros.

### Fonte dos dados

Os dados são coletados diretamente da Alesp por meio do [Portal dos Dados Abertos](https://www.al.sp.gov.br/dados-abertos/) ou, quando não disponíveis no portal, por meio de raspagem do site oficial da assembleia.

### Conteúdo

`novedejulho.py` aciona mais de duas dezenas de scripts que fazem o download de dados como gastos feitos via verba de gabinete, salários dos servidores, presenças dos deputados em comissões, projetos apresentados etc.

Pelo começo do nome dos arquivos é possível saber a qual categoria pertence cada script:

- `com` para dados de comissões (votações, sessões, preseças etc.)
- `dep` para dados de deputados (bases eleitorais, áreas de atuação, gastos na cota etc.)
- `doc` para dados de documentos (projetos de lei, autores, pareceres etc.)
- `leg` para dados de legislação (normas, anotações, temas etc.)
- `serv` para dados de servidores (lotações, cargos, salários etc.)

Alguns desses scripts terminam com `indice` no nome. Isso indica que os dados raspados por meio deles servem como `foreign keys` em agregações.

Todos os dados são salvos em arquivos `.csv` (para ler em Excel ou LibreOffice Calc) e `.xz` (para usar com Pandas). Também são agregados em um banco de dados `.db` (para acessar com SQL).

![Screenshot](https://i.imgur.com/GZlaKuJ.png)

Outros scripts estão em produção, como para baixar contratos e convênios firmados pela Alesp.

### Como usar

__Não é preciso ter experiência com qualquer linguagem de programação para usar os scripts.__ Basta seguir as instruções detalhadas [aqui](https://github.com/rodolfo-viana/novedejulho/blob/master/INSTRUCOES_DE_USO.md).

Caso você tenha algum conhecimento de Python, basta clonar este repositório...

```
$ git clone https://github.com/rodolfo-viana/novedejulho.git
```

...e instalar as bibliotecas necessárias na pasta do projeto.

```
$ cd novedejulho
$ pip install -r requirements.txt
```

### Como colaborar

Aos que desejam colaborar mas não sabem codar, uma forma muito grande de ajuda é mandando issues com bugs ou ideias para melhorar o projeto. Você pode [abrir uma issue aqui](https://github.com/rodolfo-viana/novedejulho/issues/new).

Se quiser colocar a mão em códigos e ajudar com aprimoramentos e correções, faça um fork do repositório no GitHub. Depois:

```
$ git clone https://github.com/{seu-nome-de-usuario}/novedejulho.git
```

Não esqueça de criar um branch com suas alterações...

```
$ git checkout -b {seu-nome-de-usuario}-{breve-descricao}
$ git commit -am "{Mensagem dizendo como alterou o original}"
$ git push origin {seu-nome-de-usuario}-{breve-descricao}
```

...E abrir um pull request no GitHub. Prometemos responder com agilidade.

Caso não tenha ideia de como contribuir, temos algumas sugestões:

- [ ] Alterar a função `generate_db`, em `format.py`, para inferir os tipos de dados
- [ ] Criar função em `format.py` para trocar sigla pela descrição em `tp_convocacao`, no script `com_reunioes.py`
- [ ] Criar função em `format.py` para eliminar "Deputado" e "Deputada" de `nm_presidente`, no script `com_reunioes.py`
- [ ] Criar função em `format.py` para deixar `nm_deputado`, do script `dep_gastos_cota.py`, em caixa alta e baixa
- [ ] Mapear o que mais pode ser raspado do site
- [ ] Criar scripts para os demais conjuntos que chegam como `.zip`

### Licença MIT

Copyright (c) 2019 Rodolfo Viana
