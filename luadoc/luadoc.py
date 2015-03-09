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

class MethodDefinition:
	def __init__(self):
		self.methodName = ""														# method name
		self.method = None															# tuple name,description
		self.returnValue = None														# tuple type,description
		self.parameters = []														# tuples name,type,description

	def process(self,line):
		print(self,line)

class DocumentationGenerator:
	def __init__(self,fileName):
		source = open(fileName).readlines()											# Read source code into file.
		source = [x.strip() for x in source if x.strip() != ""]						# Remove leading, trailing, blank
		source = ["---@render" if x != "" and x[:2] != "--" else x for x in source]	# anything not comment becomes @render
		source = [x for x in source if len(x) >= 3 and x[:3] == "---"]				# remove non doc comments.
		source = [x[3:].strip() for x in source]									# remove --- and spaces.
		source = " ".join(source)													# now a sequence of @s.
		while source.find("@render @render") >= 0: 									# remove duplicate @renders
			source = source.replace("@render @render","@render")
		source = source.replace("\t"," ").replace("\n"," ")							# replace controls.
		while source.find("  ") >= 0:												# remove all double spaces.
			source = source.replace("  "," ")
		source = source.split("@")													# split around @
		source = [x.strip() for x in source]										# remove any trailing spaces.
		while source[0] == '' or source[0] == 'render':								# remove leading blanks/renders
			source = source[1:]
		self.docObjects = []														# list of document objects
		currentDocObject = None														# current being written to.
		for line in source:															# work through.
			if line == "render":													# output a doc object ?
				self.docObjects.append(currentDocObject)							# append to list.
				currentDocObject = None 											# no current.
			else:
				if currentDocObject is None:										# create if required.
					currentDocObject = MethodDefinition()
				currentDocObject.process(line)										# and let it handle the line.

dc = DocumentationGenerator("testfile.lua")


#  **************************************************************************************************************
#	Date		Version		Notes
#	====		=======		=====
#	09-Mar-15	0.1 		First created
#
#  **************************************************************************************************************