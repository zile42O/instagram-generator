import requests
import threading
import names
from secrets import randbelow, choice
import random
import time
import json
from termcolor import colored
import colorama

colorama.init()

SMS_API_KEY = "" #sms activate

# generate random password
def gen_ran_passw():
	letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	chars = ["!","?","=","&","$","#"]
	random_password = ""
	oldvalue = ""
	choicelist = [0,1,2]
	for x in range(14):
		if oldvalue:
			choicelist.remove(oldvalue)
			value = choice(choicelist)
			choicelist.append(oldvalue)
		else:
			value = randbelow(3)
		if value == 0:
			if randbelow(2) == 0:
				random_password += letters[randbelow(len(letters))].upper()
			else:
				random_password += letters[randbelow(len(letters))]
		elif value == 1:
			random_password += chars[randbelow(len(chars))]
		elif value == 2:
			random_password += str(randbelow(10))
		oldvalue = value
	
	random_password += letters[randbelow(len(letters))].upper() + letters[randbelow(len(letters))]
	random_password += chars[randbelow(len(chars))] + str(randbelow(10))

	return random_password

# generates random client id
def gen_client_id():
	letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	ran4letters = ""
	for _ in range(4):
		if random.randint(0,1) == 0:
			ran4letters += letters[random.randrange(0,len(letters))]
		else:
			ran4letters += letters[random.randrange(0,len(letters))].upper()
	ran15chars = ""
	for _ in range(15):
		if random.randint(0,1) == 0:
			if random.randint(0,1) == 0:
				ran15chars += letters[random.randrange(0,len(letters))]
			else:
				ran15chars += letters[random.randrange(0,len(letters))].upper()
		else:
			ran15chars += str(random.randint(0,9))

	client_id = f'Yf{ran4letters}ALAAG{letters[random.randrange(0,len(letters))].upper() + ran15chars}'
	return client_id

# setup login headers
def setup_login_headers(csrf, claim):
	headers = {
		'accept': '*/*',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'q=0.9,en-US;q=0.8,en;q=0.7',
		'content-length': '0',
		'content-type': 'application/x-www-form-urlencoded',
		'origin': 'https://www.instagram.com',
		'referer': 'https://www.instagram.com/',
		'sec-ch-ua':'" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
		'x-asbd-id': '198387',
		'x-csrftoken': csrf,
		'x-ig-app-id': '936619743392459',
		'x-ig-www-claim': claim,
		'x-instagram-ajax': 'cc6f59f85f33',
		'x-requested-with': 'XMLHttpRequest'
	}
	return headers

