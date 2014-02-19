from flask import abort, json, render_template


def offline_render(md):
    """Renders the specified markup locally."""
    import misaka as m
    return m.html(md, extensions=m.EXT_TABLES)


def github_render(md):
	"""Renders the specified markup using the GitHub API."""
	import requests
	url = 'https://api.github.com/markdown/raw'
	headers = {'content-type': 'text/plain'}

	r = requests.post(url, headers=headers, data=md)

	# Relay HTTP errors
	if r.status_code != 200:
		try:
			message = r.json()['message']
		except:
			message = r.text
		abort(r.status_code, message)

	return r.text


def render_app(app):
	"""Renders the markup"""
	with app.test_client() as c:
		response = c.get('/')
		encoding = response.charset
		return response.data.decode(encoding)


def render_content(md):
	"""Renders the specified markup and returns the result."""
	return offline_render(md)


def render_page(md, report, style_urls=None, styles=None):
	"""Renders the specified markup text to an HTML page."""
	content = render_content(md)
	style_urls = (style_urls or [])
	styles = (styles or [])
	kwargs = {
		'content': content, 'style_urls': style_urls,
		'styles': styles, 'report': report}

	return render_template('index.html', **kwargs)

