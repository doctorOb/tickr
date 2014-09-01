from lxml import html as lhtml

import urllib2
import sys


class Document:
	"""Given an html page as a string, convert it to a document model
	Aims to mimick the document variable in the browser."""
	def __init__(self,html):
		lxml_tree = lhtml.fromstring(html)
		self.body = collect_nodes(lxml_tree.body) #the body node, in most cases, we start iterating from here
		#This is a collection of ALL the Nodes on the page. Just a flat array
		#We should probably build this first.
		self.all = parseTree(self.body)
		self.idMap = self._build_hashMap()


	def _build_hashMap(self):
		idMap = {}
		for node in self.all:
			if node.id:
				idMap[node.id] = node
		return idMap



	def getElementById(self,id):
		"""This is most likely implemented as a hash map on most browsers.
		We can probably build this while filling the document.all collection"""
		try:
			return self.idMap[id]
		except KeyError:
			return None

	def getElementsByTagName(self,tagName):
		return self.body.getElementsByTagName(tagName)

	def getElementsByClassName(self,className):
		return self.body.getElementsByClassName(className)


class Node:
	"""Implementation of javascript DOM nodes. I'm not really sure if 
	there's a propper name for these."""

	def __init__(self,elTag,parentNode=None,children=[]):
		self.tagName = elTag.tag
		self.parentNode = parentNode
		self.children = children
		self.id = elTag.get("id")
		self.className = elTag.get("class")
		self.title = elTag.get('title')
		self.href = elTag.get('href')
		self.value = elTag.get('value')
		self.name = elTag.get('name')
		self.action = elTag.get('action')
		self.innerText = elTag.text #TODO: handle recursively


	def __repr__(self):
		ret = "<dompy.Node:{}".format(self.tagName)
		if self.id:
			ret += "#{}".format(self.id)
		if self.className:
			ret += ".{}".format(self.className)
		return ret + ">"


	def appendChild(self,child):
		self.children.append(child)

	def getElementsByTagName(self,tagName):
		ret = []
		if self.tagName == tagName:
			ret.append(self)

		for node in self.children:
			ret += node.getElementsByTagName(tagName)

		return ret

	def getElementsByClassName(self,className):
		ret = []
		if self.className and className in self.className:
			ret.append(self)

		for node in self.children:
			more = node.getElementsByClassName(className)
			if more is not None:
				ret.append(more)

		if len(ret) > 0:
			return ret[0] if len(ret) == 1 else ret
		else:
			return None


def collect_nodes(tag):
	"""
	Iterate over the children of a BStag. These may be more BStags,
	which will need to be recursively iterated over, or NavigableString
	objects, which we collect into a string and set as the node's 
	innerText
	"""
	node = Node(tag,children=[])
	childs = []
	for sub in tag:
		childs.append(collect_nodes(sub))
	
	for child in childs:
		node.appendChild(child)

	return node

def parseTree(root):
	ret = [root]
	if len(root.children) < 1:
		return ret
	for node in root.children:
		ret += parseTree(node)
	return ret






