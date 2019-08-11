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

      >>> from src.data import make_dataset as mkdata
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



class ColetorDadosEpisodio():
    def __init__(self, url):
        self.ep_url = url
        self.sopa = parse_pagina(self.ep_url)
        self.titulo = ''
        self.conteudos = []
        self.topicos = []
        self.assuntos = []
        self.perolas = []
        self.num_participantes = 0
        self.num_convidados = 0
        self.participantes = []
        self.nomes_participantes = []
        self.nomes_convidados = []

    def serializado(self):
        dados = self.__dict__.copy()
        for tag in ['sopa', 'conteudos', 'participantes']:
            dados.pop(tag)
        return dados

    def conta_participantes(self):
        return len(self.sopa.find_all('img', style=re.compile("border-radius: 50%;")))

    def busca_conteudos(self, html_tag, tag='', lim_max=0, lim_min=0):
        if not tag:
            tag = self.sopa
        if lim_max and lim_min:
            conteudos = tag.find_all(html_tag)[lim_min:lim_max]
            return conteudos
        if lim_max:
            conteudos = tag.find_all(html_tag)[:lim_max]
            return conteudos
        conteudos = tag.find_all(html_tag)
        return conteudos

    def busca_texto(self, tag):
        """Método que retorna o texto de uma tag

        Parâmetros::

        :param tag: bs4.Tag, uma tag

        Retornos::

        :returns: um texto
        :rtype: str

        Uso::

          >>> busca_texto(tag)
        """
        return tag.__getattribute__('text')

    def busca_textos(self, conteudos):
        """Método que retorna uma lista de textos contidos em uma lista de tags

        Parâmetros::

        :param conteudos: [bs4.Tag], uma lista de tags

        Retornos::

        :returns: lista de strings
        :rtype: list

        Uso::

          >>> busca_itens(conteudos)
        """
        itens = []
        for conteudo in conteudos:
            itens.append(conteudo.__getattribute__('text'))
        return itens

    def busca_href(self, conteudo):
        """Método que retorna o texto de uma tag `a` e o seu conteudo textual

        Parâmetros::

        :param conteudo: bs4.Tag, uma tag do tipo `a`

        Retornos::

        :returns: uma tupla contendo o texto e o link da tag
        :rtype: tuple

        Uso::

          >>> busca_href(tag)
        """
        return (conteudo.__getattribute__('text'),
                conteudo.__getattribute__('attrs').__getitem__('href'))

    def busca_links(self, conteudos):
        itens = []
        for conteudo in conteudos:
            itens.append(self.busca_href(conteudo))
        return itens

    def arrasta(self):
        self.titulo = self.busca_texto(self.busca_conteudos('h2', lim_max=1)[0])
        self.conteudos = self.busca_conteudos('ul', lim_max=4, lim_min=1)
        self.topicos = self.busca_textos(self.busca_conteudos('li', self.conteudos[0]))
        self.assuntos = self.busca_links(self.busca_conteudos('a', self.conteudos[1]))
        self.perolas = self.busca_textos(self.busca_conteudos('li', self.conteudos[2]))

        self.num_participantes = self.conta_participantes()
        self.num_convidados = self.num_participantes - 3
        self.participantes = self.busca_conteudos('h3', lim_max=self.num_participantes)
        self.nomes_participantes = self.busca_textos(self.participantes)
        self.nomes_convidados = self.nomes_participantes[3:]