# main function
def instagram_generate(thread_id, smsapi=None, country_code=None):

	PROXY_HOST = ''
	PROXY_PORT = 40000
	PROXY_USER = ''
	PROXY_PASS = ''
	
	proxy_rotate = {
		"http": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}",
		"https": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
	}
	s = requests.Session()
	try:		
		s.proxies = proxy_rotate
	except ValueError as err:
		print(err)
		return
		
	while True:
		try:
			headers = {
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				'accept-encoding': 'gzip, deflate, br',
				'accept-language': 'en-US,en;q=0.9',
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
				'sec-ch-ua-mobile': '?0',
				'sec-ch-ua-platform': '"Windows"',
				'sec-fetch-dest': 'document',
				'sec-fetch-mode': 'navigate',
				'sec-fetch-site': 'none',
				'sec-fetch-user': '?1',
				'upgrade-insecure-requests': '1',
				'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
			}
			res = s.get('https://www.instagram.com/data/shared_data/', headers=headers)
			device_id = res.text.split('"device_id":"')[1].split('"')[0]
			csrf = res.text.split('csrf_token":"')[1].split('"')[0]
			break
		except:			
			s = requests.Session()
			try:
				s.proxies = proxy_rotate
			except ValueError as err:
				print(err)
				return
			time.sleep(2)

	time.sleep(0.2)

	password = gen_ran_passw() 
	client_id = gen_client_id()
	name = names.get_full_name()
	month = str(random.randint(1,12))
	day = str(random.randint(10,25))
	year = str(random.randint(1960,2000))
	username = name.split()[0] + str(random.randint(111,999)) + '_' + name.split()[1]
	
	headers = {
		'accept': '*/*',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9',
		'content-type': 'application/x-www-form-urlencoded',
		'origin': 'https://www.instagram.com',
		'referer': 'https://www.instagram.com/accounts/emailsignup',
		'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
		'x-asbd-id': '198387',
		'x-csrftoken': csrf,
		'x-ig-app-id': '936619743392459',
		'x-ig-www-claim': '0',
		'x-instagram-ajax': 'c35f58698901',
		'x-requested-with': 'XMLHttpRequest',
		'x-web-device-id': device_id
	}

	for x in range(3):
		res = s.get(f'https://sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=getNumber&service=ig&country={country_to_phone[country_code]}')
		try:
			phonenum = res.text.split(':')[2]
			phone_id = res.text.split(':')[1]
		except:
			print(colored(f"Process [{thread_id}] - Account can't find number for usage", "red"))
			return

		while True:
			body = {
				'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
				'phone_number': phonenum,
				'client_id': client_id,
				'username': username,
				'first_name': name,
				'stopDeletionNonce': '',
				'trustedDeviceRecords': '{}',
				'queryParams': '{}',
				'seamless_login_enabled': '1',
                'opt_into_one_tap': 'false'
			}
			res = s.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', headers=headers, data=body)
			if res.json().get("spam", False) == True:
				print(colored(f"Process [{thread_id}] - Account creation failed SPAM detected", "red"))
				return			
			try:
				if not res.json()["status"]:
					print(colored(f"Process [{thread_id}] - Account creation failed code: 1", "red"))
					return
			except:
				print(colored(f"Process [{thread_id}] - Account creation failed code: 2", "red"))
				return
			if "errors" in res.json() and "username" in res.json()["errors"]:
				print(colored(f"Process [{thread_id}] - Username is taken, choosing new one", "red"))
				username = res.json()["username_suggestions"][0]
			break
		time.sleep(1)

		body = {          
			'client_id': client_id,
			'phone_number': phonenum,
			"phone_id": phone_id,	
			"big_blue_token": ""
		} 
		res = s.post('https://www.instagram.com/accounts/send_signup_sms_code_ajax/', headers=headers, data=body)
		if res.json().get("sms_sent", True) == False:
			print(colored(f"Process [{thread_id}] - Account sms is not sent to instagram", "red"))
			return
		else:
			if res.json()['status'] == 'fail':
				print(colored(f"Process [{thread_id}] - Account can't send SMS because rate limited captcha", "red"))
				return
		print(colored(f"Process [{thread_id}] - Account waiting for sms code", "yellow"))

		sms_code = False
		while True:
			url = f'https://api.sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=getStatus&id={phone_id}'					
			try:
				res = requests.get(url)	
				status = res.text
				
				if status == "STATUS_WAIT_CODE":
					time.sleep(3)
				else:
					try:
						sms_code = res.text.split(':')[1]
						print(colored(f"Process [{thread_id}] - Account received sms code", "green"))
						break
					except:						
						print(colored(f"Process [{thread_id}] - Account getting sms code status is not good, status: {status}", "red"))
						break
			except Exception as e:
				time.sleep(3)
				break

		if sms_code:
			res = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=setStatus&status=6&id={phone_id}')
			body = {
				'client_id': client_id,
				'phone_number': phonenum,
				'sms_code': sms_code
			}
			res = s.post('https://www.instagram.com/accounts/validate_signup_sms_code_ajax/', headers=headers, data=body)
			print(colored(f"Process [{thread_id}] - Account activated sms code", "green"))
			break
		
		else:		
			requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=setStatus&status=8&id={phone_id}')
			time.sleep(1)
			return

	body = {
		'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
		'phone_number': phonenum,
		'client_id': client_id,
		'username': username,
		'first_name': name,
		'sms_code': sms_code,
		'seamless_login_enabled': '1'
	}
	res = s.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', headers=headers, data=body)
	time.sleep(0.5)

	body["month"] = month
	body["day"] = day
	body["year"] = year
	body["tos_version"] = 'eu'
	res = s.post('https://www.instagram.com/accounts/web_create_ajax/', headers=headers, data=body)
	if res.status_code == 200:
		print(colored(f"Process [{thread_id}] - Account creation success", "green"))
	else:
		print(colored(f"Process [{thread_id}] - Account creation failed", "red"))
		return

	time.sleep(15) # waiting for clipping

	for retries in range(3):
		res = s.get('https://www.instagram.com/accounts/login/')
		csrf = res.text.split('csrf_token":"')[1].split('"')[0]
		insta_claim = "0"
		payload = {
			'username': username,
			'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
			'optIntoOneTap': 'false'
		}

		headers = setup_login_headers(csrf, insta_claim)
		res = s.post('https://www.instagram.com/accounts/login/ajax/', headers=headers, data=payload)
		try:
			if res.json()["authenticated"]:
				print(colored(f"Process [{thread_id}] - Account is logged in", "green"))
				with open('results.txt', 'a') as acc_file:
					acc_file.write(f'{username}:{password}\n')
					print(colored(f"Process [{thread_id}] - Account is saved", "green"))
				break
			else:
				#login failed
				if retries < 2:
					s = requests.Session()
					try:
						s.proxies = proxy_rotate
					except ValueError as err:
						print(err)
						return
					time.sleep(15)
				else:
					print(colored(f"Process [{thread_id}] - Account saving failed, could't login", "red"))
					return				

		except Exception as e:
			if retries < 2:				
				s = requests.Session()
				try:
					s.proxies = proxy_rotate
				except ValueError as err:
					print(err)
					return
				time.sleep(15)
			else:
				print(colored(f"Process [{thread_id}] - Account auth failed, could't login", "red"))
				return

print(colored("Instagram Account Generator", "cyan"))
print(colored("Author: ", "cyan") + "Zile42O")
print("\n\n")

# currently supported countries
# to add more please check on sms-activate org

country_to_phone = {
	"DE": "43",		# Germany
	"IT": "86",		# Italy
	"ES": "56",		# Spain
	"RU": "0",		# Russia
	"CA": "36",		# Canada
	"MN": "171",	# Montenegro
	"RS": "29"		# Serbia
}

print(colored("How much accounts you need?", "cyan"))
ts = int(input('=> '))

threadlist = []
for i in range(ts):
	t = threading.Thread(target=lambda h=i:instagram_generate(h, smsapi=SMS_API_KEY, country_code="DE"))
	threadlist.append(t)
	t.start()
	time.sleep(0.3)

# wait till all tasks finished
for thread in threadlist:
	thread.join()

input(colored("Generator is finished. Press enter to exit...", "cyan"))

colorama.deinit()