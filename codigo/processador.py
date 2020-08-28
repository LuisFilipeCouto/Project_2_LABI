import requests
from PIL import Image
import sys
import sqlite3 as sql
import os

def process(fname):

    session = requests.Session()

    URL = "http://image-dnn-sgh-jpbarraca.ws.atnog.av.it.pt/process"

    image = Image.open(fname)

    with open(fname,"rb") as f:     #codigo dado no guiao

        file = {"img" : f.read()}

        r = session.post(url=URL, files=file, data=dict(thr=0.5))

        if r.status_code == 200:

            data = r.json() #data para iterar sobre

            if(len(data) > 0):

                save_original(image,fname)

                #to_database_original()

                for i in range(0,len(data)):

                    t = creatbox(data,i)

                    box = t[0]

                    x  = box[0]

                    y  = box[1]

                    x1 = box[2]

                    y1 = box[3]

                    print("x: " + str(x))
                    print("y: " + str(y))
                    print("x1: " + str(x1))
                    print("y1:" + str(y1))
                    box_width  = x1-x

                    box_height = y1-y

                    classe = t[1]

                    confidence = t[2]

                    new_image = crop(box,image)

                    save_cut(new_image,i,classe)

                    color = findcolor(new_image,box_width,box_height)

                    print("Cor dominante: " + color + '\n' )


def crop(box,image): #como argumento um tuple com as coordenadas e o nome da imagem original

    new_image = image.crop(box)

    return new_image


