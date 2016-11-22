import os
from os import path as p
from datetime import date as d

# module vars
_basedir = p.dirname(__file__)
_user = os.environ.get('USER', os.environ.get('USERNAME'))

# configurable vars
__APP_NAME__ = 'Proposer'
__YOUR_NAME__ = 'Reuben Cummings'
__YOUR_COMPANY__ = 'Nerevu Development'
__YOUR_POSITION__ = 'Managing Director'
__YOUR_EMAIL__ = 'rcummings@nerevu.com'
__YOUR_SKYPE__ = _user
__YOUR_PHONE__ = ['+255 789 477 319', '+254 703 576 035']
__YOUR_WEBSITE__ = 'http://nerevu.com'

# calculated vars
app = __APP_NAME__.lower()
year = d.today().strftime("%Y")
date = d.today().strftime("%B %d, %Y")
site_keys = (
	'author', 'author_company', 'author_position', 'author_email',
	'author_skype', 'author_phone', 'author_url', 'year', 'date')

site_values = (
	__YOUR_NAME__, __YOUR_COMPANY__, __YOUR_POSITION__, __YOUR_EMAIL__,
	__YOUR_SKYPE__, __YOUR_PHONE__, __YOUR_WEBSITE__, year, date)

# configuration
class Config(object):
	SITE = dict(zip(site_keys, site_values))
	DEBUG = False
	TESTING = False
	HOST = '127.0.0.1'
	EXPORT_DIR = p.join(_basedir, 'exports')
	INFO_PATH = p.join(_basedir, 'info.yml')
	STYLE = 'development'
	TYPE = 'html'
	TABLE = '<table class="table table-striped">'

	BOOTSTRAP_USE_MINIFIED = False
	BOOTSTRAP_USE_CDN = False
	BOOTSTRAP_FONTAWESOME = False
	BOOTSTRAP_HTML5_SHIM = False


class Production(Config):
	HOST = '0.0.0.0'
	BOOTSTRAP_USE_MINIFIED = True
	BOOTSTRAP_USE_CDN = True
	BOOTSTRAP_FONTAWESOME = True


class Development(Config):
	DEBUG = True


class Test(Config):
	TESTING = True
