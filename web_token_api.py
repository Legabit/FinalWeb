import endpoints
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from protorpc import remote

import jwt
import time

from CustomExceptions import NotFoundException

from messages import EmailPasswordMessage, TokenMessage, CodeMessage, Token, TokenKey, MessageNone
from messages import EmpresaInput, EmpresaUpdate, EmpresaList
from messages import TweetInput, TweetUpdate, TweetList
from messages import UserInput, UserUpdate, UserList
from messages import ProductInput, ProductUpdate, ProductList
from messages import LaboratorioInput, LaboratorioUpdate, LaboratorioList
from messages import ComentarioInput, ComentarioUpdate, ComentarioList
from messages import FarmaciaInput, FarmaciaUpdate, FarmaciaList

from endpoints_proto_datastore.ndb import EndpointsModel

import models
from models import validarEmail
from models import Empresa, Usuarios, Tweet, Product,Comentario,Laboratorio,Farmacia

###############
# Products
###############
@endpoints.api(name='products_api', version='v1', description='products endpoints')
class ProductsApi(remote.Service):

  ######## Add products ##########
  @endpoints.method(ProductInput, CodeMessage, path='products/insert', http_method='POST', name='products.insert')
  def product_add(cls, request):
    try:
      token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
      user = Usuarios.get_by_id(token['user_id'])
      
      myProduct = Product()

      if myProduct.product_m(request, user.key) == 0:
        codigo = 1
      else:
        codigo = -3

      message = CodeMessage(code=codigo, message='Product added')
   
    except jwt.DecodeError:
      message = CodeMessage(code=-2, message='Invalid token')
    except jwt.ExpiredSignatureError:
      message = CodeMessage(code=-1, message='Token expired')
    
    return message

  @endpoints.method(TokenKey, ProductList, path='products/get', http_method='POST', name='products.get')
  def product_get(cls, request):
    try:                 
      
      token = jwt.decode(request.tokenint, 'secret')  #checa token
      productentity = ndb.Key(urlsafe = request.entityKey)
      product = Product.get_by_id(productentity.id()) #obtiene usuario
      
      lista = []  #crea lista
      lstMessage = ProductList(code=1) # crea objeto mensaje
      lista.append(ProductUpdate(token='', 
                                 entityKey= product.entityKey,
                                 #empresa_key = user.empresa_key.urlsafe(),
                                 code = product.code,
                                 description = product.description,
                                 urlImage = product.urlImage)) # agrega a la lista

      lstMessage.data = lista #ASIGNA a la salida la lista
      message = lstMessage
    
    except jwt.DecodeError:
      message = UserList(code=-1, data=[]) #token invalido
    
    except jwt.ExpiredSignatureError:
      message = UserList(code=-2, data=[]) #token expiro
    
    return message


