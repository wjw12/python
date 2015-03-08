#!python3
# -*- coding: utf-8 -*-
import re,urllib.request,http.client,threading

rootURL = 'http://www.pixiv.net'
startURL = 'http://www.pixiv.net/search.php?order=date_d'
cookie = 'hide_premium_promotion_modal=1424864384; login_ever=yes; OX_plg=swf|shk|pm; PHPSESSID=6871999_a25be4b09af2fb8a26f4ec27612baeda; p_ab_id=9; __utma=235335808.1558172411.1424864193.1424869428.1424873116.3; __utmb=235335808.3.10.1424873116; __utmz=235335808.1424864193.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=6871999=1; _ga=GA1.2.1558172411.1424864193; visit_ever=yes; __gads=ID=dfb874fd3ef5812a:T=1424864229:S=ALNI_MbybU42Aes0RIAL9oRRz3NqJ3F6Mg; device_token=1fc18d5ddea142f1ae8f9a19804cf695; module_orders_mypage=%5B%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; __utmc=235335808' 
#使用前要修改cookie
class spider:
	def __init__(self,keyword,startPage=1):
		self.rootURL = rootURL
		self.startURL = startURL
		self.page = startPage
		self.keyword = urllib.parse.quote(keyword) #将搜索关键词汉字转换为%xx
		self.startURL += (u'&word='+self.keyword+u'&p=')
	def getHrefList(self,page): #获取赞数为三位数以上的图片页面超链接
		pattern = r'<div>|</div>'.encode('utf-8')
		replaceDIV = re.compile(pattern)
		repl = '\n'.encode('utf-8')
		page = re.sub(replaceDIV,repl,page)
		#替换<div></div>为换行符 \n 
		#注意：pattern和repl必须是相同类型(bytes或str)，此处都是bytes
		reg = r'<a href="(.*medium.*)"><h1.*tooltip="\d{3,}'.encode('utf-8')
		hrefRe = re.compile(reg)
		return re.findall(hrefRe,page)
	def getPage(self):
		pageURL = self.startURL + str(self.page)
		req = urllib.request.Request(pageURL)
		req.add_header('Cookie',cookie)
		print ('Opening ', pageURL)
		resp = urllib.request.urlopen(req)
		self.page += 1
		try:
			page = resp.read()
		except e:
			page = e.partial
			print ('IncompleteRead') #调试时发现偶尔出IncompleteRead错误，读出页面部分内容然后继续
		return page
	def saveImg(self):
		counter = 0
		while True:
			page = self.getPage() #搜索列表页
			hrefList = self.getHrefList(page)
			for href in hrefList:
				imgPageURL = self.rootURL + href.decode('utf-8') #包含图片的页面
				req = urllib.request.Request(imgPageURL)
				req.add_header('Cookie',cookie)
				print ('Opening image page ', imgPageURL)
				try:
					resp = urllib.request.urlopen(req)
				except:
					print ('Error opening ',imgPageURL)
					continue
				imgPage = resp.read()
				pattern = r'<div>|</div>'.encode('utf-8')
				replaceDIV = re.compile(pattern)
				repl = '\n'.encode('utf-8')
				imgPage = re.sub(replaceDIV,repl,imgPage)  
				#替换<div></div>为换行符 \n
				reg = r'<img alt="(.*)" width.*data-src="(http.*jpg)" .*class="original-image"'.encode('utf-8')
				imgRe = re.compile(reg)
				imgList = re.findall(imgRe,imgPage)
				for img in imgList:
					filename = img[0].decode('utf-8') + '.jpg'
					imgURL = img[1].decode('utf-8') #第一组是文件名，第二组是图片URL
					print ('Downloading ',filename.encode('gb18030'),' from ',imgURL) 
					try:
						req = urllib.request.Request(imgURL)
						referer = imgPageURL
						req.add_header('Referer',referer) #没有这个header会出现403 error
						resp = urllib.request.urlopen(req,timeout=30)
						data = resp.read()
					except:
						print ('Error saving image from ', imgURL)
						continue
					image = open(removeIllegalChars(filename),'wb')
					image.write(data)
					image.close()
					print (filename.encode('gb18030'),' saved')
					#gb18030能编码日文汉字，gbk有时会出错
					counter += 1

class spiderThread(threading.Thread):
	def __init__(self,startPage=1):
		threading.Thread.__init__(self)
		self.spider = spider(u'saber',startPage)
		print ('Start page ',startPage)
	def run(self):
		lock = threading.Lock()
		with lock:
			self.spider.saveImg()

def removeIllegalChars(filename): #处理文件名中不合法字符  \ / ? : * " > < |
	pattern = r'[\\/\?:\*"><\|]*'
	return re.sub(pattern,"",filename)

for i in range(30):
	page = 400+i*30
	t = spiderThread(page)
	t.start()
