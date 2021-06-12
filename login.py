from selenium import webdriver
import time
from chromedriver_py import binary_path
from read_captcha import decode_captcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants
import argparse
from urllib.request import urlretrieve

arg_parser = argparse.ArgumentParser()
# Add login cred to be passed
arg_parser.add_argument("-u", "--username", required=True, help="Supply username")
arg_parser.add_argument("-p", "--password", required=True, help="Supply password")
args = vars(arg_parser.parse_args())

driver = webdriver.Chrome(executable_path=binary_path)

driver.get(constants.BASE_URL)

try:
    # wait until the page has loaded and then start filling out the elements    
    email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, constants.login_elements["USR_NAME_ID"]))
    )
    email.send_keys(args["username"])
    # filling password   
    passwd = driver.find_element_by_id(constants.login_elements["PASSWD_ID"])
    passwd.send_keys(args["password"])
    # checkbox followed after password    
    checkbox = driver.find_element_by_name(constants.login_elements["CHECKBOX_ID"])
    checkbox.click()
    # read the captcha img as a byte array    
    captcha_img = driver.find_element_by_id(constants.login_elements["CAPTCHA_IMG"])
    src = captcha_img.get_attribute('src')
    # download the image    
    urlretrieve(src, "captcha.png")
    # decode the image array    
    captcha_str, decode_prob = decode_captcha()
    print(f'String decoded from easy ocr is {captcha_str} with a confidence of {decode_prob}')
    captcha_text_box = driver.find_element_by_id(constants.login_elements["CAPTCHA_TXT_BOX"])
    val = input("Enter captcha: ")
    captcha_text_box.send_keys(val)
    # final submission of the page
    submit = driver.find_element_by_id(constants.login_elements["LOGIN_SUBMIT"])
    submit.click()
    print('Successfully logged in!')
    
    # see the logged in page
    time.sleep(10)

    driver.close()
except Exception as e:
    print('Hit an exception: ', e)
    driver.quit()