######## list products ##########

  @endpoints.method(Token, ProductList, path='products/list', http_method='POST', name='products.list')
  def product_list(cls, request):
    try:
      
      token = jwt.decode(request.tokenint, 'secret')  #checa token
      user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
      lista = []  #crea lista
      lstMessage = ProductList(code=1) # crea objeto mensaje
      lstBd = Product.query().fetch() # recupera de base de datos
      
      for i in lstBd: # recorre
        lista.append(ProductUpdate(token='', entityKey = i.entityKey,
                                #empresa_key=user.empresa_key.urlsafe(),
                                code = i.code,
                                description = i.description,
                                urlImage = i.urlImage)) # agrega a la lista
      
      lstMessage.data = lista # la manda al messa
      message = lstMessage #regresa
      
    except jwt.DecodeError:
      message = ProductList(code=-1, data=[]) #token invalido
    except jwt.ExpiredSignatureError:
      message = ProductList(code=-2, data=[]) #token expiro
    return message

  @endpoints.method(ProductUpdate, CodeMessage, path='products/update', http_method='POST', name='products.update')
  #siempre lleva cls y request
  def product_update(cls, request):
    try:
      token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
      user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
      product = Product()

      # empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
      if product.product_m(request, user.key) == 0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
        codigo = 1
      
      else:
        codigo = -3
        #la funcion josue_m puede actualizar e insertar
        #depende de la ENTRADA de este endpoint method
      
      message = CodeMessage(code = 1, message='Sus cambios han sido guardados exitosamente')
    except jwt.DecodeError:
      message = CodeMessage(code = -2, message='Invalid token')
    except jwt.ExpiredSignatureError:
      message = CodeMessage(code = -1, message='Token expired')
    return message

  @endpoints.method(TokenKey, CodeMessage, path='products/delete', http_method='POST', name='products.delete')
  #siempre lleva cls y request
  def product_remove(cls, request):
    
    try:

      token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      productEntity = ndb.Key(urlsafe = request.entityKey)#Obtiene el elemento dado el EntitKey
      productEntity.delete()#BORRA
      message = CodeMessage(code = 1, message = 'Succesfully deleted')
    
    except jwt.DecodeError:
      message = CodeMessage(code = -2, message = 'Invalid token')

    except jwt.ExpiredSignatureError:
      message = CodeMessage(code = -1, message = 'Token expired')
    
    return message

###############
# Usuarios
###############
@endpoints.api(name='usuarios_api', version='v1', description='usuarios endpoints')
class UsuariosApi(remote.Service):
###############get the info of one########
 @endpoints.method(TokenKey, UserList, path='users/get', http_method='POST', name='users.get')
 def users_get(cls, request):
  try:                 
   token = jwt.decode(request.tokenint, 'secret')  #checa token
   userentity = ndb.Key(urlsafe=request.entityKey)
   user = Usuarios.get_by_id(userentity.id()) #obtiene usuario
            #user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = []  #crea lista
   lstMessage = UserList(code=1) # crea objeto mensaje
   lista.append(UserUpdate(token='', 
    entityKey= user.entityKey,
    #empresa_key = user.empresa_key.urlsafe(),
    email = user.email))
   lstMessage.data = lista#ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = UserList(code=-1, data=[]) #token invalido
  except jwt.ExpiredSignatureError:
   message = UserList(code=-2, data=[]) #token expiro
  return message


########################## list###################
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
  @endpoints.method(Token, UserList, path='users/list', http_method='POST', name='users.list')
  def lista_usuarios(cls, request):
    try:
      token = jwt.decode(request.tokenint, 'secret')  #checa token
      user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
      lista = []  #crea lista
      lstMessage = UserList(code=1) # crea objeto mensaje
      lstBd = Usuarios.query().fetch() # recupera de base de datos
      
      for i in lstBd: # recorre
        lista.append(UserUpdate(token='',
        entityKey=i.entityKey,
        #empresa_key=user.empresa_key.urlsafe(),
        email=i.email)) # agrega a la lista
      
      lstMessage.data = lista # la manda al messa
      message = lstMessage #regresa
      
    except jwt.DecodeError:
      message = UserList(code=-1, data=[]) #token invalido
    except jwt.ExpiredSignatureError:
      message = UserList(code=-2, data=[]) #token expiro
    
    return message

  @endpoints.method(TokenKey, CodeMessage, path='users/delete', http_method='POST', name='users.delete')
  #siempre lleva cls y request
  def user_remove(cls, request):
    try:
      
      token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      usersentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
      usersentity.delete()#BORRA
      message = CodeMessage(code=1, message='Succesfully deleted')
    
    except jwt.DecodeError:
      message = CodeMessage(code=-2, message='Invalid token')
    
    except jwt.ExpiredSignatureError:
      message = CodeMessage(code=-1, message='Token expired')
    
    return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
  @endpoints.method(UserInput, CodeMessage, path='users/insert', http_method='POST', name='users.insert')
  def user_add(cls, request):
    try:
      token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
      user = Usuarios.get_by_id(token['user_id'])
    
      if validarEmail(request.email) == False: #checa si el email esta registrado
                       #empresakey = ndb.Key(urlsafe=request.empresa_key) #convierte el string dado a entityKey
        if user.usuario_m(request, user.empresa_key) == 0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
          codigo = 1
        
        else:
          codigo = -3
                         #la funcion josue_m puede actualizar e insertar
                         #depende de la ENTRADA de este endpoint method
        message = CodeMessage(code = codigo, message = 'Succesfully added')
    
      else:
        message = CodeMessage(code = -4, message = 'El email ya ha sido registrado')
    
    except jwt.DecodeError:
      message = CodeMessage(code = -2, message = 'Invalid token')
    
    except jwt.ExpiredSignatureError:
      message = CodeMessage(code = -1, message = 'Token expired')
    
    return message


