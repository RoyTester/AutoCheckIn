# -*-coding:utf-8 -*-
import random
import re
import time
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

import PIL.Image as image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


class Crack:
	def __init__(self):
		self.url = 'https://www.ssru.xyz/login/'
		option = Options()
		option.add_argument('--headless')
		self.browser = webdriver.Chrome360(chrome_options=option)
		self.wait = WebDriverWait(self.browser, 10)
		self.BORDER = 6

	def open(self):
		"""
		打开浏览器,并输入查询内容
		"""
		self.browser.get(self.url)
		time.sleep(3)
		# self.browser.find_element_by_id('go_on').click()
		# time.sleep(5)
		# def findkey():
		# 	try:
		keyword = self.wait.until(EC.presence_of_element_located((By.ID,'id_userfield')))
		pwd = self.wait.until(EC.presence_of_element_located((By.ID,'id_password')))
		keyword.send_keys('username')
		pwd.send_keys('password')
			# except:
			# 	print('404 not found')
			# 	self.browser.quit()

		#bowton = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn btn-success pull-right green-btn')))
		#bowton.click()
		time.sleep(2)
		# slider = self.browser.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
		# ActionChains(self.browser).move_to_element(slider).perform()

	def get_images(self, bg_filename = 'bg.jpg', fullbg_filename = 'fullbg.jpg'):
		"""
		获取验证码图片
		:return: 图片的location信息
		"""
		bg = []
		fullgb = []
		while bg == [] and fullgb == []:
			bf = BeautifulSoup(self.browser.page_source, 'lxml')
			bg = bf.find_all('div', class_ = 'gt_cut_bg_slice')
			fullgb = bf.find_all('div', class_ = 'gt_cut_fullbg_slice')
		bg_url = re.findall('url\(\"(.*)\"\);', bg[0].get('style'))[0].replace('webp', 'jpg')
		fullgb_url = re.findall('url\(\"(.*)\"\);', fullgb[0].get('style'))[0].replace('webp', 'jpg')
		bg_location_list = []
		fullbg_location_list = []
		for each_bg in bg:
			location = {}
			location['x'] = int(re.findall('background-position: (.*)px (.*)px;',each_bg.get('style'))[0][0])
			location['y'] = int(re.findall('background-position: (.*)px (.*)px;',each_bg.get('style'))[0][1])
			bg_location_list.append(location)
		for each_fullgb in fullgb:
			location = {}
			location['x'] = int(re.findall('background-position: (.*)px (.*)px;',each_fullgb.get('style'))[0][0])
			location['y'] = int(re.findall('background-position: (.*)px (.*)px;',each_fullgb.get('style'))[0][1])
			fullbg_location_list.append(location)

		urlretrieve(url = bg_url, filename = bg_filename)
		print('缺口图片下载完成')
		urlretrieve(url = fullgb_url, filename = fullbg_filename)
		print('背景图片下载完成')
		return bg_location_list, fullbg_location_list

	def get_merge_image(self, filename, location_list):
		"""
		根据位置对图片进行合并还原
		:filename:图片
		:location_list:图片位置
		"""
		im = image.open(filename)
		new_im = image.new('RGB', (260,116))
		im_list_upper=[]
		im_list_down=[]

		for location in location_list:
			if location['y'] == -58:
				im_list_upper.append(im.crop((abs(location['x']),58,abs(location['x']) + 10, 166)))
			if location['y'] == 0:
				im_list_down.append(im.crop((abs(location['x']),0,abs(location['x']) + 10, 58)))

		new_im = image.new('RGB', (260,116))

		x_offset = 0
		for im in im_list_upper:
			new_im.paste(im, (x_offset,0))
			x_offset += im.size[0]

		x_offset = 0
		for im in im_list_down:
			new_im.paste(im, (x_offset,58))
			x_offset += im.size[0]

		new_im.save(filename)

		return new_im

	def is_pixel_equal(self, img1, img2, x, y):
		"""
		判断两个像素是否相同
		:param image1: 图片1
		:param image2: 图片2
		:param x: 位置x
		:param y: 位置y
		:return: 像素是否相同
		"""
		# 取两个图片的像素点
		pix1 = img1.load()[x, y]
		pix2 = img2.load()[x, y]
		threshold = 60
		if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(pix1[2] - pix2[2] < threshold)):
			return True
		else:
			return False

	def get_gap(self, img1, img2):
		"""
		获取缺口偏移量
		:param img1: 不带缺口图片
		:param img2: 带缺口图片
		:return:
		"""
		left = 43
		for i in range(left, img1.size[0]):
			for j in range(img1.size[1]):
				if not self.is_pixel_equal(img1, img2, i, j):
					left = i
					return left
		return left

	def get_track(self, distance):
		"""
		根据偏移量获取移动轨迹
		:param distance: 偏移量
		:return: 移动轨迹
		"""
		# 移动轨迹
		track = []
		# 当前位移
		current = 0
		# 减速阈值
		mid = distance * 4 / 5
		# 计算间隔
		t = 0.2
		# 初速度
		v = 0
		# 多往右移动10长度
		distance += 10
		while current < distance:
			if current < mid:
				# 加速度为随机数
				a = 2
			else:
				# 加速度为随机负数
				a = -3
			# 初速度v0
			v0 = v
			# 当前速度v = v0 + at
			v = v0 + a * t
			# 移动距离x = v0t + 1/2 * a * t^2
			move = v0 * t + 1 / 2 * a * t * t
			# 当前位移
			current += move
			# 加入轨迹
			track.append(round(move))
		# 加入往回移动轨迹
		for i in range(3):
			track.append(-2)
		for i in range(4):
			track.append(-1)
		return track

	def get_slider(self):
		"""
		获取滑块
		:return: 滑块对象
		"""
		while True:
			try:
				slider = self.browser.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
				break
			except:
				time.sleep(1)
		return slider

	def move_to_gap(self, slider, track):
		"""
		拖动滑块到缺口处
		:param slider: 滑块
		:param track: 轨迹
		:return:
		"""
		'''
		1.获取滑块之后及释放滑块之前要加入延时
		2.往回移动之前延时0.5s
		3.获取列表索引不使用index方法而是使用enumerate函数（有重复项）
		'''
		self.browser.execute_script('arguments[0].scrollIntoView()', slider)#将元素通过滚动条滚动使其可见
		ActionChains(self.browser).click_and_hold(slider).perform()
		# self.browser.execute_script('arguments[0].click()', slider)
		time.sleep(1)
		for index, x in enumerate(track):
			if index == len(track)-7:
				time.sleep(0.5)
			ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
		time.sleep(1)
		ActionChains(self.browser).release().perform()

	def crack(self):
		# 打开浏览器
		self.open()

		# 保存的图片名字
		bg_filename = 'bg.jpg'
		fullbg_filename = 'fullbg.jpg'

		# 获取图片
		bg_location_list, fullbg_location_list = self.get_images(bg_filename, fullbg_filename)

		# 根据位置对图片进行合并还原
		bg_img = self.get_merge_image(bg_filename, bg_location_list)
		fullbg_img = self.get_merge_image(fullbg_filename, fullbg_location_list)

        # 获取缺口位置
		gap = self.get_gap(fullbg_img, bg_img)
		print('缺口位置', gap)

		track = self.get_track(gap-self.BORDER)
		print('滑动滑块')
		print(track)
		# # 拖动滑块到缺口处
		slider = self.get_slider()
		# # 点按呼出缺口
		self.move_to_gap(slider, track)
		time.sleep(2)
		# self.browser.find_element_by_id('unchat').click()
		# time.sleep(1)
		bowton = self.browser.find_element_by_id('embed-submit')
		self.browser.execute_script('arguments[0].click()', bowton)#使用js后端脚本点击而不是前端事件
		time.sleep(5)
		try:
			self.browser.find_element_by_link_text("每日签到").click()
		except:
			crack.crack()
			return
		time.sleep(2)
		try:
			self.browser.find_element_by_id('embed-submit').click()
		except:
			print("已签到")
		time.sleep(2)
		self.browser.find_element_by_link_text("仪表盘").click()
		time.sleep(3)
		value = self.browser.find_element_by_id('tran-remain-value').text
		value1 = self.browser.find_element_by_id('tran-used-value').text
		# value= re.sub('\D','',value)
		print('*'*60)
		print('已使用{:.2f}G流量'.format(float(value1)/1024))
		print('剩余{:.2f}G流量'.format(float(value)/1024))
		print('*'*60)
		time.sleep(2)
		self.browser.quit()


if __name__ == '__main__':
	# print('开始验证')
	crack = Crack()
	crack.crack()
	# print('验证成功')
	crack.browser.quit()