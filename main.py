#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    #calls self.response.out.write so you don't have to keep typing it
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    #takes a template name and resurns a string of the render template
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    #it call "write" on the template
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blogs(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    #passing variable titles in to the template so you can use the variables throughout the template.
    def render_front_main(self, title="", blog=""):
        blogs = db.GqlQuery("SELECT * FROM Blogs "
                            "ORDER BY created DESC "
                            "LIMIT 5 ")
        self.render('main-blog.html', title=title, blog=blog, blogs=blogs)

    def get(self):
        self.render_front_main()


class NewPost(Handler):
    #passing variable titles in to the template so you can use the variables throughout the template.
    def render_front_new(self, title="", blog="", error=""):
        self.render('new-post.html', title=title, blog=blog, error=error)

    def get(self):
        self.render_front_new()

    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        #add in error handling
        if title and blog:
            a = Blogs(title=title, blog=blog)
            a.put()

            self.redirect("/blog")
        else:
            error = "we need both a title and text for the blog"
            self.render_front_new(title, blog, error)

app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/newpost', NewPost)
], debug=True)
