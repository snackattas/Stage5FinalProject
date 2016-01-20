import webapp2
import jinja2
import os
import time
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        error = 0
        note_text = self.request.get("note_text")
        Help = Helper()
        data = Help.get_data()
        [disableLesson, disableConcept, disableInformation] = Help.radio_buttons()
        self.render('template.html', data = data, disableLesson = disableLesson, 
                    disableConcept = disableConcept, disableInformation = disableInformation, 
                    error = error)

class ErrorPage(Handler):
    def get(self):
        error = 1
        note_text = self.request.get("note_text")
        Help = Helper()
        data = Help.get_data()
        [disableLesson, disableConcept, disableInformation] = Help.radio_buttons()
        self.render('template.html', data = data, disableLesson = disableLesson, 
                    disableConcept = disableConcept, disableInformation = disableInformation, 
                    error = error)

class Submit(Handler):
    def post(self):
        note_text = self.request.get("note_text")
        type_of_note = self.request.get('type_of_note')
        if note_text and type_of_note and not note_text.isspace():
            ID = Note()
            ID.note_text = note_text
            ID.type_of_note = type_of_note
            ID.put()
            delay = 1 #  1 second
            time.sleep(delay)
            self.redirect('/')
        else:
            self.redirect('/ErrorPage')

class Helper:
    def get_data(self):
        return Note.query().order(Note.date)
    def radio_buttons(self):
        most_recent_entry = 1
        qry = Note.query().order(-Note.date).fetch(most_recent_entry)
        if qry:
            type_of_note = qry[0].type_of_note
            if type_of_note == 'Lesson':
                return ['disabled', '', 'disabled']
            if type_of_note == 'Concept':
                return ['disabled', 'disabled', '']
            else:
                return ['', '', '']
        else:
            return ['','disabled','disabled']

class Note(ndb.Model):
    type_of_note = ndb.StringProperty()
    note_text = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

app = webapp2.WSGIApplication([('/', MainPage),
                              ('/ErrorPage', ErrorPage),
                              ('/Submit', Submit)],
                              debug=True)

