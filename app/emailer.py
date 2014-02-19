#!/usr/bin/env python

'''Utilities for sending e-mail'''


def _fix_addersses(**kwargs):
	for headername in ('address', 'to', 'cc', 'bcc'):
		try:
			headervalue = kwargs[headername]
			if not headervalue:
				del kwargs[headername]
				continue
			elif not isinstance(headervalue, basestring):
				# assume it is a sequence
				headervalue = ','.join(headervalue)

		except KeyError:
			pass
		except TypeError:
			raise TypeError('string or sequence expected for "%s", '
				'%s found' % (headername, type(headervalue).__name__))
		else:
			translation_map = {'%': '%25', '&': '%26', '?': '%3F'}
			for char, replacement in translation_map.items():
				headervalue = headervalue.replace(char, replacement)
			kwargs[headername] = headervalue

	return kwargs


def mailto_format(**kwargs):
	# @TODO: implement utf8 option

	kwargs = _fix_addersses(**kwargs)
	parts = []
	for headername in ('to', 'cc', 'bcc', 'subject', 'body', 'attach'):
		if kwargs.has_key(headername):
			headervalue = kwargs[headername]
			if not headervalue:
				continue
			if headername in ('address', 'to', 'cc', 'bcc'):
				parts.append('%s=%s' % (headername, headervalue))
			else:
				headervalue = encode_rfc2231(headervalue) # @TODO: check
				parts.append('%s=%s' % (headername, headervalue))

	mailto_string = 'mailto:%s' % kwargs.get('address', '')
	if parts:
		mailto_string = '%s?%s' % (mailto_string, '&'.join(parts))

	return mailto_string


def mailto(address, cc=None, bcc=None, subject=None, body=None, attach=None):
# http://code.activestate.com/recipes/511443-cross-platform-startfile-and-mailto-functions/

	'''Send an e-mail using the user's preferred composer.

	Open the user's preferred e-mail composer in order to send a mail to
	address(es) that must follow the syntax of RFC822. Multiple addresses
	may be provided (for address, cc and bcc parameters) as separate
	arguments.

	All parameters provided are used to prefill corresponding fields in
	the user's e-mail composer. The user will have the opportunity to
	change any of this information before actually sending the e-mail.

	address - specify the destination recipient
	cc		- specify a recipient to be copied on the e-mail
	bcc		- specify a recipient to be blindly copied on the e-mail
	subject - specify a subject for the e-mail
	body	- specify a body for the e-mail. Since the user will be able
			to make changes before actually sending the e-mail, this
			can be used to provide the user with a template for the
			e-mail text may contain linebreaks
	attach	- specify an attachment for the e-mail. must point to
			an existing file

	'''
	import webbrowser
	from email.Utils import encode_rfc2231

	mailto_string = mailto_format(**locals())
	return webbrowser.open(mailto_string)


def macmailto(scrpt, address, subject, body, attach, native=False):
	if native:
		# http://stackoverflow.com/a/16101613/408556
		from applescript import AppleScript
		cmd = AppleScript(scrpt)
		return cmd.run(address, subject, body, attach)
	else:
		from subprocess import call
		cmd = '"%s" "%s" "%s" "%s" "%s"' % (scrpt, address, subject, body, attach)
		return call(cmd, shell=True)

