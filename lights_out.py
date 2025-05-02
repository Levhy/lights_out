import pygame
import sys
import numpy as np

pygame.init()
#inicializálás


#most rögzítek néhány színt változóként
color_white=(255,255,255)
color_yellow=(255,255,0)
color_black=(0,0,0)
color_dark=(16,60,62)
color_red=(255,0,0)


#Ahhoz hogy könnyen tudjunk lépkedni a képernyők között a következőt használom (innen:https://www.geeksforgeeks.org/how-to-use-multiple-screens-on-pygame/)
#megjegyzés: a program nem szerette úgy használni ahogy eredetileg meg volt írva, ezért módosítanunk kellett kicsit + amiket egyáltalán nem használunk kikommenteltem
class Screen():
    def __init__(self, title, width=360, height=360):
        #Minden képernyő ugyanazokat a méreteket használja, valójában csak a title az amit külön adunk meg mindig
        self.height = height
        self.title = title
        self.width = width
        #Ezzel a bool változóval tartjuk számon hogy éppen melyik képernyőn vagyunk és milyen működést kövessen a program
        self.CurrentState = False
    def makeCurrentScreen(self):
        pygame.display.set_caption(self.title)
        self.CurrentState = True
        screen.fill(color_black)
    def endCurrentScreen(self):
        self.CurrentState = False
    #def checkUpdate(self, fill):
    #    self.fill = fill  
    #    return self.CurrentState
    #def screenUpdate(self):
    #    if self.CurrentState:
    #        self.screen.fill(self.fill)
    #def returnTitle(self):
    #    return self.screen

#Ezzel a 4 képernyővel fogunk dolgozni (változó neve hogy hogyan hivatkozunk rá mi, és zárójelben az szerepel hogy a képernyő tetején mi lesz kiírva)
main_screen=Screen("Lights out")
game_screen_3=Screen("3x3")
game_screen_5=Screen("5x5")
game_screen_6=Screen("6x6")

#Ezzel a függvénnyel könnyítjük a gombok/ feliratok megjelenítését
#paraméterek jelentése sorrendben: határoló vonal színe, gomb színe amikor a kurzor rajta van, gomb színe amikor nincs
#bal oldal helyzete a képernyőn, top helyzete a képernyőn, szélesség, magasság
#felirat szövege, felirat bal szélének helyzete, felirat tetejének a helyzete, felirat színe
def ButtonVisuals(color_border, color1, color2, left, up, width, heigth, text, textl, textu, textcol):
    pygame.draw.rect(screen,color_border,[left-0.5,up-0.5,width+2,heigth+2])
    if left <= mouse[0] <= (left+width) and up <= mouse[1] <= (up+heigth):
        pygame.draw.rect(screen,color2,[left,up,width,heigth]) 
    else: 
        pygame.draw.rect(screen,color1,[left,up,width,heigth])
    screen.blit(smallfont.render(text,True,textcol), (textl,textu)) 


#Jelenleg ezekkel próbálom követni a lámpák közül a felkapcsoltakat
matrix_3=[0,0,0,0,0,0,0,0,0]
matrix_5=[0 for i in range(25)]
matrix_6=[0 for i in range(36)]

#Itt tárolom a 3x3-mas lámpák pozícióit (alatta: 5x5-öseké, majd 6x6-osoké)
#a gombok megjelenítésénél elég lesz ezekre az adatokra hivatkozni
pos_3=[]
for i in range(3):
    for j in range(3):
        pos_3.append([90+(j*(50+15)),40+i*(50+15)])

pos_5=[]
for i in range(5):
    for j in range(5):
        pos_5.append([91+(j*(30+7)),41+i*(30+7)])

pos_6=[]
for i in range(6):
    for j in range(6):
        pos_6.append([90+(j*(25+7)),40+i*(25+7)])