def findcolor (image,width,height): # Função 1 para encontrar a cor, é mais especifica

    #Cores a considerar

    dic = {"vermelho" : 0, "laranja" : 0, "amarelo" : 0, "verde" : 0,"azul" : 0, "violeta" : 0, "preto" : 0, "branco" :0, "cinzento" :0, "castanho" : 0}

    for x in range(width):

        for y in range(height):

            p = image.getpixel((x,y))

            red = p[0]

            green = p[1]

            blue = p[2]

            if (red <= 40 and green <=40 and blue <=40) :

                trueblack = True

            else:

                trueblack = False

            if red <= 85:

                red_v = "baixo"

            elif red >= 170:

                red_v = "alto"

            else:

                red_v = "medio"

            #-------------------------------

            if green <= 85:

                green_v = "baixo"

            elif green >= 170:

                green_v = "alto"

            else:

                green_v = "medio"

            #-------------------------------

            if blue <= 85:

                blue_v = "baixo"

            elif blue >= 170:

                blue_v = "alto"

            else:

                blue_v = "medio"

            #-------------------------------

            if(red_v == "baixo" and green_v == "baixo" and blue_v == "baixo" and trueblack == True): #combinação (---) 1

                dic["preto"] = dic["preto"] + 1

            if(red_v == "baixo" and green_v == "baixo" and blue_v == "medio"): #combinação (--0) 2

                dic["azul"] = dic["azul"] + 1

            if(red_v == "baixo" and green_v == "baixo" and blue_v == "alto"): #combinação (--+) 3

                dic["azul"] = dic["azul"] + 1

            if(red_v == "baixo" and green_v == "alto" and blue_v == "baixo"): #combinação (-+-) 4

                dic["verde"] = dic["verde"] + 1

            if(red_v == "baixo" and green_v == "alto" and blue_v == "medio"): #combinação (-+0) 5

                dic["verde"] = dic["verde"] + 1

            if(red_v == "baixo" and green_v == "alto" and blue_v == "alto"): #combinação (-++) 6

                dic["azul"] = dic["azul"] + 1

            if(red_v == "baixo" and green_v == "medio" and blue_v == "baixo"): #combinação (-0-) 7

                dic["verde"] = dic["verde"] + 1

            if(red_v == "baixo" and green_v == "medio" and blue_v == "alto"): #combinação (-0+) 8

                dic["azul"] = dic["azul"] + 1

            if(red_v == "baixo" and green_v == "medio" and blue_v == "medio"): #combinação (-00) 9

                dic["azul"] = dic["azul"] + 1

            if(red_v == "alto" and green_v == "alto" and blue_v == "alto"): #combinação (+++) 10

                dic["branco"] = dic["branco"] + 1

            if(red_v == "alto" and green_v == "alto" and blue_v == "baixo"): #combinação (++-) 11

                dic["amarelo"] = dic["amarelo"] + 1

            if(red_v == "alto" and green_v == "alto" and blue_v == "medio"): #combinação (++0) 12

                dic["amarelo"] = dic["amarelo"] + 1

            if(red_v == "alto" and green_v == "medio" and blue_v == "baixo"): #combinação (+0-) 13

                dic["laranja"] = dic["laranja"] + 1

            if(red_v == "alto" and green_v == "medio" and blue_v == "medio"): #combinação (+00) 14

                dic["vermelho"] = dic["vermelho"] + 1

            if(red_v == "alto" and green_v == "medio" and blue_v == "alto"): #combinação (+0+) 15

                dic["violeta"] = dic["violeta"] + 1

            if(red_v == "alto" and green_v == "baixo" and blue_v == "baixo"): #combinação (+--) 16

                dic["vermelho"] = dic["vermelho"] + 1

            if(red_v == "alto" and green_v == "baixo" and blue_v == "medio"): #combinação (+-0) 17

                dic["violeta"] = dic["violeta"] + 1

            if(red_v == "alto" and green_v == "baixo" and blue_v == "alto"): #combinação (+-+ 18

                dic["violeta"] = dic["violeta"] + 1

            if(red_v == "medio" and green_v == "medio" and blue_v == "medio"): #combinação (000) 19

                dic["cinzento"] = dic["cinzento"] + 1

            if(red_v == "medio" and green_v == "medio" and blue_v == "baixo"): #combinação (00-) 20

                dic["amarelo"] = dic["amarelo"] + 1

            if(red_v == "medio" and green_v == "medio" and blue_v == "alto"): #combinação (00+) 21

                dic["azul"] = dic["azul"] + 1

            if(red_v == "medio" and green_v == "baixo" and blue_v == "baixo"): #combinação (0--) 22

                dic["vermelho"] = dic["vermelho"] + 1

            if(red_v == "medio" and green_v == "baixo" and blue_v == "alto"): #combinação (0-+) 23

                dic["violeta"] = dic["violeta"] + 1

            if(red_v == "medio" and green_v == "baixo" and blue_v == "medio"): #combinação (0-0) 24

                dic["violeta"] = dic["violeta"] + 1

            if(red_v == "medio" and green_v == "alto" and blue_v == "baixo"): #combinação (0+-) 25

                dic["verde"] = dic["verde"] + 1

            if(red_v == "medio" and green_v == "alto" and blue_v == "medio"): #combinação (0+0) 26

                dic["verde"] = dic["verde"] + 1

            if(red_v == "medio" and green_v == "alto" and blue_v == "alto"): #combinação (0++) 27

                dic["azul"] = dic["azul"] + 1

    #print(dic)

    return max(dic,key=lambda key:dic[key])


def creatbox(data,index):

    classe = data[index]["class"] #classe/tipo do objeto detetado

    confidence = data[index]["confidence"] # valor da confiança

    x  = int(data[index]["box"]["x"])    # coordenada "x" do canto superior esquerdo da imagem

    y  = int(data[index]["box"]["y"])    # coordenada "y" do canto superior esquerdo da imagem

    x1 = int(data[index]["box"]["x1"])   # coordenada "x" do canto inferior direito da imagem

    y1 = int(data[index]["box"]["y1"])   # coordenada "y" do canto inferior direito da imagem

    box = (x,y,x1,y1) #tuple para guardar coordenadas que definem a caixa

    print("Class: " + classe)

    print("Confianca: " + str(confidence))

    tuple = (box,classe,confidence)

    return tuple;

def save_cut(image,index,classe):

    image.save("Objects/" + classe + "-cut-number-" + str(index+1) + ".jpg")


def save_original(image,name):

    image.save("Original/"+name)


def to_database_original(nome,sintese,path):

     db = sql.connect(images.db)

     db.execute("INSERT INTO imagem_upload(nome,sintese) VALUES (?,?,?);",(nome,sintese,path))


#process(sys.argv[1]) #Descomentar linha se quiser correr este programa no terminal