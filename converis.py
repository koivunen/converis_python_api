import requests
import os,sys
import logging
from xml.etree import ElementTree

#logging.basicConfig(level=logging.DEBUG)

class CInfoObject():
	def __init__(self,cris,rtype):
		self.rtype = rtype
		self.cris = cris
	
	def makeurl(self,what,rest):
		ret = "{base}/ws/public/infoobject/{what}/{rtype}/{rest}".format(base=self.cris.url,rtype = self.rtype,what=what,rest = rest)
		print(ret)
		return ret
	
	def makereq(self,what,rest):
		url = self.makeurl(what, rest )
		response = requests.get( url )
		if response.status_code != 200:
			response.raise_for_status()

		tree = ElementTree.fromstring(response.content)
		return tree
		
		
class Converis():
	def __init__(self,url):
		self.url = url
	
	def pers(self,id):
		return CPerson(id,self)
		
	def orga(self,id):
		return COrganization(id,self)
		
	def card(self,id):
		return CCard(id,self)
	
	def publ(self,id):
		return CPublication(id,self)
		
class CPerson(CInfoObject):

	def __init__(self,personid,cris):
		CInfoObject.__init__(self, cris, "Person")
		self.id = personid
		
	def cards(self):
		tree = self.makereq('getrelated',"{0}/pers_has_card".format(self.id) )
		ret=[]
		for cardelem in tree.getchildren():
			card = self.cris.card(cardelem.get('id'))
			ret.append(card)
		return ret
		
	def get(self):
		return self.makereq('get',"{0}".format(self.id) )
	
	def publications():
		raise Exception("unimplemented")
	
class CPublication(CInfoObject):
	def __init__(self,pubid,cris):
		CInfoObject.__init__(self, cris, "Publication")
		self.id = pubid
		
	def get(self):
		return self.makereq('get',"{0}".format(self.id) )
	
class COrganization(CInfoObject):
	def __init__(self,orgid,cris):
		CInfoObject.__init__(self, cris, "Organization")
		self.id = orgid
		
	def cards(self):
		return requests.get( "{0}/ws/public/infoobject/get/Person/{1}".format(self.cris.url,self.id) )
	
	def people(self):
		raise Exception("unimplemented")
	
	def publications(self):
		raise Exception("unimplemented")
		
class CCard(CInfoObject):
	def __init__(self,cardid,cris):
		CInfoObject.__init__(self, cris, "Card")
		self.id = cardid

	def publications(self):
		tree = self.makereq('getrelated',"{0}/publ_has_card".format(self.id) )
		ret=[]
		for cardelem in tree.getchildren():
			card = self.cris.publ(cardelem.get('id'))
			ret.append(card)
		return ret
		
	def people(self):
		raise Exception("unimplemented")

if __name__ == "__main__":
	converis = Converis("https://research.utu.fi/converis")

	#person = converis.pers(900334).get() # get person info
	#print(person.get('id'))
	
	cards = converis.pers(900334).cards() # get cards of person
	card = cards[0]
	print("card",card,card.rtype)
	
	pubs = card.publications() # get publications of card
	print(pubs)
	
	pub = pubs[0].get()
	
	print(ElementTree.tostring(pub, encoding='utf8', method='xml'))
	
	import pdb; pdb.set_trace()
	
	#publ = converis.publ(pubs[0].id) # Get publication info
