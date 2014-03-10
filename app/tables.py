# -*- coding: utf-8 -*-
"""
	tables
	~~~~~~~~~~~~~~

	Process Tables (add default 'left' alignment and inline styles)
"""

from flask.ext.markdown import Extension
from markdown.extensions.tables import TableProcessor, etree


class BSTableProcessor(TableProcessor):
	""" Process Tables in a Bootstrap compatible way """
	def _build_row(self, row, parent, align, border):
		""" Given a row of text, build table cells. """
		tr = etree.SubElement(parent, 'tr')
		tag = 'td'
		if parent.tag == 'thead':
			tag = 'th'
		cells = self._split_row(row, border)
		# We use align here rather than cells to ensure every row
		# contains the same number of columns.
		for i, a in enumerate(align):
			c = etree.SubElement(tr, tag)
			try:
				c.text = cells[i].strip()
			except IndexError:
				c.text = ""

			a = (a or 'left')
			c.set('style', "text-align: %s;" % a)


class TableExtension(Extension):
	def extendMarkdown(self, md, md_globals):
		""" Add an instance of TableProcessor to BlockParser. """
		md.parser.blockprocessors.add(
			'table', BSTableProcessor(md.parser), '<hashheader')
