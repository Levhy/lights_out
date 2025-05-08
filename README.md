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
Egy lámpa lehet fel- vagy lekapcsolt állapotban és egyre rányomva az, és a vele (nem átlósan) szomszédos lámpák állapotot váltanak.
Kezdetben valamennyi lámpa fel van kapcsolva, és a játék célja lekapcsolni az összeset.  
Bizonyítottan nem minden kezdőpozíció megoldható *5*x*5*-ös esetben, de *3*x*3*-as és *6*x*6*-os táblázat esetén bármelyik állásból indulva le tudjuk kapcsolni az összes lámpát.

## A megoldás logikája

A játék táblázata tekinthető egy *n*x*n*-es (mod 2)-beli mátrixnak *((1 - ég; 0 - nem ég))*.  
Továbbá, a megoldás is, ha létezik, egy ugyanilyen mátrix *((1 - megnyomjuk; 0 - nem nyomjuk meg))*, mivel egy gombot páros sokszor megnyomva nem változik a táblázat.

A solver a megoldáshoz a következő, Gauss-elimináció-szerű algoritmust alkalmazza:  
Mivel a megnyomott gomb a fölötte lévő lámpának is megváltoztatja az állapotát, ezért le lehet vezetni a fényeket, hogy csak az alsó sorban legyenek, úgy, hogy mindig a legmagasabban lévő fény alatti mezőt nyomjuk meg addig, amíg a fények nem csak az alsó sorban vannak.  
*Manuális kidolgoztuk, hogy ezután a lépés után melyik felső sorban lévő mezőket kell megnyomni, hogy az előző lépést megismételve az alsó sorban se égjenek fények.*  
A solver az első lépés után csak beolvassa az alsó sort, összepárosítja a felső soros megoldásával, és lefuttatja mégegyszer az első lépést.  
Az algoritmus során a solver végig tárolja, hogy hányszor lett megnyomva egy gomb, és a végén ezeket elosztja 2-vel maradékosan, ezzel megkapva a megoldási mátrixot.  
Ha olyan alsó sort talál, melynek nincs felső soros párja, akkor a megoldás nem létezik, és ezt adja vissza a solver.  

## Hogy kell játszani?

A játékot futtatva megjelenik a főképernyő, amin 2 lehetőség közül választhatunk: *Solver mode* és *Play mode*

A *Solver mode*-ban egy adott input megoldását lehet lekérdezni, a Play mode-ban pedig magát a játékot lehet elindítani. Mindkét esetben a következő képernyőn kell kiválasztani a játékban szereplő táblázat méretét, amire kattintva rögtön el is indul a megfelelő módban a program. 

### Solver mode
Miután a *Solver mode* gombra kattintottunk és kiválasztottuk a méretet, egy üres (teljesen sötét) táblázat fogad, amibe megadhatjuk a megoldani kívánt állást. Ebben a módban egy lámpára való kattintás csak annak a mezőnek az állapotát változtatja meg, amire kattintottunk. Ha bevittük megoldandó állapotot, akkor a megoldást a *Solve* gombbal lehet megtekinteni: a pirossal kijelölt mezőkre nyomással lehetne megnyerni a játékot.  
Ha egy választott inputnak nincs megoldása (ez csak *5*x*5*-ös játék esetén fordul elő), akkor a program a *Not Solvable* szöveget jeleníti meg.   
A megoldás megjelenítése után a *Clear* gombbal lehet törölni ez eddigi inputot, és alapállapotba helyezni a táblázatot.
### Play mode
A *Play mode* gombra kattintva és a táblázat méretét kiválasztva, már rögtön egy kezdőállás jelenik meg a képernyőn. Ez egy random generált középpontosan szimmetrikus input, mert ezek mindig megoldhatóak az *5*x*5*-ös esetben is (ennek ellenőrzésére készült a symm_solvability nevű program).  
A mezőkre kattintva lehet azoknak (és a velük nem átlósan szomszédos) lámpáknak az állapotát változtatni.  
A *Help* gombra kattintva a jelenlegi állapot megoldását lehet megkapni: a pirossal kijelölt mezőkre nyomva az összes fény lekapcsolt állapotban lesz. A gombra mégegyszer kattintva el is lehet rejteni ezt. Következő kattintásra megintcsak a jelenlegi pozíció megoldását mutatja.    
A *New* gombra kattintva pedig egy új inputot lehet kapni.
#### Misc
A *Back to main menu* gombbal a főmenübe lehet visszalépni, ahol újonnan lehet választani a 2 mód közt.  
A *Quit* gombbal lehet bezárni a programot.

## Példák

### Solver mode

![Solver mode](https://github.com/Levhy/lights_out/blob/main/lights_out_pl_solver.gif)

### Play mode

![Play mode](https://github.com/Levhy/lights_out/blob/main/lights_out_pl_play.gif)

