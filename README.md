# Coleção de dados e métricas do Pizza

## Estrutura do projeto

```
.
├── data
│   ├── processed            <-  Dados processados
│   └── raw                  <-  Dados originais e imutáveis
├── notebooks                <-  Jupyter notebooks. Padrão de nomenclatura é um número, as iniciais de quem criou,
│                                e uma descrição ex.: `1.0-jt-coleção-de-links.ipynb`.
├── README.md                <-  Arquivo README.md contendo as informações do projeto
├── requirements.txt         <-  Arquivo de instalação de bibliotecas Python necessárias pra reproduzir o ambiente de análises.
│                                gerado usando `pip freeze > requirements.txt`
├── setup.py                 <-  Definições do pacote `src` que torna ele instalável usando o `pip`
└── src                      <-  Módulo Python criado para este projeto
    ├── data                 <-  Código para gerar/coletar dados
    │   └── make_dataset.py
    └── __init__.py
```