#Ezzel a függvénnyel fogjuk követni a megoldó módban a user-inputot. 
#Ezt majd az if ev.type==pygame.MOUSEBUTTONDOWN fül alatt hívjuk meg, és emiatt fogja azt csinélni, hogy ha a kiválasztott gombot megnyomjuk a képernyőn
#a megfelelő listában a gombhoz rendelt elem 0-ról 1-re v 1-ről 0-ra vált
def ButtonState(matrix, pos, size):
    for i in range(len(pos)):
        if  pos[i][0]<= mouse[0] <= pos[i][0]+size and pos[i][1] <= mouse[1] <= pos[i][1]+size:
            matrix[i]=(matrix[i]+1)%2

#Ez a következő szakasz a feladatmegoldó gombok működéséhez szükséges dolgokat állítják elő
#Először egy-egy listában manuálisan felvisszük melyik alsó sorhoz melyik felső sorbeli gombokat kell benyomni ahhoz,
#Hogy utána csak "toggle down" módszerrel megoldható legyen a feladat
#ezekből néhány függvény segítségével létrehozzuk azokat a dictionaryket, amik tárolják azt a gombsorozatot, ami egy csak alsó sorában
#világító feladványt megoldana

dict_3={}
#Ebben fogjuk tároni a 3x3-mas feladványok megoldókulcsait

solutions_3=[[[1,1,1],[0,1,0]],[[1,1,0],[1,0,0]],[[1,0,1],[1,0,1]],[[0,1,1],[0,0,1]],[[1,0,0],[0,1,1]],[[0,1,0],[1,1,1]],[[0,0,1],[1,1,0]]]
#A lista minden eleme kettő listát tartalmaz: az első mindig az hogy miket nyomunk be a felső sorban, a második pedig hogy ez melyik alsó sorbeli állást tudja neutralizálni

#hasonlóan 5x5 eset
#annyi eltéréssel, hogy itt nem minden alsó sor kombinációhoz van felső sor kombináció ami azt megoldja
dict_5={}

solutions_5=[[[0,0,0,0,0],[0,0,0,0,0]],[[0,1,0,0,0],[1,1,1,0,0]],[[0,0,0,1,0],[0,0,1,1,1]],[[0,0,1,0,0],[1,1,0,1,1]],[[0,0,0,0,1],[1,0,1,1,0]],[[1,0,0,0,0],[0,1,1,0,1]],[[1,1,0,0,0],[1,0,0,0,1]],[[1,0,0,1,0],[0,1,0,1,0]]]
#[[felső sorban benyomni],[alsó sorban látszik]]

#és a 6x6-os eset
dict_6={}

