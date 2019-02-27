## __Como colaborar__

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
- [ ] Criar função em `format.py` para trocar as siglas pelas descrições em `tp_convocacao`, no script `com_reunioes.py`
- [ ] Criar função em `format.py` para eliminar "Deputado" e "Deputada" de `nm_presidente`, no script `com_reunioes.py`
- [ ] Criar função em `format.py` para deixar `nm_deputado`, do script `dep_gastos_cota.py`, em caixa alta e baixa
- [ ] Criar função em `format.py` para trocar os dígitos pelas descrições em `id_tp_relacionada`, no script `leg_anotacoes.py`
- [ ] Mapear o que mais pode ser raspado do site
- [ ] Criar scripts para os demais conjuntos que chegam como `.zip`