##login##

 @endpoints.method(EmailPasswordMessage, TokenMessage, path='users/login', http_method='POST', name='users.login')
 def users_login(cls, request):
  try:
   user = Usuarios.query(Usuarios.email == request.email).fetch() #obtiene el usuario dado el email
   if not user or len(user) == 0: #si no encuentra user saca
    raise NotFoundException()
   user = user[0] 
   keye = user.empresa_key.urlsafe() # regresa como mensaje el empresa key
   if not user.verify_password(request.password): # checa la contrasena
    raise NotFoundException()

   token = jwt.encode({'user_id': user.key.id(), 'exp': time.time() + 43200}, 'secret') #crea el token
   message = TokenMessage(token=token, message=keye, code=1) # regresa token
  except NotFoundException:
   message = TokenMessage(token=None, message='Wrong username or password', code=-1)
  return message

##update##
# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(UserUpdate, CodeMessage, path='user/update', http_method='POST', name='user.update')
#siempre lleva cls y request
 def user_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   if user.usuario_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

###########################
#### Empresa
###########################

## Google Cloud Endpoint
@endpoints.api(name='empresas_api', version='v1', description='empresas REST API')
class EmpresasApi(remote.Service):


# get one

 @endpoints.method(TokenKey, EmpresaList, path='empresa/get', http_method='POST', name='empresa.get')
#siempre lleva cls y request
 def empresa_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   empresaentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #empresaentity.get().empresa_key.urlsafe() para poder optener el EntityKey
     ##### ejemplo real
    ####### message = EmpresaList(code=1, data=[EmpresaUpdate(token='Succesfully get', nombre_empresa=empresaentity.get().nombre_empresa, empresa_key=empresaentity.get().empresa_key.urlsafe(), entityKey=empresaentity.get().entityKey)])
   message = EmpresaList(code=1, data = [EmpresaUpdate(token='Succesfully get',
    entityKey = empresaentity.get().entityKey,
    codigo_empresa=empresaentity.get().codigo_empresa, 
    nombre_empresa = empresaentity.get().nombre_empresa)])

  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message




 @endpoints.method(TokenKey, CodeMessage, path='empresa/delete', http_method='POST', name='empresa.delete')
#siempre lleva cls y request
 def empresa_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   empresaentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   empresaentity.delete()#BORRA
   message = CodeMessage(code=1, message='Succesfully deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


# insert
 @endpoints.method(EmpresaInput, CodeMessage, path='empresa/insert', http_method='POST', name='empresa.insert')
#siempre lleva cls y request
 def empresa_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario models.py 
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0: 
    codigo=1
   else:
    codigo=-3
              #la funcion josue_m puede actualizar e insertar
        #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Succesfully added')
      #else:
      #  message = CodeMessage(code=-4, message='Succesfully added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(EmpresaUpdate, CodeMessage, path='empresa/update', http_method='POST', name='empresa.update')
#siempre lleva cls y request
 def empresa_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN 
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
      #empresakey = ndb.Key(urlsafe=request.empresa_key)#convierte el string dado a entityKey
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, EmpresaList, path='empresa/list', http_method='POST', name='empresa.list')
#siempre lleva cls y request
 def empresa_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   #if user.importante==1 or user.importante==2:
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = EmpresaList(code=1) #CREA el mensaje de salida
   lstBdEmpresa = Empresa.query().fetch() #obtiene de la base de datos
   for i in lstBdEmpresa: #recorre la base de datos
             #inserta a la lista creada con los elementos que se necesiten de la base de datos
             #i.empresa_key.urlsafe() obtiene el entityKey
       #lista.append(ClientesUpdate(token='', nombre=i.nombre, status=i.status, empresa_key=i.empresa_key.urlsafe(), entityKey=i.entityKey))
    lista.append(EmpresaUpdate(token='', 
     entityKey = i.entityKey,
     codigo_empresa=i.codigo_empresa, 
     nombre_empresa = i.nombre_empresa))
      
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
      #else:
      #    message = EmpresaList(code=-3, data=[])
  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message


