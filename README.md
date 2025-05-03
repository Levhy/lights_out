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

## A megoldás logikája

A játék táblázata tekinthető egy *n*x*n*-es (mod 2)-beli mátrixnak *((1 - ég; 0 - nem ég))*.  
Továbbá, a megoldás is egy ugyanilyen mátrix *((1 - megnyomjuk; 0 - nem nyomjuk meg))*, mivel egy gombot kétszer megnyomva nem változik a táblázat.

A solver a megoldáshoz a következő, Gauss-elimináció-szerű algoritmust alkalmazza:  
Mivel a megnyomott gomb a fölötte lévő lámpának is megváltoztatja az állapotát, ezért le lehet vezetni a fényeket, hogy csak az alsó sorban legyenek, úgy, hogy mindig a legmagasabban lévő fény alatti mezőt nyomjuk meg addig, amíg a fények nem csak az alsó sorban vannak.  
*Manuális kidolgoztuk, hogy ezután a lépés után melyik felső sorban lévő mezőket kell megnyomni, hogy az előző lépést megismételve az alsó sorban se égjenek fények.*  
A solver az első lépés után csak beolvassa az alsó sort, összepárosítja a felső soros megoldásával, és lefuttatja mégegyszer az első lépést.  
Az algoritmus során a solver végig tárolja, hogy hányszor lett megnyomva egy gomb, és a végén ezeket elosztja 2-vel maradékosan, ezzel megkapva a megoldási mátrixot.  

## Hogy kell játszani?

A játékot futtatva 2 lehetőség van:
### Solver mode
A *Solver mode* gombra kattintva és a táblázat méretet kiválasztva saját inputot lehet választani, amire a megoldást a *Solve* gombbal lehet megtekinteni.
### Play mode
A *Play mode* gombra kattintva és a táblázat méretét kiválasztva egy tetszőleges megjelenik egy random generált szimmetrikus input.  
A mezőkre kattintva lehet a (és a velük nem átlósan szomszédos) lámpák állapotát változtatni.  
A *Solve* gombra kattintva a jelenlegi állapot megoldását (melyik gombokat kell megnyomni) meg lehet kapni.
(Ha véletlen rossz gombot nyomsz meg, akkor a *Solve* gombot kétszer megnyomva megkaphatod a megoldását az új állapotnak)  
A *New* gombra kattintva pedig egy új inputot lehet kapni.
#### Misc
A *Back to main menu* gombbal a főmenübe lehet visszalépni, ahol újonnan lehet választani a 2 mód közt.  
A *Quit* gombbal lehet bezárni a programot.

