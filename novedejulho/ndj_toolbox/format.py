import pandas as pd
from bs4 import BeautifulSoup


# Utilitário para transformar em float e converter vírgula em ponto

def sanitize_float(item):
    return float(item.get_text().strip().replace('.', '').replace(',', '.'))
