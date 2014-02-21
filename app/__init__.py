# -*- coding: utf-8 -*-
"""
	app
	~~~~~~~~~~~~~~

	Provides the flask application
"""

from __future__ import print_function

import config
import yaml

from os import path as p
from flask import Flask, g, render_template, url_for, redirect
from flask.ext.bootstrap import Bootstrap
from flask.ext.markdown import Markdown
from flask_weasyprint import HTML
from weasyprint.css import find_stylesheets

def _get_styles(app, style_urls):
	"""Gets the content of the given list of style URLs."""
	styles = []
	for style_url in style_urls:
		with app.test_client() as c:
			response = c.get(style_url)
		styles.append(response.data)
	return styles


def create_app(config_mode=None, config_file=None):
	"""Create webapp instance"""

	# Flask application
	app = Flask(__name__)
	Bootstrap(app)
	Markdown(app, extensions=['tables', 'toc'])

	if config_mode:
		app.config.from_object(getattr(config, config_mode))
	elif config_file:
		app.config.from_pyfile(config_file)
	else:
		app.config.from_envvar('APP_SETTINGS', silent=True)

	# set g variables
	@app.before_request
	def before_request():
		stream = file(app.config['INFO_PATH'], 'r')
		[g.__setattr__(i[0], i[1]) for i in yaml.safe_load(stream).items()]
		g.site = app.config['SITE']

	# Views
	@app.route('/<style>/')
	def index(style):
		return render_template('%s.html' % style)

	@app.route('/render/<style>/')
	def render(style):
		html = HTML(string=render_template('%s.html' % style))
		stylesheets = find_stylesheets(html.root_element, html.media_type, html.url_fetcher)
		urls = [sheet.base_url for sheet in stylesheets]
		style_urls = filter(lambda x: x.endswith('css'), urls)
		styles = _get_styles(app, style_urls)
		return render_template('%s.html' % style, styles=styles)

	return app
