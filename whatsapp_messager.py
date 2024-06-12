import pywhatkit as kit
import schedule
import time

# Function to send the WhatsApp message
def send_message():
    phone_number = "<recipient_phone_number>"  # Replace with the recipient's phone number in the format "+1234567890"
    message = "Hello! This is your automated message."
    kit.sendwhatmsg_instantly(phone_number, message, wait_time=20, tab_close=True, close_time=3)

# Schedule the send_message function to run every 12 hours
schedule.every(12).hours.do(send_message)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
