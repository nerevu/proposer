#!/usr/bin/env python
# -*- coding: utf-8 -*-

# prompt user for info
# compose email

import csv
import io
import pandas as pd
import numpy as np

from os import path as p
from pprint import pprint
from tabulate import tabulate

from flask import current_app as app
from flask.ext.script import Manager
from app import create_app
from app.renderer import render_app
from app.emailer import macmailto

manager = Manager(create_app)
manager.add_option(
	'-m', '--cfgmode', dest='config_mode', default='Development')
manager.add_option('-f', '--cfgfile', dest='config_file', type=p.abspath)


def readCSV(file):
	rows = []

	with io.open(file, 'rU') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		[rows.append(row) for row in reader]

	return rows


def export_md(md, html_file, report):
	app.config['MD'] = md
	app.config['REPORT'] = report
	print 'Exporting to', html_file

	content = render_app(app)
	with io.open(html_file, 'w', encoding='utf-8') as f:
		f.write(content)


@manager.option('-f', '--file', help='path to the SWM file, defaults to sources/SWM.csv')
def create(file=None):
	"""Create AdWords Report"""

	data = []
	swm_path = (file or app.config['SWM_PATH'])
	raw = readCSV(swm_path)
	top = {r[0]: r[1] for r in raw[:5]}
	report, period = top['Name'], top['Dates']

	subject = '%s for %s' % (report, period)
	for d in raw[6:-1]:
		d[3], d[4] = d[4], d[3]
		d[5] = d[5].replace('%', '')
		d[7] = d[7].replace(',', '')
		data.append(tuple(d))

	index = [raw[5][-1]]
	index.extend(raw[5][:3])
	dtype = [
		('Account', 'a32'), ('Campaign', 'a32'),
		('Ad group', 'a32'), ('Impressions', np.int), ('Clicks', np.int),
		('CTR (%)', 'float64'), ('Avg. CPC (GBP)', 'float64'),
		('Cost (GBP)', 'float64'), ('Avg. position', 'float64'),
		('Customer ID', 'a16')]

	nparray = np.array(data, dtype=dtype)
	df = pd.DataFrame.from_records(nparray, index=index).sort()
	scrpt = app.config['MAIL_SCRIPT']

	for g in df.groupby(level=index[0]).groups:
		# create main data frame
		group = df.ix[g]
		client_name = group.ix[[0]].index[0][0]
		safe_name = client_name.replace(' ', '_').replace('&', 'and').replace('/', '-')
		new_index = group.index.names[1:]
		sorted_df = group.reset_index().sort(['Campaign', 'Impressions'], ascending=[1, 0])
		new_df = sorted_df.set_index(new_index).ix[:,group.columns]
		unfrmttd_df = new_df.reset_index()
		data_dtl = unfrmttd_df.values
		columns = [c for c in unfrmttd_df.columns]

		# create totals
		totals = unfrmttd_df.ix[:,[columns[2], columns[3]]].sum()
		ctr = totals[columns[3]] / float(totals[columns[2]]) * 100.
		cost = unfrmttd_df[columns[6]].sum()
		cpc = cost / totals[columns[3]]
		ave_pos = np.average(unfrmttd_df[columns[7]], weights=unfrmttd_df[columns[2]])
		values = totals.values.tolist()
		values.extend([ctr, cpc, cost, ave_pos])
		data_ave = zip(columns[2:], values)

		# create files
		export_file = p.join(app.config['EXPORT_DIR'], '%s.csv' % safe_name)
		new_df.to_csv(export_file, encoding='utf-8')
		md = "##%s Account: %s\n" % (client_name, period)
		md += "###Account Wide Averages\n"
		md += tabulate(data_ave, headers=['Metric', 'Value'], floatfmt=',.2f', tablefmt='pipe')
		md += "\n\n###Campaign Details\n"
		md += tabulate(data_dtl, headers=columns, floatfmt=',.2f', tablefmt='pipe')
		html_file = p.join(app.config['EXPORT_DIR'], '%s.html' % safe_name)
		export_md(md, html_file, report)

		try:
			email = app.config['CLIENT_DATA'][g]['email']
			salutation = app.config['CLIENT_DATA'][g]['salutation']

		except KeyError:
			import yaml
			print '%s (%s) not found. Please enter details below.' % (
				client_name, g)
			email = raw_input("Email address: ")
			salutation = raw_input("Salutation: ")
			print 'Saving data for %s (%s)' % (client_name, g)
			data_file = app.config['CLIENT_DATA_FILE']
			new_data = {g: {'email': email, 'salutation': salutation}}
			with open(data_file, 'a') as f:
				f.write(yaml.dump(new_data, default_flow_style=False))

		body = salutation + app.config['SIGNATURE']
		macmailto(scrpt, email, subject, body, html_file)
		print "Composing email to %s at %s." % (client_name, email)
		raw_input("Press any key to continue or <ctrl>+C to abort...")


if __name__ == '__main__':
	manager.run()