S_0 = [[[0,0,0,0,0,0],[0,0,0,0,0,0]]]
S_1 = [[[1,0,0,0,0,0],[1,0,0,0,1,0]],[[0,0,0,0,0,1],[0,1,0,0,0,1]],[[0,1,0,0,0,0],[0,1,0,1,0,1]],[[0,0,0,0,1,0],[1,0,1,0,1,0]],[[0,0,1,0,0,0],[0,0,0,0,1,0]],[[0,0,0,1,0,0],[0,1,0,0,0,0]]]
S_2 = [[[1,1,0,0,0,0],[1,1,0,1,1,1]],[[0,0,0,0,1,1],[1,1,1,0,1,1]],[[0,1,1,0,0,0],[0,1,0,1,1,1]],[[0,0,0,1,1,0],[1,1,1,0,1,0]],[[0,0,1,1,0,0],[0,1,0,0,1,0]],[[1,0,0,0,0,1],[1,1,0,0,1,1]],[[1,0,1,0,0,0],[1,0,0,0,0,0]],[[0,0,0,1,0,1],[0,0,0,0,0,1]],[[0,1,0,1,0,0],[0,0,0,1,0,1]],[[0,0,1,0,1,0],[1,0,1,0,0,0]],[[1,0,0,1,0,0],[1,1,0,0,1,0]],[[0,0,1,0,0,1],[0,1,0,0,1,1]],[[0,1,0,0,1,0],[1,1,1,1,1,1]],[[1,0,0,0,1,0],[0,0,1,0,0,0]],[[0,1,0,0,0,1],[0,0,0,1,0,0]]]
S_3 = [[[1,1,1,0,0,0],[1,1,0,1,0,1]],[[0,0,0,1,1,1],[1,0,1,0,1,1]],[[1,1,0,1,0,0],[1,0,0,1,1,1]],[[0,0,1,0,1,1],[1,1,1,0,0,1]],[[1,1,0,0,1,0],[0,1,1,1,0,1]],[[0,1,0,0,1,1],[1,0,1,1,1,0]],[[1,1,0,0,0,1],[1,0,0,1,1,0]],[[1,0,0,0,1,1],[0,1,1,0,0,1]],[[1,0,1,0,1,0],[0,0,1,0,1,0]],[[0,1,0,1,0,1],[0,1,0,1,0,0]],[[1,0,1,1,0,0],[1,1,0,0,0,0]],[[0,0,1,1,0,1],[0,0,0,0,1,1]],[[1,0,0,1,1,0],[0,1,1,0,0,0]],[[0,1,1,0,0,1],[0,0,0,1,1,0]],[[1,0,1,0,0,1],[1,1,0,0,0,1]],[[1,0,0,1,0,1],[1,0,0,0,1,1]],[[0,1,1,1,0,0],[0,0,0,1,1,1]],[[0,0,1,1,1,0],[1,1,1,0,0,0]],[[0,1,0,1,1,0],[1,0,1,1,1,1]],[[0,1,1,0,1,0],[1,1,1,1,0,1]]]
S_4 = [[[1,1,1,1,0,0],[1,0,0,1,0,1]],[[0,0,1,1,1,1],[1,0,1,0,0,1]],[[0,1,1,1,1,0],[1,0,1,1,0,1]],[[1,1,1,0,1,0],[0,1,1,1,1,1]],[[0,1,0,1,1,1],[1,1,1,1,1,0]],[[1,1,1,0,0,1],[1,0,0,1,0,0]],[[1,0,0,1,1,1],[0,0,1,0,0,1]],[[0,1,1,1,0,1],[0,1,0,1,1,0]],[[1,0,1,1,1,0],[0,1,1,0,1,0]],[[1,1,0,1,1,0],[0,0,1,1,0,1]],[[0,1,1,0,1,1],[1,0,1,1,0,0]],[[1,1,0,0,1,1],[0,0,1,1,0,0]],[[1,0,1,1,0,1],[1,0,0,0,0,1]],[[1,1,0,1,0,1],[1,1,0,1,1,0]],[[1,0,1,0,1,1],[0,1,1,0,1,1]]]
S_5 = [[[1,1,1,1,1,0],[0,0,1,1,1,1]],[[0,1,1,1,1,1],[1,1,1,1,0,0]],[[1,1,1,1,0,1],[1,1,0,1,0,0]],[[1,0,1,1,1,1],[0,0,1,0,1,1]],[[1,1,1,0,1,1],[0,0,1,1,1,0]],[[1,1,0,1,1,1],[0,1,1,1,0,0]]]
S_6 = [[[1,1,1,1,1,1],[0,1,1,1,1,0]]]
#S_i azokat a megoldáspárokat tartalmazza, amiben a felső sorban i db mezőt kell megnyomni

solutions_6 = S_0 + S_1 + S_2 + S_3 + S_4 + S_5 + S_6


def toggleDown(n,solver):
    solver2=[0 for i in range(n**2)]
    for i in range(n-1):
        for j in range(n):
            if solver[i*n+j]==1:
                solver2[(i+1)*n+j]=(solver2[(i+1)*n+j]+1)%2
                #print(solver2)
                changes=[i*n+j, (i+1)*n+j]
                if j%n>0:
                    changes.append((i+1)*n+j-1)
                if j%n<n-1:
                    changes.append((i+1)*n+j+1)
                if i<n-2:
                    changes.append((i+2)*n+j)
                #print(changes)
                for k in changes:
                    solver[k]=(solver[k]+1)%2
                #print(solver)
        ending=""
        for i in range(n):
            ending+=str(solver[n*(n-1)+i])
    return(solver2, ending)
