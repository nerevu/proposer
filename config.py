import os
import yaml
from os import path as p
from datetime import date as d

# module vars
_basedir = p.dirname(__file__)
_user = os.environ.get('USER', os.environ.get('USERNAME'))
signature = '''

Kind regards

Sarah Stocks
South West Marketing | Moorland View | Wembury Road | Plymouth | Devon | PL9 0DQ
Tel: 01752 863 400
www.southwest-marketing.co.uk
'''

# configuration
class Config(object):
	SIGNATURE = signature
	CLIENT_DATA_FILE = p.join(_basedir, 'clients.yml')
	stream = file(CLIENT_DATA_FILE, 'r')
	CLIENT_DATA = yaml.safe_load(stream)
	MAIL_SCRIPT = p.join(_basedir, 'macmailto.sh')
	SWM_PATH = p.join(_basedir, 'sources', 'swm.csv')
	EXPORT_DIR = p.join(_basedir, 'exports')
	STYLE_CACHE_DIRECTORY = p.join(_basedir, 'app', 'static')
	EMAIL = False
	DEBUG = False
	DEBUG_GRIP = False
	STYLE_URLS = []
	STYLE_URLS_SOURCE = 'https://github.com/joeyespo/grip'
	STYLE_URLS_RE = '<link.+href=[\'"]?([^\'" >]+)[\'"]?.+media=[\'"]?(?:screen|all)[\'"]?.+rel=[\'"]?stylesheet[\'"]?.+/>'


class Production(Config):
	EMAIL = True


class Development(Config):
	DEBUG = True
	DEBUG_GRIP = True
