'''
Jogo Hienas Sapecas, criado exclusivamente por Gabriel Garib Gomes

'''

#imports
import turtle as t
from math import cos, sin, radians,atan2,degrees,sqrt
import random as r
import time 

#tela de inicioo e configuracoes inciais
t.title("Hienas sapecas 2D") #nome da aba
t.setup(1160, 940)          #define o tamanho da tela
t.bgpic('./Tela-de-inicio-hiena-gif.gif')     #adicionar uma tela de comeco
t.hideturtle()

#adiciona os sprites
tela=t.Screen()
tela.addshape('./hienaa.gif')
tela.addshape('./inimigo-gif.gif')
tela.addshape('./ecobier-gif.gif')
tela.addshape('./latinhaa.gif')
tela.addshape('./coisa.gif')
tela.addshape('./intencion.gif')

#cria turtle do tiro
tiro = t.Turtle()
tiro.hideturtle()
tiro.shape("./latinhaa.gif")
tiro.penup()
tiro.speed(0)

#cria turtle do personagem
hiena=t.Turtle()         
hiena.hideturtle()
hiena.penup()

#cria turtle do chefao
coisa=t.Turtle()
coisa.hideturtle()
coisa.penup()
coisa.speed(0)

#variável que armazena informação do começo do jogo
começou=False

# limites da tela
margem_de_erro=50
limites=[[],[]]
superior = tela.window_height() // 2 - margem_de_erro  
inferior = -tela.window_height() // 2 + margem_de_erro
esquerda = -tela.window_width() // 2 + margem_de_erro
direita = tela.window_width() // 2 - margem_de_erro

#dados do protagonista
dict_hiena={
            'x':esquerda,
            'y':0,
            'vidas':3,
            'passo':30
            }

#dados do tiro
dict_tiro={
            'x':None,
            'y':None,
            'flag':True,
            'passo':20
           }

#variável que armazena o número da fase
fase=1

#desenha o personagem 
def deshiena():
    hiena.shape('./hienaa.gif')
    hiena.speed(0)
    hiena.penup()
    hiena.setx(esquerda)
    hiena.showturtle()

#cria arena e inicia o jogo 
def startgame():   
    global começou            
    t.bgpic('./logo-container-bar_gif.gif')
    dicinimigos(3)
    deshiena()
    desvidas()
    desini()
    animaini()
    
    começou=True



  
       
#fecha o jogo (ao pressionar 'q')
def fechajogo():
    t.bye()

#animacoes personagem (se a posicao for superior ao limite + margem de erro a funcao nao é chamada quando se aperta a tecla)

def andacima():
    global dict_hiena       #permite atualizar o dicionário globalmente
    nova_posicao_y = dict_hiena['y'] + dict_hiena['passo']
    if dict_hiena['y']<superior and colisaoelp(dict_hiena['x'],nova_posicao_y,formato):
        hiena.sety(nova_posicao_y)
        dict_hiena['y']=hiena.ycor()        #atualiza a posição y do personagem no dicionário
    

def andabaixo():
    global dict_hiena          #permite atualizar o dicionário globalmente
    nova_posicao_y = dict_hiena['y'] - dict_hiena['passo']
    if dict_hiena['y'] > inferior and colisaoelp(dict_hiena['x'],nova_posicao_y,formato):
        hiena.sety(nova_posicao_y)
        dict_hiena['y']=hiena.ycor()        #atualiza a posição y do personagem no dicionário

def andaesquerda():
    global dict_hiena       #permite atualizar o dicionário globalmente
    nova_posicao_x = dict_hiena['x'] - dict_hiena['passo']
    
    if dict_hiena['x']> esquerda and colisaoelp(nova_posicao_x,dict_hiena['y'],formato):
        hiena.setx(nova_posicao_x)
        dict_hiena['x']=hiena.xcor()        #atualiza a posição x do personagem no dicionário

