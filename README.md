# SafeControl-Master-Nadzoru2

A simulação se tornou uma ferramenta essencial para a elaboração e execução de projetos elétricos complexos. Além disso, ela também é a única ferramenta robusta o suficiente para examinar sistematicamente o impacto de variáveis chaves no projeto. As simulações podem ser divididas em dois grupos, as em tempo contínuo (i) e as em tempo discreto (ii), sendo a segunda a utilizada no presente trabalho.
	
A Simulação em Eventos Discretos (SED), como o próprio nome já diz, modela um sistema discretizando ele no tempo, isto é, ao invés de simular todo o sistema continuamente, é feita a quantização do sistema em eventos que ocorrem em instantes de tempos específicos. Dessa maneira, é possível descartar eventos irrelevantes para o propósito final da simulação.

A pesquisa tem como intuito atualizar o algoritmo SafeControl-Master, que foi realizado pela Ludimilla Freitas com base no software já realizado pela Giovanna Sponchiado. O algoritmo elaborado consistia em, a partir de autômatos exportados em formato .xml pela ferramenta Nadzoru, verificar se ele é diagnosticável, diagnosticável seguro, prognosticável, prognosticável seguro, controlável seguro pela diagnose, controlável seguro pela prognose e controlável seguro pela diagnose ou pela prognose simultaneamente, caracterizando assim um autômato DP - Controlável Seguro. Entretanto, ele não funcionava para quando, para uma mesma falha, há mais de uma cadeia possível que leve a mesma, sendo esse problema a atualização realizada nesta pesquisa. 

A metodologia utilizada para  atualização do algoritmo, pode-se observar a Figura X. Nela é possível observar que não existe um fim na atualização dele, pois sempre é possível elaborar mais autômatos para testar, e como existem diversas maneiras de criar um, sempre haverá uma tipologia específica que o algoritmo não está levando em consideração, sendo necessário assim uma nova atualização de funções ou até módulos inteiros.

