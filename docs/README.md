# Documentação

## Visão Geral

> ![Competidores, robôs e mapa da RCB Challenge na CBR 2024](/docs/assets/cbr2024.png)
> Competidores, robôs e mapa da RCB Challenge na CBR 2024.

Este repositório contém o código desenvolvido pela equipe Roboforge para dois robôs que competiram na categoria RoboCup Brasil Challenge da CBR 2024. O robô nomeado "sandy-junior", que competiu na modalidade KIT, que restringe os materiais para apenas de kits educacionais de um único fabricante, e o nomeado "lilo-stitch", que competiu na modalidade OPEN, sem restrições de materiais.

Ambas as equipes, de cada um dos robôs, conquistaram o 4º lugar em suas respectivas modalidades.

Os Teams Description Papers (artigos descritivos das equipes) estão disponíveis neste repositório, na pasta `/docs/tdps`. Vale lembrar que eles descrevem os planos preliminares do desenvolvimento dos robôs da equipe, e foram escritos meses antes da competição. Desde a entrega até o evento os projetos de ambos os robôs sofreram alterações, mas os TDPs descrevem o ponto de partida inicial de cada um deles (para referência, essa documentação foi escrita após a participação na competição).

> A Equipe Roboforge submeteu artigos para possivelmente competir em 3 sub-equipes, uma na modalidade OPEN e duas na modalidade KIT, mas na competição em si apenas uma das equipes KIT realmente participou, a com o TDP nomeado como "KIT-1".

- [TDP Roboforge OPEN](/docs/tdps/tdp_roboforge_cbr_2024_open.pdf)
- [TDP Roboforge Kit-1](/docs/tdps/tdp_roboforge_cbr_2024_kit_1.pdf)
- [TDP Roboforge Kit-2 (não competiu)](/docs/tdps/tdp_roboforge_cbr_2024_kit_2.pdf)

# O desafio

Na competição, robôs que representam carros autônomos, em lados opostos do mapa que simula uma cidade, devem competir entre si para levar passageiros (tubos coloridos, que se encontram na zona de embarque central) aos seus respectivos pontos de destino, que são determinados pela cor e tamanho desses tubos. Além do cenário estático previamente conhecido, durante as partidas também podem ser adicionados ou retirados obstáculos como impedidores de vias (representados por caixas de leite) e/ou lombadas. Você pode conferir o documento descritivo das regras da competição clicando [aqui](/regras.pdf).

> ![Vista superior da arena da competição](/docs/assets/arena.png)
> Vista superior da arena da competição.

# Os robôs

Em ambas as modalidades foram utilizados robôs construídos principalmente com peças do kit LEGO Mindstorms EV3. Na modalidade OPEN, o robô conta com peças especiais extras: um conjunto de 4 rodas "mecanum", que permite que o robô possa se mover de forma omnidirecional, um sensor de cor HiTechnic, e ligas de borracha para maior aderência na pinça da garra. Como ambos os robôs contém 2 controladores EV3, eles levam nomes de duplas escolhidos pela equipe.

O robô da modalidade KIT é o "Sandy&Junior" e o da modalidade OPEN é o "Lilo&Stitch".

> Em geral os robôs das competições sofrem alterações em sua estrutura e composição física com frequência em vários momentos da preparação e participação na competição. Os aspectos mostrados a seguir descrevem o conceito de cada robô, que cada versão diferente de base e estrutura montada sempre tentava respeitar.

> Essa documentação é focada mais nos aspetos de Software do que de Hardware envolvidos, então não abordará detalhes das montagens.

## Sandy & Junior

Composição:

- 2 motores grandes para movimentação de 2 rodas;
- 2 sensores de cor apontados para o solo, à frente das rodas nas laterais do robô;
- 1 sensor infravermelho na lateral esquerda, apontado para fora, para varredura da área de embarque;
- 1 sensor ultrassônico frontal, apontado para frente, para detecção de obstáculos;
- uma garra com 2 graus de liberdade ("abre-fecha" e "sobe-desce") e 2 sensores acoplados (cor e ultrassônico), para detecção da cor e tamanho associados ao passageiro a bordo.

#TODO adicionar imagem

## Lilo & Stitch

Composição:

- 4 motores grandes para movimentação das 4 rodas omnidirecionais;
- 4 sensores de cor apontados para o solo em cada extremidade do robô;
- 2 sensores ultrassônicos para detecção de obstáculos nas partes dianteira e traseira do robô;
- uma garra com 2 graus de liberdade ("abre-fecha" e "sobe-desce") com um sensor de distância (inicialmente ultrassônico, posteriormente infravermelho) acoplado para detecção do passageiro a bordo;
- e um sensor de cor HiTechnic na lateral direita, apontado para fora, para varredura da área de embarque e detecção das cores associadas aos passageiros.

> ![Lilo&Stitch no mapa da CBR 2024](/docs/assets/lilostich.png)
> Lilo&Stitch no mapa da CBR 2024

# Estrutura do código (src)

#TODO