def andadireita():
    global dict_hiena       #permite atualizar o dicionário globalmente
    nova_posicao_x = dict_hiena['x'] +dict_hiena['passo']
    if dict_hiena['x'] < direita and colisaoelp(nova_posicao_x ,dict_hiena['y'],formato):
            hiena.setx(nova_posicao_x )
            dict_hiena['x']=hiena.xcor()        #atualiza a posição x do personagem no dicionário

        



#funcao que verifica se um ponto esta dentro da elipse (com margem de erro para o sprite=200)
def colisaoelp(posx,posy,forma):
    if len(forma)==4:
        elp=forma               #fase1
        if ((posx - elp[0]) ** 2) / (elp[2] ** 2) + ((posy - elp[1]) ** 2) / (elp[3] ** 2) <= 1 + (200/ elp[2]) ** 2:    #equacao da elipse
            return False
        else:
            return True
    elif len(forma)==3:         #fase2
        circ=forma
        if((posx-circ[0])**2)+((posy-circ[1])**2)<=circ[2]**2 :  
            return False
        else:
            return True

# funcao utilizada para printar coordenadas no canvas
# def marcapos():
#     print(hiena.xcor(),hiena.ycor())
       


#funcao utilizada para medir a elipse central do mapa
# def desenhar_elipse(xc, yc, a, b):
#     elp1=t.Turtle()
#     elp1.penup()
#     elp1.color('blue')
#     elp1.speed(0)
    
#     theta = 0
#     while theta < 360:
#         x = xc + a * cos(radians(theta))
#         y = yc + b * sin(radians(theta))
        
#         elp1.goto(x, y)
#         elp1.pendown()
        
#         theta += 1
        


# desenhar_elipse(0, 20, 345, 225)        #elipse maior exterior

#define o formato da fase como uma elipse
formato=(0,20,345,225)

# Calcula a distância entre dois pontos usando o Teorema de Pitágoras
def calcular_distancia(x1, y1, x2, y2):
    
    distancia =sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distancia

# dados dos inimigos
inimigos1 = []

#dicinimigos com args 2,3 argumento servem para gerar inimigos com posição
def dicinimigos(numini):
    global fase
    for _ in range(numini):
        inimigo = {'x' : r.randint(-500,500),
                'y': r.randint(-400,400),
                'passo': 20,
                }
        inimigos1.append(inimigo)
    if fase==1:
        fase=2 #variavel que libera passar para 2 fase assim que os inimigos forem eliminados

lista_inimigos=[]

#variável que define o sprite da fase 1
sprite='./intencion.gif'

#desenha os inimigos 
#puxa a quantidade de inimigos da lista de inimigos1
def desini():
    global contini     #variavel utilizada para laços de todos os inimigos
    for contini in range(len(inimigos1)):
        ini=t.Turtle()
        ini.speed(0)
        ini.penup()
        ini.shape(sprite)
        lista_inimigos.append(ini)
        ini.goto(inimigos1[contini]['x'],inimigos1[contini]['y'])

#dados do chefao                 
def dicichefao():
    global dict_chefao
    dict_chefao= {'x' : 0,
                  'y': 0,
                  'passo': 5
                }

#desenha o chefão
def deschefao():
    coisa.showturtle()
    coisa.penup()
    coisa.shape('./coisa.gif')
    coisa.goto(dict_chefao['x'],dict_chefao['y'])

#movimentacao dos inimigos
def perseguir():
    global contini          #evita o erro: local variable 'contini' referenced before assignment
    for ini in lista_inimigos:
        ini.setheading(ini.towards(hiena)+r.uniform(-50,50))
        if contini>=len(inimigos1):      #arruma o erro de diminuir o comprimento da lista dentro do laço
            contini-=1
        distancia = calcular_distancia(dict_hiena['x'],dict_hiena['y'],inimigos1[contini]['x'], inimigos1[contini]['y'])
        if distancia > 20:
            ini.forward(inimigos1[contini]['passo'])
            inimigos1[contini]['x']=ini.xcor()  #atualiza a posição x no dicionario
            inimigos1[contini]['y']=ini.ycor()  #atualiza a posição y no dicionario

