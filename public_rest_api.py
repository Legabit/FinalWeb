import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.api import images
from google.appengine.ext import blobstore
import cloudstorage
import mimetypes
import json
import os
import jinja2

from models import Empresa
from models import Tweet
from models import Laboratorio
from models import Comentario
from models import Farmacia
jinja_env = jinja2.Environment(
 loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class DemoClass(object):
 pass

def MyClass(obj):
 return obj.__dict__


class GetTweetsHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     """id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe() 
     myEmpKey = ndb.Key(urlsafe=strKey) 
     myTweets = Tweet.query(Tweet.empresa_key == myEmpKey)
  """
     myTweets = Tweet.query()
     myList = []
     for i in myTweets:
      myObj = DemoClass()
      myObj.title = i.title
      myObj.description = i.description
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)



###########################################################################     


class UpHandler(webapp2.RequestHandler):
    def _get_urls_for(self, file_name):
        
     bucket_name = app_identity.get_default_gcs_bucket_name()
     path = os.path.join('/', bucket_name, file_name)
     real_path = '/gs' + path
     key = blobstore.create_gs_key(real_path)
     try:
      url = images.get_serving_url(key, size=0)
     except images.TransformationError, images.NotImageError:
      url = "http://storage.googleapis.com{}".format(path)

     return url


    def post(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     bucket_name = app_identity.get_default_gcs_bucket_name()
     uploaded_file = self.request.POST.get('uploaded_file')
     file_name = getattr(uploaded_file, 'filename', None)
     file_content = getattr(uploaded_file, 'file', None)
     real_path = ''

     if file_name and file_content:
      content_t = mimetypes.guess_type(file_name)[0]
      real_path = os.path.join('/', bucket_name, file_name)

      with cloudstorage.open(real_path, 'w', content_type=content_t,
       options={'x-goog-acl': 'public-read'}) as f:
       f.write(file_content.read())

      key = self._get_urls_for(file_name)
      self.response.write(key)


class LoginHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('login.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)


class TweetHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('tweet.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class GetComentariosHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     """id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe() 
     myEmpKey = ndb.Key(urlsafe=strKey) 
     myComentarios = Comentario.query(Comentario.empresa_key == myEmpKey)
  """
     myComentarios = Comentario.query()
     myList = []
     for i in myComentarios:
      myObj = DemoClass()
      myObj.title = i.title
      myObj.description = i.description
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)
class ComentarioHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('comentario.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class GetLaboratoriosHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     """id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe() 
     myEmpKey = ndb.Key(urlsafe=strKey) 
     myLaboratorios = Laboratorio.query(Laboratorio.empresa_key == myEmpKey)
  """
     myLaboratorios = Laboratorio.query()
     myList = []
     for i in myLaboratorios:
      myObj = DemoClass()
      myObj.title = i.title
      myObj.description = i.description
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)

class LaboratorioHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('laboratorio.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class GetFarmaciasHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     """id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe() 
     myEmpKey = ndb.Key(urlsafe=strKey) 
     myFarmacias = Farmacia.query(Farmacia.empresa_key == myEmpKey)
  """
     myFarmacias = Farmacia.query()
     myList = []
     for i in myFarmacias:
      myObj = DemoClass()
      myObj.title = i.title
      myObj.description = i.description
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)
class FarmaciaHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('farmacia.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class MainHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('index.html', template_context))


   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/medicines', TweetHandler),
    ('/comentarios', ComentarioHandler),
    ('/laboratorios', LaboratorioHandler),
    ('/farmacias', FarmaciaHandler),
    ('/up', UpHandler),
    ('/gettweets', GetTweetsHandler),
    ('/getlaboratorios', GetLaboratoriosHandler),
    ('/getfarmacias', GetFarmaciasHandler),
    ('/getcomentarios', GetComentariosHandler),
], debug = True)