###########################
#### Tweets
###########################

@endpoints.api(name='tweet_api', version='v1', description='tweet REST API')
class TweetApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, TweetList, path='tweet/get', http_method='POST', name='tweet.get')
#siempre lleva cls y request
 def tweet_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   tweetentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = TweetList(code=1, data=[TweetUpdate(token='Succesfully get',
    entityKey=tweetentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    title=tweetentity.get().title, 
    description=tweetentity.get().description, 
    urlImage=tweetentity.get().urlImage)])
  except jwt.DecodeError:
   message = TweetList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TweetList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='tweet/delete', http_method='POST', name='tweet.delete')
#siempre lleva cls y request
 def tweet_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   tweetentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   tweetentity.delete()#BORRA
   message = CodeMessage(code=0, message='tweet deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, TweetList, path='tweet/list', http_method='POST', name='tweet.list')
#siempre lleva cls y request
 def tweet_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = TweetList(code=1) #CREA el mensaje de salida
   lstBd = Tweet.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(TweetUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     title=i.title, 
     decription=i.decription, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = TweetList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TweetList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TweetInput, CodeMessage, path='tweet/insert', http_method='POST', name='tweet.insert')
#siempre lleva cls y request
 def tweet_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mytweet = Tweet()
   if mytweet.tweet_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Medicine added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TweetUpdate, CodeMessage, path='tweet/update', http_method='POST', name='tweet.update')
#siempre lleva cls y request
 def tweet_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mytweet = Tweet()
   if mytweet.tweet_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='tweet updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message




###########################
#### Laboratorios
###########################

@endpoints.api(name='laboratorio_api', version='v1', description='laboratorio REST API')
class LaboratorioApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, LaboratorioList, path='laboratorio/get', http_method='POST', name='laboratorio.get')
#siempre lleva cls y request
 def laboratorio_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   laboratorioentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = LaboratorioList(code=1, data=[LaboratorioUpdate(token='Succesfully get',
    entityKey=laboratorioentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    title=laboratorioentity.get().title, 
    description=laboratorioentity.get().description, 
    urlImage=laboratorioentity.get().urlImage)])
  except jwt.DecodeError:
   message = LaboratorioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = LaboratorioList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='laboratorio/delete', http_method='POST', name='laboratorio.delete')
