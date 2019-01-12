## __Como usar os scripts__

Nove de Julho é um projeto escrito em Python. Para rodar os scripts são requisitos:

1. ter Python na sua máquina (versão 3),
2. instalar os módulos necessários
3. fazer o download dos scripts

Saber programação não é requisito, e este tutorial explica como você pode usar os arquivos.

### __Instalação de Python__

Python não vem "de fábrica" com Windows, e se você é usuário de MacOS ou Linux, possivelmente tem a versão 2.7 na sua máquina, que se tornará obsoleta em breve.

Para instalar o Python 3, que é a versão usada no projeto, siga este passo a passo:

1. Vá à [página oficial de download de Python](https://www.python.org/downloads/)
2. Faça o download da versão mais recente para seu sistema operacional (Windows, MacOS, Linux)
3. Clique no arquivo para começar a instalação
4. Durante a instalação, certifique-se de clicar nas opções "Install launcher for all users (recommended)" e "Add Python x.x to PATH"
5. Clique no botão "Install Now"
6. Quando aparecer a mensagem "Do you want the allow the following program to make changes to this computer?", escolha "Yes"
7. Uma janela de instalação irá aparecer. Quando a barra de progresso chegar ao fim, a instalação estará completa
8. Para checar se a instalação correu perfeitamente, vá ao console (aplicativo Terminal no MacOS e Linux, e Prompt de Comando no Windows) e digite `python --version` ou `python3 --version`, caso seu sistema seja MacOS ou Linux. Depois de pressionar `Enter`, você terá uma mensagem com a versão de Python que instalou -- por exemplo, `Python 3.6.5`. Isso significa que a instalação foi concluída com êxito

### __Instalação dos módulos__

Para rodar os scripts, você precisará ter alguns módulos de Python instalados na sua máquina. Não são muitos, e você pode consegui-los assim:

1. Abra o Terminal (MacOS e Linux) ou o Prompt de Comando (Windows)
2. Digite `pip install pandas requests beautifulsoup4`
3. Pressione `Enter`, e os módulos Pandas, Requests e BeautifulSoup serão instalados

### __Instalação dos scripts__

Os scripts do Nove de Julho podem ser baixados em [https://github.com/rodolfo-viana/novedejulho/archive/master.zip](https://github.com/rodolfo-viana/novedejulho/archive/master.zip).

1. Clique no link e faça o download
2. Descompacte o arquivo `.zip`. Será criada uma pasta chamada `novedejulho-master`, que contém os scripts

## __Como rodar os scripts__

Com o passo a passo anterior concluído:

1. Abra o Terminal (MacOS e Linux) ou o Prompt de Comando (Windows)
2. Vá até a pasta `novedejulho-master`
3. Dentro de `novedejulho-master` digite `cd novedejulho`
4. Dentro de `novedejulho` há os scripts. Para rodar, digite `python nomedoscript.py` (se não funcionar, digite `python3 nomedoscript.py`). Há três scripts prontos: `deputados.py` (para trazer dados dos deputados), `gasto_cota.py` (para obter dados de gastos efetuados por meio da verba de gabinete) e `salarios_servidores.py` (para retornar os nomes dos servidores e os valores recebidos desde 2014)
5. Aguarde até o script terminar de processar
6. Automaticamente será gerada a pasta `data`, com dois arquivos: um `.csv`, com os dados para serem abertos em processadores de planilhas como Excel e LibreOffice Calc, e um `.xz`, com os mesmo dados, mas para serem usados caso você pretenda trabalhar com Jupyter Notebook. Ambos os arquivos são idênticos.

Qualquer dúvida, mande uma DM no Twitter para @rodolfoviana. Estarei lá para ajudar. :)


