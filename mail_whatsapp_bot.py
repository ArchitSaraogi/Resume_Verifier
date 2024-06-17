from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver



service = Service(executable_path="C:\\Users\\i_sar\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Use the correct parameter 'executable_path' for specifying the driver executable path

driver.get('https://eazeplace.com/login')

# Find and fill in the login form fields
username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
password_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'password')))

username_field.send_keys('ravihalbharat@gmail.com')
password_field.send_keys('your_password')

# Submit the form
login_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sign-in-btn')))
login_button.click()

# Wait for the login process to complete
# Add necessary waits or conditions here

# Navigate to the desired URL
driver.get('https://eazeplace.com/eazeuvtovf')

# To prevent session timeout
driver.execute_script("window.focus();")
driver.execute_script("window.onfocus=function(){};")


wait = WebDriverWait(driver, 5)

# Find the third div with class 'literator' under the parent div
parent_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'activeinternlist')))
div_elements = parent_div.find_elements_by_class_name('literator')

# Check if there are at least 3 div elements with class 'literator'
if len(div_elements) >= 3:
    third_div_text = div_elements[2].text
    print(third_div_text)
else:
    print("Not enough 'literator' elements found")

# Close the browser
driver.quit()