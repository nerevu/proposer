# -*- coding: utf-8 -*-
"""
	app
	~~~~~~~~~~~~~~

	Provides the flask application

Modified from GRIP https://github.com/joeyespo/grip
"""

import os
import re
import config
import requests

from urlparse import urlparse
from traceback import format_exc
from flask import Flask, url_for, send_from_directory
from .renderer import render_page


def create_app(config_mode=None, config_file=None):
	"""Starts a server to render the specified file or directory containing a README."""

	# Flask application
	app = Flask(__name__)
	if config_mode:
		app.config.from_object(getattr(config, config_mode))
	elif config_file:
		app.config.from_pyfile(config_file)
	else:
		app.config.from_envvar('APP_SETTINGS', silent=True)

	# Setup style cache
	style_cache_path = app.config['STYLE_CACHE_DIRECTORY']
	# Get initial styles
	style_urls = list(app.config['STYLE_URLS'] or [])
	styles = []

	# Get styles from style source
	@app.before_first_request
	def retrieve_styles():
		"""Retrieves the style URLs from the source and caches them, if requested."""

		# Get style URLs from the source HTML page
		retrieved_urls = _get_style_urls(
			app.config['STYLE_URLS_SOURCE'], app.config['STYLE_URLS_RE'],
			style_cache_path, app.config['DEBUG_GRIP'])

		style_urls.extend(retrieved_urls)
		styles.extend(_get_styles(app, style_urls))
		style_urls[:] = []

	# Views
	@app.route('/')
	def render():
		md = app.config['MD']
		report = app.config['REPORT']
		return render_page(md, report, style_urls, styles)

	@app.route('/cache/<path:filename>')
	def render_cache(filename=None):
		return send_from_directory(style_cache_path, filename)

	return app

def _get_style_urls(source_url, pattern, style_cache_path, debug=False):
	"""Gets the specified resource and parses all style URLs in the form of the specified pattern."""
	try:
		# TODO: Add option to clear the cached styles
		# Skip fetching styles if there's any already cached
		if style_cache_path:
			cached = _get_cached_style_urls(style_cache_path)
			if cached:
				return cached

		# Find style URLs
		r = requests.get(source_url)
		if not 200 <= r.status_code < 300:
			print ' * Warning: retrieving styles gave status code', r.status_code
		urls = re.findall(pattern, r.text)

		# Cache the styles
		if style_cache_path:
			_cache_contents(urls, style_cache_path)
			urls = _get_cached_style_urls(style_cache_path)

		return urls
	except Exception as ex:
		if debug:
			print format_exc()
		else:
			print ' * Error: could not retrieve styles:', str(ex)
		return []


def _get_styles(app, style_urls):
	"""Gets the content of the given list of style URLs."""
	styles = []
	for style_url in style_urls:
		if not urlparse(style_urls[0]).netloc:
			with app.test_client() as c:
				response = c.get(style_url)
				encoding = response.charset
				content = response.data.decode(encoding)
		else:
			content = requests.get(style_url).text
		styles.append(content)
	return styles


def _get_cached_style_urls(style_cache_path):
	"""Gets the URLs of the cached styles."""
	files = os.listdir(style_cache_path)
	cached_styles = filter(lambda x: x.endswith('css'), files)
	return [url_for('render_cache', filename=style) for style in cached_styles]



def _write_file(filename, contents):
	"""Creates the specified file and writes the given contents to it."""
	with open(filename, 'w') as f:
		f.write(contents.encode('utf-8'))


def _cache_contents(urls, style_cache_path):
	"""Fetches the given URLs and caches their contents in the given directory."""
	for url in urls:
		basename = url.rsplit('/', 1)[-1]
		filename = os.path.join(style_cache_path, basename)
		contents = requests.get(url).text
		_write_file(filename, contents)
		print ' * Downloaded', url