#siempre lleva cls y request
 def laboratorio_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   laboratorioentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   laboratorioentity.delete()#BORRA
   message = CodeMessage(code=0, message='laboratorio deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, LaboratorioList, path='laboratorio/list', http_method='POST', name='laboratorio.list')
#siempre lleva cls y request
 def laboratorio_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = LaboratorioList(code=1) #CREA el mensaje de salida
   lstBd = Laboratorio.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(LaboratorioUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     title=i.title, 
     decription=i.decription, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = LaboratorioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = LaboratorioList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(LaboratorioInput, CodeMessage, path='laboratorio/insert', http_method='POST', name='laboratorio.insert')
#siempre lleva cls y request
 def laboratorio_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mylaboratorio = Laboratorio()
   if mylaboratorio.laboratorio_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Laboratorio added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(LaboratorioUpdate, CodeMessage, path='laboratorio/update', http_method='POST', name='laboratorio.update')
#siempre lleva cls y request
 def laboratorio_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mylaboratorio = Laboratorio()
   if mylaboratorio.laboratorio_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='laboratorio updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



###########################
#### Comentarios
###########################

@endpoints.api(name='comentario_api', version='v1', description='comentario REST API')
class ComentarioApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, ComentarioList, path='comentario/get', http_method='POST', name='comentario.get')
#siempre lleva cls y request
 def comentario_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   comentarioentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = ComentarioList(code=1, data=[ComentarioUpdate(token='Succesfully get',
    entityKey=comentarioentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    title=comentarioentity.get().title, 
    description=comentarioentity.get().description, 
    urlImage=comentarioentity.get().urlImage)])
  except jwt.DecodeError:
   message = ComentarioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ComentarioList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='comentario/delete', http_method='POST', name='comentario.delete')
#siempre lleva cls y request
 def comentario_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   comentarioentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   comentarioentity.delete()#BORRA
   message = CodeMessage(code=0, message='comentario deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, ComentarioList, path='comentario/list', http_method='POST', name='comentario.list')
#siempre lleva cls y request
 def comentario_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = ComentarioList(code=1) #CREA el mensaje de salida
   lstBd = Comentario.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(ComentarioUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     title=i.title, 
     decription=i.decription, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = ComentarioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ComentarioList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ComentarioInput, CodeMessage, path='comentario/insert', http_method='POST', name='comentario.insert')
#siempre lleva cls y request
 def comentario_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mycomentario = Comentario()
   if mycomentario.comentario_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Comentario added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ComentarioUpdate, CodeMessage, path='comentario/update', http_method='POST', name='comentario.update')
#siempre lleva cls y request
 def comentario_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mycomentario = Comentario()
   if mycomentario.comentario_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='comentario updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


###########################
#### Farmacias
###########################

@endpoints.api(name='farmacia_api', version='v1', description='farmacia REST API')
class FarmaciaApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, FarmaciaList, path='farmacia/get', http_method='POST', name='farmacia.get')
#siempre lleva cls y request
 def farmacia_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   farmaciaentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = FarmaciaList(code=1, data=[FarmaciaUpdate(token='Succesfully get',
    entityKey=farmaciaentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    title=farmaciaentity.get().title, 
    description=farmaciaentity.get().description, 
    urlImage=farmaciaentity.get().urlImage)])
  except jwt.DecodeError:
   message = FarmaciaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = FarmaciaList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='farmacia/delete', http_method='POST', name='farmacia.delete')
#siempre lleva cls y request
 def farmacia_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   farmaciaentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   farmaciaentity.delete()#BORRA
   message = CodeMessage(code=0, message='farmacia deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, FarmaciaList, path='farmacia/list', http_method='POST', name='farmacia.list')
#siempre lleva cls y request
 def farmacia_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = FarmaciaList(code=1) #CREA el mensaje de salida
   lstBd = Farmacia.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(FarmaciaUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     title=i.title, 
     decription=i.decription, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = FarmaciaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = FarmaciaList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(FarmaciaInput, CodeMessage, path='farmacia/insert', http_method='POST', name='farmacia.insert')
#siempre lleva cls y request
 def farmacia_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myfarmacia = Farmacia()
   if myfarmacia.farmacia_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Drug Store added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(FarmaciaUpdate, CodeMessage, path='farmacia/update', http_method='POST', name='farmacia.update')
#siempre lleva cls y request
 def farmacia_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myfarmacia = Farmacia()
   if myfarmacia.farmacia_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='farmacia updated')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


application = endpoints.api_server([UsuariosApi, EmpresasApi, FarmaciaApi, LaboratorioApi, TweetApi, ComentarioApi, ProductsApi], restricted=False)