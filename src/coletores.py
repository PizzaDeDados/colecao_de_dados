import re

from bs4 import BeautifulSoup
from requests import get


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
            
    def parse_pagina(self, u=None):
        if not u:
            u = self.url
        req = get(u)
        decodificado = req.content.decode('utf-8')
        self.sopa = BeautifulSoup(decodificado, 'html.parser')

    def procura_proxima_pagina(self, s=None):
        #self.prox_pag = self.sopa.find_all('a', text=re.compile('Older'))
        if not s:
            s = self.sopa
        self.prox_pag = s.find_all('a', text=re.compile('Older'))
        if self.prox_pag:
            self.prox_pag = self.prox_pag[0].get('href')
    
    def arrasta(self):
        self.parse_pagina()
        self.coleta_links_episodios()
        self.procura_proxima_pagina()
        
        while self.prox_pag:
            self.parse_pagina(self.prox_pag)
            self.procura_proxima_pagina(self.sopa)
            self.coleta_links_episodios()