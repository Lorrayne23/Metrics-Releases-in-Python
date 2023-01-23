<div align="justify">
# Analysis of Static Metrics Across Releases in Python Language Repositories on GitHub

This repository is part of the Interdisciplinary Work at the institution Puc minas. It aims to answer the following questions:
 
  * With each release of the python software, is there an increase in raw metrics?
  * With each release, do the systems become easier to read and less risky to change?
  * Does creating releases decrease system maintainability?
  
With this, the static metric analyzes considered in this work will be obtained for a set of 300 systems that use the Python programming language. They will be extracted from the GitHub version control system, being chosen the Python systems that have at least 10 releases. The tool used to perform the metric analysis will be Radon.
 
To obtain the measurement data presented in this work, was necessary download the code of 300 python systems. For this, the github graphql tool was used, which allows, through the web service API, to download information from the repositories. Then a script was developed to automate the cloning of repositories. And finally, we develop a program in charge of going through each of these systems, carrying out the measurements using the Radon tool and building a table where all these measurements were recorded. 

## Team Members
* André Murilo Neves Vasconcelos
* Leonardo Antunes Barreto Noman
* Lorrayne Reis Silva
* Paulo Henrique Cota Starling
* Victor Augusto dos Santos

## Teachers

* Humberto Torres Marques Neto


Link to acess the project in overlaf: https://www.overleaf.com/project/6281378431d6a3512e481623

<div>
