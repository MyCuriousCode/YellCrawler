import urllib
import time
import sys

class crawler:
	pages = []
	keyword = ""
	location = ""

	def setKeyword(self,keywordInput):
		self.keyword = keywordInput

	def setLocation(self,locationInput):
		self.location = locationInput

	def createPages(self):
		if self.keyword != "" and self.location != "":
			for i in range(1,100):
				page = 'http://www.yell.com/ucs/UcsSearchAction.do?startAt=10&keywords='+self.keyword+'&location='+self.location+'&scrambleSeed=18441148&ssm=1&showOoa=10&ppcStartAt=0&pageNum=%s' % i
				self.pages.append(page)
		else:
			print "Location or Keyword not set\nUse setKeyword or setLocation functions before precedding"
			sys.exit(0)

	def crawl(self,inputDiv):
		# Company
		company = []

		# End Span
		endSpanStr = '</span>'

		# Company Name
		companyStr = 'data-omniture="LIST:COMPANYNAME" title="'
		companyStart = inputDiv.find(companyStr)
		companyEnd = inputDiv.find('"',companyStart+len(companyStr))
		companyName = inputDiv[companyStart+len(companyStr)+len('View '):companyEnd]

		# Telephone
		telephoneStr = 'Tel: <span class="tel">'
		telephoneStart = inputDiv.find(telephoneStr)
		telephoneStop = inputDiv.find(endSpanStr,telephoneStart)
		if telephoneStart > -1:
			telephone = inputDiv[telephoneStart+len(telephoneStr):telephoneStop]
		else:
			telephone = ''

		# Mobile
		mobileStr = 'Mob: <span class="tel">'
		mobileStart = inputDiv.find(mobileStr)
		mobileEnd = inputDiv.find(endSpanStr,mobileStart)
		if mobileStart > -1:
			mobile = inputDiv[mobileStart+len(mobileStr):mobileEnd]
		else:
			mobile = ''

		# Street Address
		streetAddressStr = '<span class="street-address">'
		streetAddressStart = inputDiv.find(streetAddressStr)
		streetAddressStop = inputDiv.find(endSpanStr,streetAddressStart)
		if streetAddressStart > -1:
			streetAddress = inputDiv[streetAddressStart+len(streetAddressStr):streetAddressStop]
			streetAddress = streetAddress.strip()
			streetAddress = streetAddress.replace(",","")
		else:
			streetAddress = ''

		# Locality
		localityStr = '<span class="locality">'
		localityStart = inputDiv.find(localityStr)
		localityStop = inputDiv.find(endSpanStr,localityStart)
		if localityStart > -1:
			locality = inputDiv[localityStart+len(localityStr):localityStop]
		else:
			locality = ''
		
		# Region
		regionStr = '<span class="region">'
		regionStart = inputDiv.find(regionStr)

		if regionStart == -1:
			regionStr = '<span class="region"><strong>'
			regionStart = inputDiv.find(regionStr)
			regionEnd = inputDiv.find('</strong>',regionStart)
		else:
			regionEnd = inputDiv.find('</span>',regionStart)

		if regionStart > -1:
			region = inputDiv[regionStart+len(regionStr):regionEnd]
			region = region.replace('<strong>','')
			region = region.replace('</strong>','')
		else:
			region = ''

		# Postcode
		postcodeStr = '<span class="postal-code">'
		postcodeStart = inputDiv.find(postcodeStr)
		postcodeStop = inputDiv.find(endSpanStr,postcodeStart)
		if postcodeStart > -1:
			postcode = inputDiv[postcodeStart+len(postcodeStr):postcodeStop]
			postcode = postcode.replace('  ',' ')
		else:
			postcode = ''

		# Keyword
		keywordStr = 'title="Show only those results in'
		keywordStart = inputDiv.find(keywordStr)
		keywordEnd = inputDiv.find('>',keywordStart)
		if keywordStart > -1:
			keyword = inputDiv[keywordStart+len(keywordStr):keywordEnd]
			keyword = keyword[keyword.find('">')+2:keywordEnd]
			keyword = keyword.replace('&amp;','&')
			keyword = keyword.replace('"','')
		else:
			keyword = ''
		
		# Website
		websiteStr = '<li class="website"> <a class="url" target="_blank" href='
		websiteStart = inputDiv.find(websiteStr)
		websitesStop = inputDiv.find(' id',websiteStart)
		if websiteStart > -1:
			website = inputDiv[websiteStart+len(websiteStr)+1:websitesStop-1]
		else:
			website = ''

		company = [companyName,telephone,mobile,streetAddress,locality,region,postcode,website,keyword]

		return company


	def start(self):
		self.createPages()

		# Div tags to recognise start and end of company entry
		divStartStr = '<div class="parentListing ui-draggable"'
		divStartStr = '<div class=" parentListing"'
		divEndStr = '<div class="pusherDiv"></div> '

		if self.pages:
			i = 0
			for page in self.pages:
				f = urllib.urlopen(page)
				#f = urllib.urlopen('index.html')
				f = f.read()

				while f:
					divStart = f.find(divStartStr)
					divEnd = f.find(divEndStr,divStart)

					if divStart > -1:
						company = self.crawl(f[divStart:divEnd])
						print company
						i = i + 1
						f = f[divEnd:]
					else:
						break

				time.sleep(15)
			

