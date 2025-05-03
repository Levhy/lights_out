# Lights Out

Ez a *Lights out* nevezetű logikai játék rekreációja, beépített solver-rel.

### Készítették:
- Erdei Zsófia
- Országh Júlia
- Molnár Levente

## Futtatás

A lights_out.py fájl futtatásával indítható el a játék.

### Futtatási előfeltételek:

- [Python 3.8+](https://www.python.org/downloads/)
- [Pygame](https://www.pygame.org/wiki/GettingStarted)
- [Numpy](https://numpy.org/install/)

## A Játék Működése

A játék egy *n*x*n*-es (tradícionálisan *5*x*5*-ös) táblázatból áll, ahol minden mező egy lámpa.
Egy lámpa lehet fel- vagy lekapcsolt állapotban és egyre rányomva az és a vele (nem átlósan) szomszédos lámpák állapotot váltanak.
Kezdetben valamennyi lámpa fel van kapcsolva, és a játék célja lekapcsolni az összeset.

## Lehetséges megoldási módszerek

Mátrixos lineáris algebrával. Meg ilyen Gauss-elimináció-szerű. Mint az utóbbit használjuk. Említendően 4 ekvivalens megoldás van.

## A solver logikája
Leviszi az aljára, algoritmikusan visszavezeti hogy melyikeket kell felül megnyomni. Végén a lámpánkénti kapcsolási számot elosztjuk maradékosan kettővel, mert vagy megnyomunk egy lámpát egy megoldásban, vagy nem.
## Hogy kell játszani?
### 3x3
### 5x5
### 6x6
 
