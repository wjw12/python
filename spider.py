# -*- coding: utf-8 -*-
import re,urllib2,httplib
rootURL = 'http://dou.lesile.net/'
startURL = 'http://dou.lesile.net/thread0806.php?fid=8&page='
class spider:
	def __init__(self,keyword):
		self.rootURL = rootURL
		self.startURL = startURL
		self.page = 1
		self.keyword = keyword.decode('utf-8').encode('gb2312')
		self.img = None
	def getHrefList(self,page): #获取包含搜索词的超链接列表
		reg = r'<h3><a href="(.*html)" target="_blank" id="">.*' + self.keyword + r'.*</a></h3>'
		hrefRe = re.compile(reg)
		return re.findall(hrefRe,page)
	def getPage(self):
		pageURL = self.startURL + str(self.page)
		req = urllib2.Request(pageURL)
		print 'Opening ' + pageURL
		resp = urllib2.urlopen(req)
		self.page += 1
		try:
			page = resp.read()
		except httplib.IncompleteRead, e: #处理IncompleteRead异常
			print 'IncompleteRead ' + pageURL
			page = e.partial
		return page
	def fetchImageData(self,imgURL):
		try:
			print 'Downloading from ' + imgURL
			self.img = urllib2.urlopen(imgURL,timeout=20).read()
		except:
			print 'Error saving image ' + imgURL
			self.img = None
	def saveImg(self):
		counter = 0
		while True:
			page = self.getPage()
			hrefList = self.getHrefList(page)
			for href in hrefList:
				imgPageURL = self.rootURL + href
				print 'Opening image page ' + imgPageURL
				try:
					resp = urllib2.urlopen(imgPageURL)
				except:
					print 'Error opening ' + imgPageURL
					continue
				imgPage = resp.read()
				replaceBR = re.compile('<br>')
				imgPage = re.sub(replaceBR,'\n',imgPage)  #替换<br>为换行符 \n
				reg = r'<input type=\'image\' src=\'(http.*\.jpg)\''
				imgRe = re.compile(reg)
				imgList = re.findall(imgRe,imgPage)
				for img in imgList:
					self.fetchImageData(img)
					if self.img is not None:
						filename = str(counter) + '.jpg'
						image = file(filename,'wb')
						image.write(self.img)
						image.close()
						print filename + ' saved.'
						counter += 1
						self.img = None
					else:
						print 'No image data, nothing is saved'

if __name__ == '__main__':
	mySpider = spider('少女')
	mySpider.saveImg()