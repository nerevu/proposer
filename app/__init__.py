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
from flask import Flask, g, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.markdown import Markdown


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

	return app
