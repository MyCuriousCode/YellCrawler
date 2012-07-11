import urllib
import mysql.connector
import time

# MySQL Conneciton
conn = mysql.connector.connect(host='localhost',database='coursekit',user='root',password='toor')
c = conn.cursor()


def dataMiner(inputDiv):
	# End Span
	EndSpanStr = '</span>'

	# Company Name
	companyNameStr = '<span class="fn org"'
	companyNameStart = inputDiv.find(companyNameStr)
	companyNameStop = inputDiv.find(EndSpanStr,companyNameStart)
	companyName = inputDiv[companyNameStart+len(companyNameStr)+1:companyNameStop]
	companyName = companyName.replace('&amp;','&')

	# Telephone
	telephoneStr = 'Tel: <span class="tel">'
	telephoneStart = inputDiv.find(telephoneStr)
	telephoneStop = inputDiv.find(EndSpanStr,telephoneStart)
	if telephoneStart > -1:
		telephone = inputDiv[telephoneStart+len(telephoneStr):telephoneStop]
	else:
		telephone = ''

	# Mobile
	mobileStr = 'Mob: <span class="tel">'
	mobileStart = inputDiv.find(mobileStr)
	mobileEnd = inputDiv.find(EndSpanStr,mobileStart)
	if mobileStart > -1:
		mobile = inputDiv[mobileStart+len(mobileStr):mobileEnd]
	else:
		mobile = ''

	# Street Address
	streetAddressStr = '<span class="street-address">'
	streetAddressStart = inputDiv.find(streetAddressStr)
	streetAddressStop = inputDiv.find(EndSpanStr,streetAddressStart)
	if streetAddressStart > -1:
		streetAddress = inputDiv[streetAddressStart+len(streetAddressStr):streetAddressStop]
	else:
		streetAddress = ''

	# Locality
	localityStr = '<span class="locality">'
	localityStart = inputDiv.find(localityStr)
	localityStop = inputDiv.find(EndSpanStr,localityStart)
	if localityStart > -1:
		locality = inputDiv[localityStart+len(localityStr):localityStop]
	else:
		locality = ''
	
	# Region
	regionStr = '<span class="region"><strong>'
	regionStart = inputDiv.find(regionStr)
	regionEnd = inputDiv.find('</strong>',regionStart)
	if regionStart > -1:
		region = inputDiv[regionStart+len(regionStr):regionEnd]
	else:
		region = ''

	# Postcode
	postcodeStr = '<span class="postal-code">'
	postcodeStart = inputDiv.find(postcodeStr)
	postcodeStop = inputDiv.find(EndSpanStr,postcodeStart)
	if postcodeStart > -1:
		postcode = inputDiv[postcodeStart+len(postcodeStr):postcodeStop]
	else:
		postcode = ''

	# Keyword
	keywordStr = '<div class="keywords">'
	keywordStart = inputDiv.find(keywordStr)
	keywordEnd = inputDiv.find('</a>',keywordStart)
	if keywordStart > -1:
		keyword = inputDiv[keywordStart+len(keywordStr):keywordEnd]
		keyword = keyword[keyword.find('">')+2:keywordEnd]
		keyword = keyword.replace('&amp;','&')
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


	# Insert company into MySQL Database
	v = """insert into companies(name,telephone,mobile,street_address,locality,region,postcode,keyword,website) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %  (companyName,telephone,mobile,streetAddress,locality,region,postcode,keyword,website)
	c.execute(v)
	conn.commit()

	print '%s has been added' % companyName




pages = []

for i in range(1,100):
	urlStr = 'http://www.yell.com/ucs/UcsSearchAction.do?startAt=10&keywords=cleaning&location=Berkshire&scrambleSeed=18441148&ssm=1&showOoa=10&ppcStartAt=0&pageNum=%s' % i
	pages.append(urlStr)
	urlStr = 'http://www.yell.com/ucs/UcsSearchAction.do?startAt=10&keywords=restaurant&location=Berkshire&scrambleSeed=50960820&ssm=1&showOoa=10&ppcStartAt=0&pageNum=%s' % i
	pages.append(urlStr)
	urlStr = 'http://www.yell.com/ucs/UcsSearchAction.do?startAt=10&keywords=security&location=Berkshire&scrambleSeed=50960820&ssm=1&showOoa=10&ppcStartAt=0&pageNum=%s' % i
	pages.append(urlStr)


divStartStr = '<div class="parentListing ui-draggable"'
divStartStr = '<div class=" parentListing"'
divEndStr = '<div class="pusherDiv"></div> '

i = 0
for page in pages:
	# Get Page
	f =urllib.urlopen(page)
	f = f.read()

	while f:
		divStart = f.find(divStartStr)
		divEnd = f.find(divEndStr,divStart)

		if divStart > -1:
			dataMiner(f[divStart:divEnd])
			i = i + 1
			f = f[divEnd:]
		else:
			break

	print '\n%d Companies added\n' % i
	time.sleep(20)


print "\n *** IMPORT COMPLETE ***\n"

