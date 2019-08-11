import re

from bs4 import BeautifulSoup
from requests import get


def parse_pagina(url):
    """Este método faz a requisição da URL recebida e retorna um objeto
    BeautifulSoup com a página parseada.

    Parâmetros::

    :param url: string, URL da página a ser parseada

    Retornos::

    :returns: BeautifulSoup
    :rtype: bs4.BeautifulSoup

    Uso::

      >>> from src import make_dataset as mkdata
      >>> pagina = mkdata.parse_pagina('https://pizzadedados.com')
    """
    req = get(url)
    decodificado = req.content.decode('utf-8')
    return BeautifulSoup(decodificado, 'html.parser')


class ColetorLinksPizza():
    def __init__(self):
        self.url = 'https://podcast.pizzadedados.com/'
        self.links = []
        self.sopa = ''
        self.prox_pag = ''

    def coleta_links_episodios(self, sopa_de_letras=None):
        r = re.compile('Episódio')
        if not sopa_de_letras:
            sopa_de_letras = self.sopa
        for tag in sopa_de_letras.find_all('h2', text=r):
            self.links.append(tag.find('a').get('href'))

    def procura_proxima_pagina(self, s=None):
        if not s:
            s = self.sopa
        self.prox_pag = s.find_all('a', text=re.compile('Older'))
        if self.prox_pag:
            self.prox_pag = self.prox_pag[0].get('href')

    def arrasta(self):
        self.sopa = parse_pagina(self.url)
        self.coleta_links_episodios()
        self.procura_proxima_pagina()

        while self.prox_pag:
            self.sopa = parse_pagina(self.prox_pag)
            self.procura_proxima_pagina(self.sopa)
            self.coleta_links_episodios()