#configura as vidas do personagem
def perdevida():
    global dict_hiena
    for i in range(len(lista_inimigos)):
        if i>=len(lista_inimigos):      #arruma o erro de diminuir o comprimento da lista dentro do laço
            i-=1
        if lista_inimigos[i].distance(hiena) < margem_de_erro and lista_inimigos[i].isvisible():
            dict_hiena['vidas'] -= 1
            vidas[dict_hiena['vidas']].hideturtle()
            lista_inimigos[i].hideturtle()
            lista_inimigos.remove(lista_inimigos[i])                
        if dict_hiena['vidas']==0:
            dict_hiena['passo']=0
            acabajogo()
            break

#determina o gameover
def acabajogo():
    hiena.hideturtle()
    coisa.hideturtle()
    for ini in lista_inimigos:
        ini.hideturtle()
    for vida in vidas:
        vida.hideturtle()
    tela.bgpic('./gameover-gif.gif')


#anima os inimigos
def animaini():
    perdevida()
    perseguir()
    eliminarini()
    inicia2fase()
    tela.update()
    tela.ontimer(animaini,100)

#desenha as vidas do personagem
def desvidas():
    global vidas
    vidas = []
    for i in range(4):
        coração = t.Turtle()
        coração.hideturtle()
        coração.penup()
        coração.shape('./ecobier-gif.gif')
        coração.speed(0)
        coração.goto(esquerda+ ((i) * 50),superior)
        coração.showturtle()
        vidas.append(coração)
    coração.hideturtle()

#função que determina a morte dos inimigos se atingindos por disparos
def eliminarini():
    global dict_tiro
    for i in range(len(lista_inimigos)):
        if i>=len(lista_inimigos):
            i-=1
        if lista_inimigos[i].distance(tiro)<margem_de_erro and tiro.isvisible():
            lista_inimigos[i].hideturtle()
            lista_inimigos.remove(lista_inimigos[i])
            tiro.hideturtle()
            dict_tiro['flag']=True

            
#funções atribuidas às teclas
def disparocima(): 
    if começou and dict_tiro['flag']:
        tiro.goto(dict_hiena['x'], dict_hiena['y'] + margem_de_erro)  
        movetirocima()
def disparobaixo():
    if começou and dict_tiro['flag']:
        tiro.goto(dict_hiena['x'], dict_hiena['y'] - margem_de_erro) 
    movetirobaixo()
def disparoesquerda():   
    if começou and dict_tiro['flag']:
        tiro.goto(dict_hiena['x']-margem_de_erro, dict_hiena['y'])

    movetiroesquerda()
def disparodireita():
    if começou and dict_tiro['flag']:
        tiro.goto(dict_hiena['x']+margem_de_erro, dict_hiena['y'])

    movetirodireita()

#animacao tiro pra cima
def movetirocima():
    global dict_tiro
    dict_tiro['flag']=False
    tiro.showturtle()
    dict_tiro['x'],dict_tiro['y']=tiro.xcor(),tiro.ycor()
    y = dict_tiro['y'] +dict_tiro['passo']
    tiro.sety(y)
    dict_tiro['y']=tiro.ycor()
    # Verificando colisão com as bordas e obstáculos
    if tiro.ycor() > superior or not colisaoelp(dict_tiro['x'],dict_tiro['y'],formato):
        tiro.hideturtle()
        dict_tiro['flag']=True
        return
    tela.ontimer(movetirocima, 20)

