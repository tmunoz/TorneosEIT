from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re
import json
import time
import sys

# lang: 1: C
# 		2: JAVA
# 		3: C++
# 		4: PASCAL
# 		5: C++11
# 		6: Python 3.5.1

#se puede mejorar el codigo analisando las respuestas que envia la pagina, de momento es solo un scrapper.

chrome_options = Options()  
chrome_options.add_argument("--headless")  #Silent mode

driver = webdriver.Chrome(ChromeDriverManager().install())#path of the browser,

def login_in(user,pwd): # 2 string
	
	driver.get('https://onlinejudge.org/index.php?option=com_comprofiler&task=login')

	input_user_field = driver.find_element_by_xpath('.//input[@id="mod_login_username"]')
	input_user_field.send_keys(user)

	input_pass_field = driver.find_element_by_xpath('.//input[@id="mod_login_password"]')
	input_pass_field.send_keys(pwd)
	login_buttom = driver.find_element_by_xpath('.//input[@value="Login"]')
	login_buttom.click()
	return True

def submit_answer(id_problem, language, answer, kind): # all string less answer, it can be a text or a file- kind it is the type of the answer
	driver.get('https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=25')

	input_field = driver.find_element_by_xpath('.//input[@name="localid"]')
	input_field.send_keys(id_problem)

	try:
		input_lang_field = driver.find_element_by_xpath('.//input[@name="language"][@value="{}"]'.format(language)) 
		input_lang_field.click()
	except:
		pass
	
	try:
		if kind == '0': #file
			input_field = driver.find_element_by_xpath('.//input[@name="codeupl"]')
			input_field.send_keys(answer) #cuando le paso answer no pasa la direccion del archivo
			
		elif kind == '1': # string 
			input_field = driver.find_element_by_xpath('.//textarea[@name="code"]') #revisar esto
			input_field.send_keys(answer) # deberiamos eliminar esta opcion, puede tener problemas de identacion


		submit_buttom = driver.find_element_by_xpath('.//input[@value="Submit"]')
		submit_buttom.click()
	except:
		pass

	id_submittion=-1#valor default para saber que hubo un error
	status=-1
	time.sleep(10) #tiempo de espera para obtener la respuesta del envio

	message_submit = driver.find_element_by_class_name('message').text  #put an assert here to determine the error
	array_message_search=re.findall("[0-9]+", message_submit)
	if len(array_message_search)==1:
		id_submittion=array_message_search[0]
		status=0
	if  id_submittion == -1: 
		if message_submit[len(message_submit)-2]=="D" or  message_submit[len(message_submit)-2]=="I": #ID
			status=1
		elif  message_submit[len(message_submit)-2]=="t": #exist
			status=2
		elif message_submit[len(message_submit)-3]=="g":  #language
			status=3
		elif message_submit[len(message_submit)-2]=="e": #code
			status=4
	
	response = "%d,%d,%s"%(int(id_submittion), status, message_submit)
	return response

def submit_problem (user, pwd, id_problem, language, answer, kind ): #(str) usuario ,(str) pass, (str) id problema,(str {0-1}) lenguaje, (str {0-1}) tipo de respuesta,({str - file} ) respuesta
	login_in(user, pwd)
	return submit_answer(id_problem, language, answer, kind)

print(submit_problem(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]))

sys.stdout.flush()
driver.close()
