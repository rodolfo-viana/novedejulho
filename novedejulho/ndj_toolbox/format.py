# Utilitário para transformar em float e converter vírgula em ponto

def sanitize_float(item):
    return float(item.get_text().strip().replace('.', '').replace(',', '.'))


# Utilitário para limpar a coluna 'tipo' - ref.: deputados_gastos_cota.py

def clean_expenses_categories(df):
    df['tipo'].replace({'A - COMBUSTÍVEIS E LUBRIFICANTES': 'COMBUSTÍVEIS E LUBRIFICANTES',
                        'B - LOCAÇÃO E MANUT DE BENS MÓVEIS E IMÓVEIS, CONDOMÍNIOS E OUTROS': 'LOCAÇÃO E MANUTENÇÃO DE BENS MÓVEIS, IMÓVEIS E CONDOMÍNIO',
                        'C - MATERIAIS E SERVIÇOS DE MANUT E CONSERV DE VEÍCULOS ; PEDÁGIOS': 'MANUTENÇÃO DE VEÍCULOS E PEDÁGIOS',
                        'D - MATERIAIS E SERVIÇOS GRÁFICOS, DE CÓPIAS  E REPRODUÇÃO DE DOCS': 'SERVIÇOS GRÁFICOS',
                        'E - MATERIAIS DE ESCRITÓRIO E OUTROS MATERIAIS DE CONSUMO': 'MATERIAL DE ESCRITÓRIO',
                        'F - SERVIÇOS TÉCNICOS PROFISSIONAIS (CONSULTORIA, PESQUISAS ETC)': 'SERVIÇOS TÉCNICOS E CONSULTORIAS',
                        'G - ASSINATURAS DE PERIÓDICOS, PUBLICAÇÕES E INTERNET': 'ASSINATURA DE JORNAIS, REVISTAS E INTERNET',
                        'H - SERV.UTIL.PÚBLICA (TELEF.MÓVEL/FIXA, ENERGIA, ÁGUA, GÁS ETC)': 'TELEFONE, ENERGIA, ÁGUA E OUTROS SERVIÇOS',
                        'I - HOSPEDAGEM, ALIMENTAÇÃO E DESPESAS DE LOCOMOÇÃO': 'ALIMENTAÇÃO, HOSPEDAGEM E LOCOMOÇÃO',
                        'J - SERVIÇOS DE COMUNICAÇÃO': 'SERVIÇOS DE COMUNICAÇÃO',
                        'K - LOCAÇÃO DE BENS MÓVEIS': 'LOCAÇÃO DE BENS MÓVEIS',
                        'L - LOCAÇÃO DE BENS IMÓVEIS': 'LOCAÇÃO DE IMÓVEIS',
                        'M - MANUTENÇÃO DE BENS MÓVEIS,  IMÓVEIS, CONDOMÍNIOS E OUTROS': 'MANUTENÇÃO DE BENS MÓVEIS, IMÓVEIS E CONDOMÍNIO',
                        'N - MORADIA': 'MORADIA'}, inplace=True)
