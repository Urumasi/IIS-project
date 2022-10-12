from flask import render_template

from . import public

@public.route('/')
def root():
    return render_template("index.html")
