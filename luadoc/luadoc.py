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

import re,datetime

class MethodDefinition:
	def __init__(self):
		self.methodName = ""														# method name
		self.method = None															# tuple name,description
		self.returnValue = None														# tuple type,description
		self.parameters = []														# tuples name,type,description
		self.fileName = "" 															# where it comes from in source

	def process(self,line):
		match = re.match("^method\\s+(\\S+)\\s+(.*)$",line)							# match method <name> <desc>
		ok = False
		if match is not None:
			self.method = match.groups()
			self.methodName = self.method[0]
			ok = True
		match = re.match("^param\\s+(\\S+)\\s+(\\S+)\\s+(.*)$",line)				# match param <name> <type> <desc>
		if match is not None:
			self.parameters.append(match.groups())
			ok = True
		match = re.match("^return\\s+(\\S+)\\s+(.*)$",line)
		if match is not None:														# match return <type> <desc>
			self.returnValue = match.groups()
			ok = True
		if not ok:																	# doesn't match
			raise Exception("Cannot process '"+line+"'")

	def toHTML(self,txt):
		return "<p>"+(txt.replace("|","</p><p>"))+"</p>"							# text -> HTML.

	def dump(self):
		print(self.methodName)														# just for debugging.
		print(self.method)
		print(self.returnValue)
		print(self.parameters)

	def render(self):																# render as HTML
		render = '<div id="title">Method: '+self.methodName+'</div>\n'
		render = render + '<div id="body"><i> Defined in "'+self.fileName+'"</i></div>\n'
		render = render + '<div id="body">'+self.toHTML(self.method[1])+'</div>\n'
		render = render + "<table>\n"
		if len(self.parameters) > 0 or self.returnValue is not None:
			render = render + self.renderRow("<b>Parameter</b>","<b>Type</b>","<b>Description</b>")
		for p in self.parameters:
			render = render + self.renderRow(p[0],p[1],p[2])
		if self.returnValue is not None:
			render = render + self.renderRow("returns:",self.returnValue[0],self.returnValue[1])
		render = render + "</table>\n"
		return render

	def renderRow(self,name,type,description):
		render = "    <tr>\n"
		render = render + "        <td>"+name+"</td>\n"
		render = render + "        <td>"+type+"</td>\n"
		render = render + "        <td>"+description+"</td>\n"
		render = render + "    </tr>\n"
		return render

class DocumentationGenerator:
	def __init__(self):
		self.docObjects = []														# list of document objects

	def parse(self,fileName):
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
		currentDocObject = None														# current being written to.
		for line in source:															# work through.
			if line == "render":													# output a doc object ?
				currentDocObject.fileName = fileName 								# save filename
				self.docObjects.append(currentDocObject)							# append to list.
				currentDocObject = None 											# no current.
			else:
				if currentDocObject is None:										# create if required.
					currentDocObject = MethodDefinition()
				currentDocObject.process(line)										# and let it handle the line.
		self.docObjects.sort(key=lambda x: x.methodName)							# sort documentation objects by method name

	def render(self,fileName = "documentation.html"):
		render = '<!DOCTYPE html>\n'
		render = render + '<html>\n'
		render = render + '<head>\n'
		render = render + '<link rel="stylesheet" href="luadoc.css">\n'
		render = render + '</head>\n'
		render = render + '<body>\n'
		for do in self.docObjects:
			render = render + do.render()
		render = render + '<br />\n'
		render = render + '<div><i>Generated by luadoc.py on '+str(datetime.datetime.now())+'</i></div>\n'
		render = render + '</body>\n'
		render = render + '</html>\n'
		if fileName is not None:
			open(fileName,"w").write(render)
		return render

dc = DocumentationGenerator()
dc.parse("testfile.lua")
dc.render()

#  **************************************************************************************************************
#	Date		Version		Notes
#	====		=======		=====
#	09-Mar-15	0.1 		First created
#
#  **************************************************************************************************************