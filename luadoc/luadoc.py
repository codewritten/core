#  **************************************************************************************************************
#  **************************************************************************************************************
#
#	Name: 		luadoc.py
#	Author:		Paul Robson (paul@robsons.org.uk)
#	Purpose:	Scans lua files generating documentation in HTML from inline comments.
#	Created: 	9th March 2015
#	Released:	-
#	Version:	0.1
#
#  **************************************************************************************************************
#  **************************************************************************************************************

import re

class NullDoc:
	def __init__(self,body):											
		self.text = body 															# save full text
		self.parts2 = re.match("^(\\w+)\\s+(.*)$",body)								# attempt to split into 2 parts.
		self.parts3 = re.match("^(\\w+)\\s+(\\w+)\\s+(.*)$",body)					# attempt to split into 3 parts.
		if self.parts3 is not None:
			print(self.parts3.groups())

	def toHTML(self,text):
		return "<p>"+(text.replace("|","</p><p>"))+"</p>"							# convert text to HTML equivalent

	def bodyRender(self):													
		return ""
	def tableRender(self):		
		return ""

class MethodDoc(NullDoc):
	pass

class ParamDoc(NullDoc):
	def tableRender(self):
		if self.parts2 is None:														# requires name,type and comment
			raise Exception("Badly formatted @return")
	return "<td>returns</td><td>"+self.parts2.group(1)+"</td><td>"+self.parts2.group(2)+"</td>"
	pass

class ReturnDoc(NullDoc):
	def tableRender(self):
		if self.parts2 is None:														# requires type and comment
			raise Exception("Badly formatted @return")
	return "<td>returns</td><td>"+self.parts2.group(1)+"</td><td>"+self.parts2.group(2)+"</td>"

class DocumentationGenerator:
	def __init__(self,fileName):
		source = open(fileName).readlines()											# Read source code into file.
		source = [x.strip() for x in source if x.strip() != ""]						# Remove leading, trailing, blank
		self.docObjects = []														# List of documentation objects
		current = "" 																# Currently constructed.
		for line in source:															# work through code.
			if line[:3] == "---":													# have we found a documentation comment
				comment = line[3:].strip()											# extract the actual comment.
				if comment != '' and comment[0] == '@':								# is it a new preprocessor ?
					self.process(current)											# clear out the old one.
					current = ""
				current = current + "  "+ comment 									# append the comment to current.
			else:
				if current != "":													# something outstanding
					self.process(current)											# process any comment outstanding.
					current = ""													# erase it.
					print("<RENDER>")

	def process(self,line):
		line = line.strip() 														# remove spaces.
		line = line.replace("\t"," ")												# replace tabs.
		while line.find("  ") >= 0:													# remove all multiple spacing.
			line = line.replace("  "," ")
		if line != "":
			match = re.match("^@\\s*(\\w+)\\s*(.*)$",line)							# look for correct line.
			if match is None:														# didn't get it ...
				raise Exception("Badly formed inline documentation")
			name = match.group(1).lower()											# documentation type.
			if name == "method":													# add the appropriate object.
				self.docObjects.append(MethodDoc(match.group(2)))
			elif name == "param":
				self.docObjects.append(ParamDoc(match.group(2)))
			elif name == "return":
				self.docObjects.append(ReturnDoc(match.group(2)))
			else:
				raise Exception("Unknown documentation type "+name)

dc = DocumentationGenerator("testfile.lua")


#  **************************************************************************************************************
#	Date		Version		Notes
#	====		=======		=====
#	09-Mar-15	0.1 		First created
#
#  **************************************************************************************************************