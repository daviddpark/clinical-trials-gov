#!/usr/bin/env python
#
#	cTAKES and RegEx wizardry
#
#	2012-12-14	Created by Pascal Pfiffner
#

import re


def split_inclusion_exclusion(string):
	""" Returns a tuple of lists describing inclusion and exclusion criteria.
	"""
	
	if not string or len(string) < 1:
		raise Exception('No string given')
	
	# split on newlines
	rows = re.compile("(?:\n\s*){2,}").split(string)
	
	# loop all rows
	inc = []
	exc = []
	at_inc = False
	at_exc = False
	
	for row in rows:
		string = list_trim(row)
		if len(row) < 1 or 'none' == string:
			continue
		
		# detect switching to inclusion criteria
		if re.search('^inclusion criteria', string, re.IGNORECASE) is not None \
			and re.search('exclusion', string, re.IGNORECASE) is None:
			at_inc = True
			at_exc = False
		
		# detect switching to exclusion criteria
		elif re.search('exclusion criteria', string, re.IGNORECASE) is not None \
			and re.search('inclusion', string, re.IGNORECASE) is None:
			at_inc = False
			at_exc = True
		
		# assign accordingly
		elif at_inc:
			inc.append(string)
		elif at_exc:
			exc.append(string)
	
	if len(inc) < 1 or len(exc) < 1:
		print "No inclusion or exclusion criteria found in:\n-----\n%s\n-----\n" % string
	
	# -- TEST: join back into sentences
	inc = ['. '.join(inc)] if len(inc) > 0 else []
	exc = ['. '.join(exc)] if len(exc) > 0 else []
	# --
	
	return (inc, exc)


def list_trim(string):
	""" Trim text phases that are part of the string because the string was
	pulled off of a list, e.g. a leading "-" or "1."
	"""
	
	string.strip()
	string = re.sub('\s+', ' ', string)						# multi-whitespace
	string = re.sub('^-\s+', '', string, count=1)			# leading "-"
	string = re.sub('^\d+\.\s+', '', string, count=1)		# leading "1."
	
	return string

