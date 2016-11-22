# -*- coding: utf-8 -*-
"""
	app
	~~~~~~~~~~~~~~

	Provides the flask application
"""
__version__ = "0.6.0"

from __future__ import print_function

import config
import yaml

from flask import Flask, g, render_template, url_for, Response
from flask.ext.bootstrap import Bootstrap
from flask.ext.markdown import Markdown
from flask_weasyprint import HTML, render_pdf
from weasyprint.css import find_stylesheets
from app.tables import TableExtension
from datetime import timedelta, date as d

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
	md = Markdown(app, extensions=['toc'])
	md.register_extension(TableExtension)


	if config_mode:
		app.config.from_object(getattr(config, config_mode))
	elif config_file:
		app.config.from_pyfile(config_file)
	else:
		app.config.from_envvar('APP_SETTINGS', silent=True)

	table = app.config['TABLE']

	@app.before_request
	def before_request():
		# set g variables
		stream = file(app.config['INFO_PATH'], 'r')
		[g.__setattr__(i[0], i[1]) for i in yaml.safe_load(stream).items()]
		g.site = app.config['SITE']
		g.valid_until = (d.today() + timedelta(days=g.days_valid)).strftime(
			"%B %d, %Y")

	# Views
	@app.route('/<style>/')
	def index(style):
		return render_template('%s.html' % style).replace('<table>', table)

	@app.route('/render/<style>/')
	@app.route('/render/<style>/<type>/')
	def render(style, type='html'):
		if type.startswith('html'):
			html = render_template('%s.html' % style).replace('<table>', table)
			html_doc = HTML(string=html)
			stylesheets = find_stylesheets(
				html_doc.root_element, html_doc.media_type, html_doc.url_fetcher)
			urls = [sheet.base_url for sheet in stylesheets]
			style_urls = filter(lambda x: x.endswith('css'), urls)
			styles = _get_styles(app, style_urls)
			kwargs = {'styles': styles}
			return render_template('%s.html' % style, **kwargs).replace('<table>', table)
		elif type.startswith('pdf'):
			kwargs = {'to_print': True}
			return render_pdf(url_for('index', style=style))
		elif type.startswith('png'):
			kwargs = {'to_print': True}
			html = render_template('%s.html' % style, **kwargs).replace('<table>', table)
			html_doc = HTML(string=html)
			return Response(html_doc.write_png(), mimetype='image/png')
		else:
			pass

	return app