#Ez a függvény 2 adatot ad ki: Az első az, hogy a kapott mátrixban alkalmazva a toggle-down technikát (fentről lefele és soronként balról jobbra haladva
#minden egyes alatt kattintunk, így csak az alsó sorban szerepelnek égő lámpák) pontosan melyik cellákra kattintottunk rá;
#A másik pedig hogy amikor végeztünk mi szerepel az alsó sorban. Ezt technikai okokból stringként írja ki, mert csak dictionary-műveletekre használjuk úgyis


def firstToggle(n, solver):
    solver3=[0 for i in range(n**2)]
    for i in range(n):
        if solver[i]==1:
            changes=[i, n+i]
            if i>0:
                changes.append(i-1)
            if i<n-1:
                    changes.append(i+1)
            for k in changes:
                    solver3[k]=(solver3[k]+1)%2
            #print(solver)
    return(solver3)
#Ez a függvény szolgál arra, hogy ha a legfelső sorban a solver-ben található 1-esek helyét megnyomnánk, akkor lássuk, hogy mi az új mátrix


for i in range(len(solutions_3)):
    string=str(solutions_3[i][1][0])+str(solutions_3[i][1][1])+str(solutions_3[i][1][2])
    q,r=toggleDown(3,firstToggle(3,solutions_3[i][0]))
    for j in range(3):
        q[j]=(q[j]+solutions_3[i][0][j])%2
    dict_3.update({string:q})
dict_3.update({'000':[0 for i in range(9)]})
#Ez eddig az álatlános fv és a 3x3-mas eset


for i in range(len(solutions_5)):
    string=str(solutions_5[i][1][0])+str(solutions_5[i][1][1])+str(solutions_5[i][1][2])+str(solutions_5[i][1][3])+str(solutions_5[i][1][4])
    q,r=toggleDown(5,firstToggle(5,solutions_5[i][0]))
    for j in range(5):
        q[j]=(q[j]+solutions_5[i][0][j])%2
    dict_5.update({string:q})
dict_5.update({'00000':[0 for i in range(25)]})
#ez az 5x5 esethez tárolja minden alsó sorhoz azt a gombkombinációt ami azt megoldja


for i in range(len(solutions_6)):
    string=str(solutions_6[i][1][0])+str(solutions_6[i][1][1])+str(solutions_6[i][1][2])+str(solutions_6[i][1][3])+str(solutions_6[i][1][4])+str(solutions_6[i][1][5])
    q,r=toggleDown(6,firstToggle(6,solutions_6[i][0]))
    for j in range(6):
        q[j]=(q[j]+solutions_6[i][0][j])%2
    dict_6.update({string:q})
dict_6.update({'000000':[0 for i in range(36)]})
#ez a 6x6 esethez tárolja minden alsó sorhorhoz azt a gombkombinációt ami azt megoldja

smallfont = pygame.font.SysFont('Arial',22) 
#betűtípus és méret

#kezdetben csak megnyitunk egy fekete képernyőt 360x360-as méretben, és a main_screen képernyővel kezdünk
screen = pygame.display.set_mode((360,360)) 
screen.fill(color_black)
main_screen.makeCurrentScreen()
#a következő 2 bool változót a megoldó módban használjuk
#az elsőt csak az 5x5 esetben mert nem minden eset megoldható és külön kell kezelnünk az ilyen eseteket
#a másodikat pedig arra használjuk hogy megjelenjen a 'clear' gomb amivel új inputot tudunk megadni
solvable=True
empty=True

