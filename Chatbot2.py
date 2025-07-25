#Khai báo các thư viện cần thiết
import os
import playsound
import speech_recognition as sr
import time
import sys
import pyttsx3
import ctypes # thư viện giúp Python gọi các hàm trong ngôn ngữ C 
import wikipedia
import datetime
import json #JSON là JavaScript Object Notation, để python hỗ trợ đọc từ json cần thư viện này, nếu đọc đối tượng object trong json thì khi qua python sẽ là kiểu dữ liệu dict
import re 
import webbrowser
import smtplib
import requests   #thư viện requests, urllib, urllib.request là 3 thư viện phổ biến để truy cập vào http
import urllib
import urllib.request as urllib2 #thư viện này chủ yếu dùng để mở và lấy url
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
from datetime import date, datetime 

path=ChromeDriverManager().install()

def speak(text):
	print("Robot: {}".format(text))
	robot_mouth= pyttsx3.init()
	robot_mouth.say(text)
	robot_mouth.runAndWait()

def get_voice():
	r=sr.Recognizer()
	with sr.Microphone() as mic:
		print("Robot: I'm listening")
		audio=r.listen(mic, phrase_time_limit=5)#nghe giọng người nói trong 5s
		print("Robot:...")
		try: 
			you=r.recognize_google(audio)
			print("You: "+you)
			return you
		except:
			you='...'
			print("You: "+you)
			return 0


def stop():
	speak('See you again')
     #đọc lại đoạn text 'See you again' bằng hàm speak ở trên

def get_text():
	for i in range(3):
		text=get_voice() #text là kết quả của hàm get_voice()
		if text:  #nếu text khác 0 
			return text.lower()
		elif i<2: # trường hợp text=0 thì sẽ cho lặp 3 lần
			speak("Can you speak again, please?") # lặp lại hỏi 3 lần
	time.sleep(2) #tạm dừng 2s
	stop() # dừng luôn chương trình bằng cách chạy hàm stop() ở trên
	return 0

def talk(name):
	day_time=int(strftime('%H')) #gán biến day_time bằng giờ
	if day_time <12:
		speak("Good morning {}. Have a good day!".format(name))
	elif 12<=day_time<18:
		speak("Good afternoon {}. Do you have any plan today?".format(name))
	else: speak("Good everning {}. Do you have dinner?".format(name))

def get_time(text):
	now=datetime.now()
	if 'time' in text:
		speak(str(now.strftime("%H:%M:%S")))
	elif 'today' in text:
		today=date.today()
		speak(str(today.strftime("%B %d, %Y")))
	else:
		speak("Sorry, I can't understand. Please try again.")


