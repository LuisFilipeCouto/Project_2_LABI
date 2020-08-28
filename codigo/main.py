import cherrypy
import json
import requests
import sqlite3 as sql
import os
from processador import *

class Root(object):

    @cherrypy.expose

    #página inicial

    def index(self):

        cherrypy.response.headers["Content-Type"] = "text/html"

        return open('Interface/index.html', 'r').read()

    @cherrypy.expose

    #lista de objetos já detectados

    def listnames(self):

        db = sql.connect('images.db')#conecta a base de dados

        result = db.execute("SELECT class FROM objetos_detetados")#procura a imagem

        for row in result:#codificar em json

            rew= json.loads(row)

        db.close()

        return json.dumps(rew)

    @cherrypy.expose


    #devolve a class e as imagens cortadas e originais
    def listdetected(self):

        db = sql.connect('images.db')#conecta á base de dados

        result = db.execute("SELECT class, sha_original, sha_objeto, confidence FROM objetos_detetados")#

        raws= result.fetchall()

        for row in raws:#cria string que codifique me json

            data={

            row[0] : [

                {'original': row[1], 'objeto': row[2], 'confidence': row[3]},

                        ]

            }

            jason=json.loads(data)

        db.close()

        cherrypy.response.headers["Content-Type"] = "application/json"

        return json.dumps(jason, indent=2)


    #devolve as imagens cortadas e as imagens originais das imagens com a class pretendida
    @cherrypy.expose

    def listdetectedname(self, name):

        db = sql.connect('images.db')

        result = db.execute("SELECT class, sha_original, sha_objeto, FROM objetos_detetados WHERE class LIKE ?",(name,))

        raws= result.fetchall()

        for row in result:

            data={

            row[0] : [

                {'original': row[1], 'objeto': row[2], 'confidence': row[3]},

                        ]

            }

            jason=json.loads(data)

        db.close()

        cherrypy.response.headers["Content-Type"] = "application/json"

        return json.dumps(jason, indent=2)


        #devolve as imagens cortadas e as imagens originais das imagens com a class e cor pretendida


        #devolve as imagens cortadas e as imagens originais das imagens com a class e cor pretendida

    @cherrypy.expose

    def listdetectednameandcolor(self, name, color):

        db = sql.connect('images.db')

        result = db.execute("SELECT class, sha_original, sha_objeto FROM objetos_detetados WHERE class,color LIKE ??",(name,color))

        raws= result.fetchall()

        for row in result:

            data={

            row[0] + row[1] : [

                {'original': row[2], 'objeto': row[3], 'confidence': row[4]},

                        ]
            }

            jason=json.loads(data)

        db.close()

        cherrypy.response.headers["Content-Type"] = "application/json"

        return json.dumps(jason, indent=2)

    #corre o processador de imagens, que corta obejtos, identifica a cor, a confiança e envia tudo para a base de dados.
    @cherrypy.expose
    def put(self, fname):
       process(fname)

    #corre o processador de imagens, que corta obejtos, identifica a cor, a confiança e envia tudo para a base de dados.

    @cherrypy.expose

    def put(self, fname):

       process(fname)
       

    @cherrypy.expose

    def identifier(self, sintese):#procura a imagem com o identificador que é a sintese da mesma

        db = sql.connect('images.db')

        result = db.execute("SELECT image FROM imagem_upload WHERE sintese LIKE ??",(sintese,))

        raws= result.fetchall()

        return raws


if __name__ == "__main__":

    cherrypy.config.update({'server.socket_port': 10019,})#mudar a porta

    current_dir = os.path.abspath(os.path.dirname(__file__))#caminho para este ficheiro

    conf = {'/': {'tools.staticdir.root': current_dir},

                    '/vendor': {'tools.staticdir.on': True,
                                'tools.staticdir.dir': 'Interface/vendor'},   
                    '/css': {   'tools.staticdir.on': True,
                                'tools.staticdir.dir': 'Interface/css'},
                    '/js': {    'tools.staticdir.on': True,
                                'tools.staticdir.dir': 'Interface/js'},
                    '/font-awesome': {  'tools.staticdir.on': True,
                                'tools.staticdir.dir': 'Interface/vendor/font-awesome'},
                    '/Imagens': {'tools.staticdir.on': True,
                                'tools.staticdir.dir': 'Interface/Imagens'},
                    '/imagens.html':{'tools.staticfile.on': True,
                                'tools.staticfile.filename': current_dir+'/Interface/imagens.html'},
                    '/index.html':{'tools.staticfile.on': True,
                                'tools.staticfile.filename': current_dir+'/Interface/index.html'},
                    '/info.html':{'tools.staticfile.on': True,
                                'tools.staticfile.filename': current_dir+'/Interface/info.html'},
                    '/objetos.html':{'tools.staticfile.on': True,
                                'tools.staticfile.filename': current_dir+'/Interface/objetos.html'},
                    '/pesquisar.html':{'tools.staticfile.on': True,
                                'tools.staticfile.filename': current_dir+'/Interface/pesquisar.html'},
                    '/upload.html':{'tools.staticfile.on': True,
                                'tools.staticfile.filename': current_dir+'/Interface/upload.html'},
                    '/YOLO.mp4':{'tools.staticfile.on': True,
                                'tools.staticfile.filename': current_dir+'/Interface/YOLO.mp4'},           
                    }

    cherrypy.tree.mount(Root(), "/", conf)

    cherrypy.server.start()#inicia o servidor


