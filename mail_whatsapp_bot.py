from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import smtplib

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--enable-local-storage")  # Ensuring local storage is enabled

# Specify the path to the ChromeDriver executable
service = Service(executable_path="C:\\Users\\i_sar\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the login page
driver.get('https://eazeplace.com/login')

# Wait for the login fields to be present and fill them in
username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))

username_field.send_keys('ravihalbharat@gmail.com')
password_field.send_keys('ravihalbharat')

# Submit the form
login_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sign-in-btn')))
login_button.click()

# Wait for the login process to complete
WebDriverWait(driver, 15).until(EC.url_changes('https://eazeplace.com/login'))

# Navigate to the desired URL after login
driver.get('https://eazeplace.com/eazeuvtovf')

# Wait for the parent div to be present
wait = WebDriverWait(driver, 30)
parent_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cardwrap')))



email ="EazePlaceSupp22@gmail.com"

# Find the third div with class 'literator'
div_elements = parent_div.find_elements(By.CLASS_NAME, 'literator')
# Check if there are at least 3 div elements with class 'literator'
emails={"Archit":"architkush1000@gmail.com"}
for i in range(int(len(div_elements)/8)):
    if div_elements[8*i+3].text== "No link":
        emails[div_elements[8*i+1].text]=div_elements[8*i+2].text
# Example of interacting with local storage

password="byao wybx mihv slmu"

connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
connection.starttls()
connection.login(user=email,password=password)
def message(name):
    message_=f"Subject: Complete Your Sign-Up Details \n\n Dear {name},\nWe noticed that you haven't completed your sign-up details yet. To take advantage of the exciting opportunities we have, please complete your profile as soon as possible. New opportunities are added every day, and one of them could be just right for you!\nThank you for your attention to this matter. We look forward to seeing your completed profile and helping you find the perfect opportunity.\n\nBest regards,\nSupport team ,\nEazeplace"
    msg_clean = ''.join(char if ord(char) < 128 else ' ' for char in message_)
    
    return msg_clean
for key in emails:
    connection.sendmail(from_addr=email,to_addrs=emails[key],msg=message(key).encode('utf-8'))
connection.quit()

# Close the browser
driver.quit()

