import requests
from selenium import webdriver
from pyshadow.main import Shadow
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time 
import urllib.request
from PIL import Image

# #root > div > div > div > div
# initialize the webdriver
driver = webdriver.Chrome()
loginURL = 'https://login.vitalsource.com/?redirect_uri=https%3A%2F%2Fevantage.gilmoreglobal.com%2F%23%2F&brand=evantage.gilmoreglobal.com'
baseUrl = "https://evantage.gilmoreglobal.com"
bookName = 'SN-HRI-Q010-PG-E' 
relativeUrl = "/reader/books/"+bookName+"/pageid/"
delay = 20 # seconds
driver.get(loginURL);
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'username-field')))
    print("Login page is ready!")
except TimeoutException:
    print("Loading login page took too much time!")
username = "surajshankar.pagad@servicenow.com"
password = "Welcome123@"

# find username/email field and send the username itself to the input field
driver.find_element("id", "username-field").send_keys(username)
# find password input field and insert password as well
driver.find_element("id", "password-field").send_keys(password)
button = driver.find_element('id',"submit-btn")
driver.execute_script('arguments[0].scrollIntoView(true);', button)
driver.find_element('id',"signin-form").submit()
time.sleep(10)
# Accept cookie
driver.find_element(By.XPATH,'//*[@id="bookshelf"]/div/div/div[1]/div/button[2]').click()
for i in range(1,230): 
    driver.get(baseUrl+relativeUrl+str(i))
    try:
        print('try')
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[1]/div/div[2]/div')))
        print("Course page is ready!")
        time.sleep(1) 
        frame = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/iframe")))
        driver.switch_to.frame(frame)
        shadowHost = driver.find_element(By.XPATH, "/html/body/mosaic-book")
        shadow_root = driver.execute_script("return arguments[0].shadowRoot;",shadowHost)
        print(shadow_root)
        frame2 = shadow_root.find_element(By.CSS_SELECTOR,'div > div:nth-child(2) > div > div:nth-child(1) > iframe');
        driver.switch_to.frame(frame2)
        img = driver.find_element(By.XPATH,'/html/body/img')
        src = img.get_attribute('src')
        imgURL = src.replace('/800','/2000')
        print(imgURL)
        driver.get(imgURL);
        time.sleep(5);
        driver.save_screenshot(bookName+str(i)+".png")
        im = Image.open(bookName+str(i)+".png") # uses PIL library to open image in memory
        im = im.crop((475, 5, 1080, 850)) # defines crop points
        im.save(bookName+str(i)+".png") # saves new cropped image
    except TimeoutException:
        print("Loading course page took too much time!")
# close the webdriver
driver.quit()