def open_application(text):
	if 'google' in text:
		speak('Open Google Chrome')
		os.startfile(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
	elif 'word' in text:
		speak('Open Microsoft Word')
		os.startfile(r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE')
	elif 'excel' in text:
		speak('Open Microsoft Excel')
		os.startfile(r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE')
	elif 'edge' in text:
		speak('Open Microsoft Edge')
		os.startfile(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
	elif 'geometry' in text:
		speak('Open Geometry Sketchpad')
		os.startfile(r'D:\Math\TOÁN\Chuyên đề toán\Hình học\GSP 5.0.exe')
	elif 'combinatorics' in text:
		speak('Open combinatorics document')
		os.startfile(r'D:\Math\TOÁN\Chuyên đề toán\Tổ hợp')
	else:
		speak('This app has not been installed')

def open_website(text):
	reg_ex=re.search('open (.+)', text) # sử dụng phương thức search trong thư viện re
	speak('Ok!')
	if reg_ex:
		domain =reg_ex.group(1)
		url='https:///www.'+domain
		webbrowser.open(url)
		speak('The website you suggest has just been accessed.')
		return True
	else: return False

def open_google_and_search(text):
	search_for=text.split("find", 1)[1]
	speak('Ok!')
	driver=webdriver.Chrome(path) #hàm webdriver.Chrome(path) trong thư viện selenium để vào ứng dụng gg Chrome
	driver.get("http://www.google.com") #mở trình duyệt google.com
	query=driver.find_element_by_xpath("//input[@name='q']")#lấy query, truy vấn
	query.send_keys(str(search_for))
	query.send_keys(Keys.RETURN)

#Mở nhạc 
def play_youtube():
	speak("Please choose the song")
	my_song=get_text()
	while True:
		result=YoutubeSearch(my_song, max_results=10).to_dict()  #đưa vào 1 dict
		if result:
			break #Khi nào tìm thấy được thì kết thúc vòng lặp ko cần tìm tiếp nữa
	url='http://www.youtube.com'+result[0]['url_suffix']#lấy ra phần tử đầu tiên của dict trên
	webbrowser.open(url)
	speak('Your song has been opened')

#Mở dự báo thời tiết
def weather():
	speak("Which location do you want to know about its weather condition?")
	ow_url="http://api.openweathermap.org/data/2.5/weather?"
	city=get_text()
	if not city:
		pass
	api_key="fe8d8c65cf345889139d8e545f57819a"
	call_url = ow_url + "appid=" + api_key + "&q=" + city+ "&units=metric"
	response = requests.get(call_url) #truy cập vào link call_url thông qua thư viện requests
	data=response.json()#lấy các thông tin tiêu đề + số liệu tương ứng của link call_url và đưa 1 vào dict
	if data['cod']!='404': #lấy value của dic data['cod'] với key là 'cod' kiểm tra xem có khác '404' hay không? nếu ko có thì nghĩa là thành phố muốn tìm kiếm đã đc truy vấn thành công
		city_res=data['main']
		current_temperature=city_res['temp']
		current_pressure=city_res['pressure']
		current_humidity=city_res['humidity']
		suntime=data['sys']
		sunrise=datetime.fromtimestamp(suntime['sunrise'])
		sunset=datetime.fromtimestamp(suntime['sunset'])
		wthr=data['weather']
		weather_description=wthr[0]["description"]
		now=datetime.now()
		content = """
        Today is {day} {month} {year}
        The sun rises on {hourrise} hours {minrise} minutes
        The sun sets in {hourset} hours {minset} minutes
        The average temperature is {temp} degrees Celsius
        Air pressure is {pressure} hectare Pascal
        Humidity is {humidity}%
        The sky is clear today. Scattered rain is forecast in some places.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute, 
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
		speak(content)
		time.sleep(20)
	else: speak("Sorry, I can't find that location.")

#Thay đổi hình nền máy tính
def change_background():
	api_key='RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
	url='https://api.unsplash.com/photos/random?client_id=' + api_key #web lấy ảnh (unsplash)
	try:
		with urllib2.urlopen(url) as f:#dùng phương thức urlopen của module urllib2 để mở đường dẫn url ở trên
			json_string=f.read() # đây đang là 1 tệp đối tượng của json => nên cần phải chuyển về python
			#câu lệnh with sẽ giúp đóng file f luôn sau khi đọc file mà ko cần đến phương thức close()
		parsed_json=json.loads(json_string) # chuyển từ json-> python, và sẽ trả về 1 dict lớn (có thể chứa nhiều dict nhỏ bên trong) và sẽ chứa nhiều key
		photo=parsed_json['urls']['full']# lấy ra value của key kép urls-full do đây là 1 dict

		urllib2.urlretrieve(photo, r"C:\Users\dungc\Downloads\image.png") #tải file ảnh về thư mục Downloads và đặt tên là image.png
		image=os.path.join(r"C:\Users\dungc\Downloads\image.png") # đọc image đó ra từ ổ cứng
		ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
		speak("The computer background has just been changed")
		time.sleep(2)
	except:
		speak("Sorry, I can't do it.")

#Đọc báo hôm nay
def read_newspaper():
	speak("Which newspaper's topic do you want?")
	queue=get_text()
	speak('Ok!')
	params={
	    'apiKey':'30d02d187f7140faacf9ccd27a1441ad', 'q':queue
	}
	api_result=requests.get('http://newsapi.org/v2/top-headlines?', params)
	api_response=api_result.json()
	print("News")
	for number, result in enumerate(api_response['articles'], start=1):#dùng kiểu dữ liệu enumerate để sắp xếp có thứ tự và bắt đầu đánh số từ số 1
		print(f"""News {number}:\nHeading: {result['title']}\nQuote: {result['description']}\nLink: {result['url']}
    """)
		if number<=3:
			webbrowser.open(result['url'])
		else: 
			break
	speak("The information you are interested in has been displayed.")
	time.sleep(5)
#Tra wikipedia
def absorb_knowledge():
	try:
		speak("Which definition do you want to know?")
		infor=get_text()
		content=wikipedia.summary(infor).split('\n') #thông tin về infor sẽ ở kiểu list với các phần tử kiểu string
		speak(content[0])# cho robot đọc thông tin cơ bản nhất của content(với kiểu dữ liệu là list)
		time.sleep(15)
		for i in content[1:]:
			speak("Do you want to hear more?")
			rep=get_text()
			if 'no' in rep:
				break
			else: speak(content)
			time.sleep(15)
		speak("Thank you.")
	except:
		speak("Sorry, I can't hear you.")



def call_sen():
	speak("Hello! What's your name?")
	name=get_text()
	time.sleep(3)
	if name:
		speak('Hello {}'.format(name))
		time.sleep(3)
		speak('What can I help you?')
		while True:
			text=get_text()
			if not text:
				break
			elif 'talk' in text or 'talking' in text:
				talk(name)
			elif 'bye' in text or 'stop' in text:
				stop()
				break
			elif 'open' in text:
				if 'open google and search' in text:
					open_google_and_search(text)
				else:
					open_website(text)
			elif 'time' in text or 'day' in text:
				get_time(text)
			elif 'song' in text:
				play_youtube()
			elif 'weather' in text:
				weather()
			elif 'wallpaper' in text:
				change_background()
			elif 'news' in text:
				read_newspaper()
			elif 'knowledge' in text:
				absorb_knowledge() 

call_sen()





