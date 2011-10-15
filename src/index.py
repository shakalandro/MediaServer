import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
    MEDIA = {'MUSIC': 'Music',
             'MOVIES': 'Movies'}
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_args = {self.MEDIA.MUSIC:[],
                         self.MEDIA.MOVIES: []}
        for file in os.listdir(self.MEDIA.MUSIC):
            template_args[self.MEDIA.MUSIC].append(file)
        for file in os.listdir(self.MEDIA.MOVIES):
            template_args[self.MEDIA.MOVIES].append(file)
        self.response.out.write(template.render('home.html', template_args, True))
        
class MoviePage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        movie = self.request.path.split('/')[-1]
        self.response.out.write(movie);
            
class MusicPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        song = self.request.path.split('/')[-1]
        self.response.out.write(song);


application = webapp.WSGIApplication([('/', MainPage),
                                      ('/movie', MoviePage),
                                      ('/music', MusicPage)
                                     ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
