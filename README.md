# reporter

## Introduction

Reporter is a [Flask](http://flask.pocoo.org) powered script that automatically generates html and csv AdWords reports. It has been tested on the following configuration:

- MacOS X 10.7.5
- Python 2.7.5

## Requirements

Reporter requires the following in order to run properly:

- [Xcode](https://developer.apple.com/xcode)
- [Command Line Tools](http://jaranto.blogspot.com/2012/08/os-x-unable-to-execute-clang-no-such.html)
- [Python >= 2.7](http://www.python.org/download) (MacOS X comes with python preinstalled)

## Quick Start

*Open Terminal*

	Applications > Terminal.app

*Install python modules (inside Terminal) - First time only*

	cd ~/Dropbox/Sarah\ S./reporter
	sudo easy_install pip
	sudo pip install -r requirements.txt
	sudo touch /System/Library/DTDs/sdef.dtd

*Create reports (inside Terminal) - Any time*

	cd ~/Dropbox/Sarah\ S./reporter
	./report.py create

## Scripts

Reporter comes with a built in script manager `report.py`. Use it to create reports.

### Usage

	~/Dropbox/Sarah\ S./reporter/report.py create [-h] [-f FILE]

### Examples

The following examples assume you have first run `cd ~/Dropbox/Sarah\ S./reporter`

*Use the default SWM.csv file (it is located in Dropbox/Sarah S./reporter/sources)*

	./report.py create

*Use a custom SWM.csv file (you can drag and drop the SWM file into the terminal instead of typing in the path)*

	./report.py create -f path/to/the/file.csv

*Show the help menu*

	./report.py create -h

## Configuration

All client details are located in the file `clients.yml`.
Any clients not found when running reporter will be automatically added.

## Directory Structure

    Reporter
     ├──LICENSE
     ├──README.md
     ├──app
     |    ├──__init__.py
     |    ├──emailer.py
     |    ├──renderer.py
     |    ├──static
     |    |    ├──github-1d6e450b54230462761f7f0fb692c60039b0e67c.css
     |    |    ├──github2-b4dcbb73b0e43228627f42f62e0587eed9d692fb.css
     |    ├──templates
     |         ├──base.html
     |         ├──index.html
     ├──clients.yml
     ├──config.py
     ├──exports
     |    ├──Pestforce_Leicestershire.csv
     |    ├──Pestforce_Leicestershire.html
     ├──macmailto.sh
     ├──report.py
     ├──requirements.txt
     ├──sources
          ├──PPC.csv
          ├──SWM.csv

## License

Reporter is distributed under the [BSD License](http://opensource.org/licenses/BSD-3-Clause), the same as [Flask](http://flask.pocoo.org) on which this program depends.
