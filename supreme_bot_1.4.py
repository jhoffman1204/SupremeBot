from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import datetime
import sys
from bs4 import BeautifulSoup
import urllib


# self.label_list = ['Item Keyword' , 'Item Type' , 'Color' , 'Size' , 'First Name' , 
# 'Last Name' , 'Email' , 'Phone' , 'Address' , 'City', 'Zip Code' , 
# 'State' , 'Country' , 'Month' , 'Year' , 'Card Number', 'CVV' ]
def find_item():
	
	file_name = sys.argv[1]
	print("reading from " , file_name)
	r = open(file_name, "r") 

	target_word = file_name = sys.argv[2]
	type_item = file_name = sys.argv[3]
	target_color = file_name = sys.argv[4]
	size = file_name = sys.argv[5]
	
	if(size == "none"):
		print("size not defined")
		sizeChange = False
	else:
		print("size has been defined")
		sizeChange = True
	size = size.title()
		
	if(target_color == "none"):
		print("color not defined")
		colorChange = False
	else:
		print("color has been defined")
		colorChange = True
		
	target_color = target_color.title()					# color needs to be capitalized

	nameFirst = r.readline().split(" ")[1].strip()
	nameLast = r.readline().split(" ")[1].strip()

	# Checkout info with fields 
	email = r.readline().split(" ")[1].strip()
	phone = r.readline().split(" ")[1].strip()
	address = r.readline().split(" ")
	address = address[1] + " " + address[2] + " " + address[3]

	city = r.readline().split(" ")[1].strip()
	zip = r.readline().split(" ")[1].strip()
	state = r.readline().split(" ")[1].strip()
	country = r.readline().split(" ")[1].strip()
	
	card_number = r.readline().split(" ")[1].strip()
	month = r.readline().split(" ")[1].strip()
	year = r.readline().split(" ")[1].strip()

	addressTwo = ""

	cardOne = card_number[0:5]
	cardTwo = card_number[5:9]
	cardThree = card_number[9:13]
	cardFour = card_number[13:16]
	cvv = r.readline().split(" ")[1]
	target_time = sys.argv[6]

	print(target_time)

	print(cardOne)
	print(cardTwo)
	print(cardThree)
	print(cardFour)
	
	print(city)
	

	baselink = "http://www.supremenewyork.com"
			

	print(type_item)
	print(target_word)
	print(target_color)

	# type_item = "Jackets"
	# target_word = "Tiger"
	# target_color = "White"

	r = urllib.request.urlopen("http://www.supremenewyork.com/shop")
	soup = BeautifulSoup(r,"html.parser")


	# this does the whole googling process which isn't needed at all

	# this will open chrome which we might not need to do yet
	# driver.get("http://www.supremenewyork.com/shop")

	items_soups = soup.find_all(class_= type_item)
	links = []

	driver = webdriver.Firefox(executable_path="geckodriver.exe")
	
	if(target_time != 'none'):
		while True:
			now = datetime.datetime.now()
			currentTime = now.strftime('%I:%M:%S')
			if (currentTime == target_time):
				break
				
	now = datetime.datetime.now()
	currentTime = now.strftime('%I:%M:%S')
	print(currentTime)

	for item in items_soups:
		href = item.find('a', href=True)
		links.append(href.get('href'))

	newlinks = []
	for link in links:
		newlinks.append(baselink + link)

	targetLink = ""
	for i in range(0,len(newlinks)):
		r = urllib.request.urlopen(newlinks[i])
		soup = BeautifulSoup(r,"html.parser")
		title = soup.find(class_="protect")
		if target_word in title.get_text():
			targetLink = newlinks[i]
			break
	
	while(targetLink == ""):
		print("Nothing Found for that keyword")
		r = urllib.request.urlopen("http://www.supremenewyork.com/shop")
		soup = BeautifulSoup(r,"html.parser")
		items_soup = soup.find(class_= "shop")
		href = items_soup.find_all('a', href=True)
		for a in href:
				r = urllib.request.urlopen(baselink + a.get('href'))
				soup = BeautifulSoup(r,"html.parser")
				sub_details = soup.find("div", {"id": "details"})
				title = soup.find(class_="protect")
				if target_word in title.get_text():
					targetLink = baselink + a.get('href')
					print("new Target Link: " + targetLink)
					break
	
	# print("Target Link: " , targetLink)
	original_target = targetLink
			
	if(colorChange):
		try:
			colors = soup.find("div", {"id": "details"})
			links  = colors.find_all('a')
			for a in links:
				colorLink = (baselink + a.get('href'))
				r = urllib.request.urlopen(baselink + a.get('href'))
				soup = BeautifulSoup(r,"html.parser")
				sub_details = soup.find("div", {"id": "details"})
				#print(sub_details)
				color = sub_details.find(class_= "style protect")
				if target_color in color.get_text():
					targetLink = colorLink
					break
		except:
			print("Color " , target_color , " not available :: Switching to Default Color")
			targetLink = original_target

	print("target link " , targetLink)
	driver.get(targetLink)                                                 # Opens the URL to the item selected

	# Executes only if we are trying to get a size
	try:
		if (sizeChange):
			sizeBox = driver.find_element_by_xpath('//*[@id="s"]')
			sizeBox.click()
			select = Select(sizeBox)
			try:
				select.select_by_visible_text(size)
			except NoSuchElementException:
				try:
					if not(select.first_selected_option.text == size):
						select.select_by_visible_text("Medium")
				except NoSuchElementException:
					pass
	except:
		print("Size " , size , " not available :: Using Default Size")

	# find the color


	while (len(driver.find_elements_by_xpath('//*[@id="add-remove-buttons"]/input')) == 0):
		driver.refresh()

	# Once page has loaded click button 
	addToCart_button = driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input')
	addToCart_button.click()
	time.sleep(1)

	# While webpage does not have checkout button
	while (len(driver.find_elements_by_xpath('//*[@id="cart"]/a[2]')) == 0):
		driver.refresh()
	
	# Once checkout button has appeared click it
	checkout_botton = driver.find_element_by_xpath('//*[@id="cart"]/a[2]')
	checkout_botton.click()
	time.sleep(.6)
	
	driver.refresh()
	# Handles Shipping Information\
	while (len(driver.find_elements_by_xpath('//*[@id="order_billing_city"]')) == 0):
		driver.refresh()
	cityField = driver.find_element_by_xpath('//*[@id="order_billing_city"]')
	print("city: ", city)
	cityField.send_keys(city)
	nameField = driver.find_element_by_xpath('//*[@id="order_billing_name"]')
	nameField.send_keys(nameFirst)
	nameField.send_keys(" ")
	nameField.send_keys(nameLast)
	emailField = driver.find_element_by_xpath('//*[@id="order_email"]')
	emailField.send_keys(email)
	phoneField = driver.find_element_by_xpath('//*[@id="order_tel"]')
	phoneField.send_keys(phone)
	addressField = driver.find_element_by_xpath('//*[@id="bo"]')
	addressField.send_keys(address)
	addressFieldTwo = driver.find_element_by_xpath('//*[@id="oba3"]')
	addressFieldTwo.send_keys(addressTwo)
	zipField = driver.find_element_by_xpath('//*[@id="order_billing_zip"]')
	zipField.send_keys(zip)

	# Handles card info
	monthField = driver.find_element_by_xpath("//*[@id='credit_card_month']/option[@value='01']")
	monthField.click()

	yearField = driver.find_element_by_xpath("//*[@id='credit_card_year']/option[@value='2020']")
	yearField.click()

	countryField = driver.find_element_by_xpath("//*[@id='order_billing_country']/option[@value='USA']")
	countryField.click()



	# checkbox and card info
	cardField = driver.find_element_by_xpath('//*[@id="nnaerb"]')
	cardField.click()
	cardField.clear()
	cardField.send_keys(cardOne)
	cardField.click()
	cardField.send_keys(cardTwo)
	cardField.click()
	cardField.send_keys(cardThree)
	cardField.click()
	cardField.send_keys(cardFour)

	cvvField = driver.find_element_by_xpath('//*[@id="orcer"]')
	cvvField.click()
	cvvField.send_keys(cvv)

	# state and country
	stateField = driver.find_element_by_xpath("//*[@id='order_billing_state']/option[@value='NY']")
	stateField.click()
	
	# click the checkbox
	checkbox = driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p[2]/label/div/ins')
	checkbox.click()
	
	# payment_button = driver.find_element_by_xpath('//*[@id="pay"]/input')
	# payment_button.click()
	
	now = datetime.datetime.now()
	finish_time = now.strftime('%I:%M:%S')
	print(finish_time)
	print("Total Time: " , int(finish_time[-2:]) - int(currentTime[-2:]) , " Seconds")\

	time.sleep(100)

find_item()