run=True
while run==True:
    #ezzel követjük a kurzor mozgását
    mouse = pygame.mouse.get_pos() 
    
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            pygame.quit()
            break
        if ev.type==pygame.MOUSEBUTTONDOWN:
            if 220 <= mouse[0] <= 320 and 240 <= mouse[1] <= 280: 
                pygame.quit()
                break
                #Ez a kilépés gomb működését intézi, képernyőfüggetlen az egyszerűség kedvéért
            if main_screen.CurrentState==True:
                #ezen a képernyőn navigáló gombok vannak, ezzel választjuk ki melyik méretet szeretnénk nézni
                #és a választással egyben inicializáljuk a matrix_3-5-6 és a solver3 listákat, amikhez a kijelzőn gombok megjelenése is van rendelve
                #ezért fontos hogy rögtön megfelelő méretben és csupa 0-kal szerepeljenek
                if 40 <= mouse[0] <= 120 and 80 <= mouse[1] <= 160: 
                    main_screen.endCurrentScreen()
                    game_screen_3.makeCurrentScreen()
                    matrix_3=[0 for i in range(9)]
                    solver3=[0 for i in range(9)]
                if 140 <= mouse[0] <= 220 and 80 <= mouse[1] <= 160: 
                    main_screen.endCurrentScreen()
                    game_screen_5.makeCurrentScreen()
                    matrix_5=[0 for i in range(25)]
                    solver3=[0 for i in range(25)]
                if 240 <= mouse[0] <= 320 and 80 <= mouse[1] <= 160: 
                    main_screen.endCurrentScreen()
                    game_screen_6.makeCurrentScreen()
                    matrix_6=[0 for i in range(36)]
                    solver3=[0 for i in range(36)]
            if game_screen_3.CurrentState==True:
                #gombok működése manuális input esetben a megfelelő képernyőn
                ButtonState(matrix_3, pos_3, 50)
                #Vissza gomb működése
                if 40 <= mouse[0] <= 180 and 300 <= mouse[1] <= 340: 
                    game_screen_3.endCurrentScreen()
                    main_screen.makeCurrentScreen()
                #Solve gomb működése: lemásolja azt a mátrixot (igazából lista), ami a képernyőn világító gombokat tárolja,
                #alkalazza rá a toggleDown függvényt, ebből megnézi hogy miket nyomott meg eddig, mi szerepel az alsó sorban,
                #és az alsó sor alapján kinézi a dict-ből hogy miket kell még megnyomni
                #majd ennek a kettő 'karakterisztikus vektornak' veszi az összegét mod 2, és tárolja a solver3 listában
                if 40<= mouse[0] <= 140 and 240<= mouse[1]<=280:
                    empty=False
                    current=[]
                    for i in range(9):
                        current.append(matrix_3[i])
                    solver1, ending= toggleDown(3, current)
                    solver2=dict_3.get(ending)
                    for i in range(9):
                        solver3[i]=(solver1[i]+solver2[i])%2
                #a következő gomb csak akkor jelenik meg, ha a képernyőn egy feladvány megoldását látjuk, és kattintásra 'tisztítja' a képernyőt
                #hogy visszalépés nélkül tudjunk új inputot megadni
                if empty==False:
                    if 220<= mouse[0] <=320 and 300<= mouse[1] <= 340:
                        empty=True
                        matrix_3=[0 for i in range(9)]
                        solver3=[0 for i in range(9)]

            #A másik két méretben ugyanezek történnek annyi különbséggel, hogy az 5x5-ös esetben nem minden megoldható, és ekkor a helyes
            #működésnek azt állítottuk be, hogy ezt vegye észre, és a képernyő közepére írja ki hogy 'Not Solvable'
            if game_screen_5.CurrentState==True:
                solvable=True
                ButtonState(matrix_5, pos_5, 30)
                if 40 <= mouse[0] <= 180 and 300 <= mouse[1] <= 340: 
                    game_screen_5.endCurrentScreen()
                    main_screen.makeCurrentScreen()
                if 40<= mouse[0] <= 140 and 240<= mouse[1]<=280:
                    empty=False
                    current=[]
                    for i in range(25):
                        current.append(matrix_5[i])
                    solver1, ending= toggleDown(5, current)
                    solver2=dict_5.get(ending)
                    if solver2==None:
                        #Ezzel veszi észer hogy nem megoldható, a kiiratás lentebb történik
                        solvable=False
                    else:
                        for i in range(25):
                            solver3[i]=(solver1[i]+solver2[i])%2
                if empty==False:
                    if 220<= mouse[0] <=320 and 300<= mouse[1] <= 340:
                        empty=True
                        matrix_5=[0 for i in range(25)]
                        solver3=[0 for i in range(25)]
                        
            if game_screen_6.CurrentState==True:
                ButtonState(matrix_6, pos_6, 25)
                if 40 <= mouse[0] <= 180 and 300 <= mouse[1] <= 340: 
                    game_screen_6.endCurrentScreen()
                    main_screen.makeCurrentScreen()
                if 40<= mouse[0] <= 140 and 240<= mouse[1]<=280:
                    empty=False
                    current=[]
                    for i in range(36):
                        current.append(matrix_6[i])
                    solver1, ending= toggleDown(6, current)
                    solver2=dict_6.get(ending)
                    for i in range(36):
                        solver3[i]=(solver1[i]+solver2[i])%2
                if empty==False:
                    if 220<= mouse[0] <=320 and 300<= mouse[1] <= 340:
                        empty=True
                        screen.fill(color_black)
                        matrix_6=[0 for i in range(36)]
                        solver3=[0 for i in range(36)]
            
                    

    if main_screen.CurrentState==True:
        #Ez teszi oda a Quit gombot vizuálisan
        ButtonVisuals(color_white, color_black, color_dark,220,240,100,40,"Quit",250,247,color_white)
        
        #Ez teszi oda a 3x3 gombot vizuálisan
        ButtonVisuals(color_white, color_black, color_dark, 40, 80, 80, 80, "3x3", 63, 108, color_white)
        
    
        #Ez teszi ada a 5x5 "gombot" vizuálisan
        ButtonVisuals(color_white,color_black, color_dark, 140, 80, 80, 80, "5x5", 163, 108, color_white)
        
    
        #Ez teszi ada a 6x6 "gombot" vizuálisan
        ButtonVisuals(color_white, color_black, color_dark, 240, 80, 80, 80, "6x6", 263, 108, color_white)
        

    if game_screen_3.CurrentState==True:

        #a lámpák gombjainak megjelenése a matrix_3 lista elemeihez van kötve
        #helyes működés: kezdetben a lista csak 0 elemeket tárol, ezért minden lámpa lekapcsolva szerepel, de kattintásra változnak a listaelemek,
        #és ennek megfelelően a gombok színei is
        
        #A gombok körvonalai pedig a solver3 lista elemeihez vannak kötve
        #helyes működés: kezdetben (amíg nem hívjuk meg a megoldó programot) a solver3 lista csak 0 elemeket tárol
        #amikor meghívjuk, az kiszámolja hogy miket kell megnyomni ahhoz hogy megoldódjon, és ott 1-esek szerepelnek
        #Amiket meg kell nyomni ott a körvonal vastag piros, ahol nem, ott vékony fehér
        #a Clear gomb megnyomásával (csak akkor jelenik meg ha a solver3 nem csupa 0), a matrix_3 és solver3 listák tartalma is visszaáll a kezdeti állapotba
        #ezzel a képernyő is, és lehet megadni új inputot
        for i in range(9):
            if solver3[i]==1:
                pygame.draw.rect(screen,color_red,[pos_3[i][0]-1,pos_3[i][1]-1,50+2,50+2])
                if matrix_3[i]==0:
                    ButtonVisuals(color_red, color_black,color_black, pos_3[i][0]+3, pos_3[i][1]+3, 44, 44, "", 0,0,color_white)
                else:
                    ButtonVisuals(color_red, color_yellow,color_yellow, pos_3[i][0]+3, pos_3[i][1]+3, 44, 44, "", 0,0,color_white)
            else:
                if matrix_3[i]==0:
                    ButtonVisuals(color_white, color_black,color_black, pos_3[i][0], pos_3[i][1], 50, 50, "", 0,0,color_white)
                else:
                    ButtonVisuals(color_yellow, color_yellow,color_yellow, pos_3[i][0], pos_3[i][1], 50, 50, "", 0,0,color_white)

        
        ButtonVisuals(color_white,color_black, color_dark,220,240,100,40,"Quit",250,247,color_white)
        ButtonVisuals(color_white,color_black, color_dark,40,300,140,40,"Back to Main",45,307,color_white)
        ButtonVisuals(color_white,color_black, color_dark,40,240,100,40,"Solve",60,247,color_white)
        if empty==False:
            ButtonVisuals(color_white,color_black, color_dark,220,300,100,40,"Clear",250,307,color_white)
            
    if game_screen_5.CurrentState==True:
        screen.fill(color_black)
        #Ez benne van alapból a MakeCurrentScreen függvényben, de mivel itt van olyan eset hogy azt íratjuk ki középre hogy nem megoldható
        #ide inkább visszaraktam, mert utána ha újat szeretnék indítani anélkül hogy ki- meg belépünk a képernyőbe nem eltűnik a felirat, hanem csak háttérbe kerül

            
        #gombok megjelenése és működése ugyanaz mint 3x3-mas esetben
        for i in range(25):
            if solver3[i]==1:
                pygame.draw.rect(screen,color_red,[pos_5[i][0]-1,pos_5[i][1]-1,30+2,30+2])
                if matrix_5[i]==0:
                    ButtonVisuals(color_red, color_black,color_black, pos_5[i][0]+3, pos_5[i][1]+3, 24, 24, "", 0,0,color_white)
                else:
                    ButtonVisuals(color_red, color_yellow,color_yellow, pos_5[i][0]+3, pos_5[i][1]+3, 24, 24, "", 0,0,color_white)
            else:
                if matrix_5[i]==0:
                    ButtonVisuals(color_white,color_black,color_black, pos_5[i][0], pos_5[i][1], 30, 30, "", 0,0,color_white)
                else:
                    ButtonVisuals(color_yellow,color_yellow,color_yellow, pos_5[i][0], pos_5[i][1], 30, 30, "", 0,0,color_white)

        #ez az egy eltérés van: a megoldó program felismeri ha nem megoldható egy feladvány, és ennek megfelelően azt közli is a felhasználóval
        if solvable==False and empty==False:
            ButtonVisuals(color_red,color_red,color_red,105, 110,150,40,'Not Solvable',115,120,color_white)

        ButtonVisuals(color_white,color_black, color_dark,220,240,100,40,"Quit",250,247,color_white)
        ButtonVisuals(color_white,color_black, color_dark,40,300,140,40,"Back to Main",45,307,color_white)
        ButtonVisuals(color_white,color_black, color_dark,40,240,100,40,"Solve",60,247,color_white)
        
        #Ez a gomb csak akkor jelenjen meg ha a képernyőn egy feladvány megoldása szerepel
        if empty==False:
            ButtonVisuals(color_white,color_black, color_dark,220,300,100,40,"Clear",250,307,color_white)
            
    if game_screen_6.CurrentState==True:

        for i in range(36):
            if solver3[i]==1:
                pygame.draw.rect(screen,color_red,[pos_6[i][0]-1,pos_6[i][1]-1,25+2,25+2])
                if matrix_6[i]==0:
                    ButtonVisuals(color_red, color_black,color_black, pos_6[i][0]+3, pos_6[i][1]+3, 19, 19, "", 0,0,color_white)
                else:
                    ButtonVisuals(color_red, color_yellow,color_yellow, pos_6[i][0]+3, pos_6[i][1]+3, 19, 19, "", 0,0,color_white)
            else:
                if matrix_6[i]==0:
                    ButtonVisuals(color_white,color_black,color_black, pos_6[i][0], pos_6[i][1], 25, 25, "", 0,0,color_white)
                else:
                    ButtonVisuals(color_yellow,color_yellow,color_yellow, pos_6[i][0], pos_6[i][1], 25, 25, "", 0,0,color_white)

        ButtonVisuals(color_white,color_black, color_dark,220,240,100,40,"Quit",250,247,color_white)
        ButtonVisuals(color_white,color_black, color_dark,40,300,140,40,"Back to Main",45,307,color_white)
        ButtonVisuals(color_white,color_black, color_dark,40,240,100,40,"Solve",60,247,color_white)
        if empty==False:
            ButtonVisuals(color_white,color_black, color_dark,220,300,100,40,"Clear",250,307,color_white)

    
    

    

    pygame.display.update()