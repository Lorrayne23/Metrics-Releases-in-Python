# Análise de Métricas Estáticas entre releases em repositórios  de linguagem Python no GitHub

Este repositorio faz parte do trabalho Trabalho Interdisciplinar de Software VI na instituição Puc minas. E tem como objetivo responder as seguintes questions:
 
  * A cada release do software python, existe o aumento de métricas brutas ?
  * A cada release, os sistemas se tornam mais fáceis de serem lidos e menos arriscados de serem modificados?
  * A criação de releases diminui a manutenibilidade do sistema?

Com isto, as  análises métricas estáticas consideradas neste trabalho serão obtidas para um conjunto de 300 sistemas que utilizam a linguagem de programação Python. Serão extraídos do sistema de controle de versão GitHub, sendo escolhidos os sistemas python que possuem, no mínimo, 10 releases. A ferramenta utilizada para efetuar as análises métricas será o Radon.
 
Para obter os dados de medição apresentados neste trabalho será necessário baixar o código de 300 sistemas python. Para isto será utilizado a ferramenta graphql do github que permite por meio de web service API, baixar informações dos repositórios. Então será desenvolvido um script para automatizar a clonagem dos repositórios. E por fim, desenvolver um programa encarregado de percorrer cada um desses sistemas, realizar as medidas por meio da ferramenta Radon e construir uma tabela onde foram registradas todas essas medidas. 

## Alunos integrantes da equipe
* André Murilo Neves Vasconcelos
* Leonardo Antunes Barreto Noman
* Lorrayne Reis Silva
* Paulo Henrique Cota Starling
* Victor Augusto dos Santos

## Professores responsáveis

* Humberto Marques

## Instruções de utilização

[Assim que a primeira versão do sistema estiver disponível, deverá complementar com as instruções de utilização. Descreva como instalar eventuais dependências e como executar a aplicação.]

https://www.python.org/

https://pypi.org/project/radon/

https://docs.github.com/pt/graphql

Link para acessar o artigo no overleaf: https://www.overleaf.com/project/6281378431d6a3512e481623
