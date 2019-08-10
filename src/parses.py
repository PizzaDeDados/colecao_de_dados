from bs4 import BeautifulSoup
from requests import get


def parse_pagina(u):
    req = get(u)
    decodificado = req.content.decode('utf-8')
    return BeautifulSoup(decodificado, 'html.parser')