#animacao tiro pra baixo
def movetirobaixo():
    global dict_tiro
    dict_tiro['flag']=False
    tiro.showturtle()
    dict_tiro['x'],dict_tiro['y']=tiro.xcor(),tiro.ycor()
    y = dict_tiro['y'] -dict_tiro['passo']
    tiro.sety(y)
    dict_tiro['y']=tiro.ycor()
    # Verificando colisão com as bordas e obstáculos
    if tiro.ycor() < inferior or not colisaoelp(dict_tiro['x'],dict_tiro['y'],formato):
        tiro.hideturtle()
        dict_tiro['flag']=True  
        return
    tela.ontimer(movetirobaixo, 20)

#animacao tiro pra direita
def movetirodireita():
    global dict_tiro
    dict_tiro['flag']=False
    tiro.showturtle()
    dict_tiro['x'],dict_tiro['y']=tiro.xcor(),tiro.ycor()
    x = dict_tiro['x'] +dict_tiro['passo']
    tiro.setx(x)
    dict_tiro['x']=tiro.xcor()
    # Verificando colisão com as bordas e obstáculos
    if tiro.xcor() > direita or not colisaoelp(dict_tiro['x'],dict_tiro['y'],formato):
        tiro.hideturtle()
        dict_tiro['flag']=True  
        return
    tela.ontimer(movetirodireita, 20)

#animacao tiro pra esquerda         so pode atirar quando terminar o tiro
def movetiroesquerda():
    global dict_tiro
    dict_tiro['flag']=False
    tiro.showturtle()
    dict_tiro['x'],dict_tiro['y']=tiro.xcor(),tiro.ycor()
    x = dict_tiro['x'] -dict_tiro['passo']
    tiro.setx(x)
    dict_tiro['x']=tiro.xcor()
    # Verificando colisão com as bordas e obstáculos
    if tiro.xcor() < esquerda or not colisaoelp(dict_tiro['x'],dict_tiro['y'],formato):
        tiro.hideturtle()
        dict_tiro['flag']=True  
        return
    tela.ontimer(movetiroesquerda, 20)

#inicia segunda fase e acaba o jogo
def inicia2fase():
    global formato,dict_hiena,fase,sprite
    if lista_inimigos==[] and dict_hiena['vidas']!=0 and fase==2:     
        fase=0
        dict_hiena['vidas']=1       #determina o dano dos inimigos da fase 2
        sprite='./inimigo-gif.gif'
        t.bgpic('life.gif')
        formato=(-10,10,280)
        hiena.goto(esquerda,0)
        dict_hiena['x']=hiena.xcor()
        dict_hiena['y']=hiena.ycor()
        inimigos1.clear()
        dicinimigos(6)
        desini()
        dicichefao()
        deschefao()
    if lista_inimigos==[] and fase==0:
        for i in range(200):
            if coisa.distance(hiena)< margem_de_erro*3:     #easter egg morte pelo coisa

                acabajogo()
            coisa.goto(0,i*dict_chefao['passo'])            #coisa saindo da tela
            if coisa.xcor()==0 and coisa.ycor()>700:        #se o coisa sai da tela o jogo acaba
                voceganhou()
                return


    
#função que determina o que acontece caso zere o jogo
def voceganhou():
    if lista_inimigos==[]:
        coisa.hideturtle()
        hiena.hideturtle()
        for vida in vidas:
            vida.hideturtle()
        tiro.hideturtle() 
        tela.bgcolor('black')       
        tela.bgpic('./youwon.gif')
        return
    tela.ontimer(voceganhou,800)

#atualiza rapidamente as animações
# tela.tracer()

# Le as teclas pressionadas no teclado
tela.listen()
tela.onkey(startgame,'p')
tela.onkey(fechajogo, "q")
tela.onkeypress(andacima, "Up")
tela.onkeypress(andabaixo, "Down")
tela.onkeypress(andaesquerda, "Left")
tela.onkeypress(andadireita, "Right")
tela.onkey(disparocima,"w")
tela.onkey(disparobaixo,"s")
tela.onkey(disparodireita,"d")
tela.onkey(disparoesquerda,"a")

#mantem o canvas aberto
t.mainloop()