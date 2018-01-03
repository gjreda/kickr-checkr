from configparser import ConfigParser
from bs4 import BeautifulSoup
import requests
import smtplib

BASE_URL = 'https://www.wahoofitness.com/devices/bike-trainers/wahoo-kickr-powertrainer'

config = ConfigParser()
config.read('config.cfg')

def send_text(toaddr, msg):
    fromaddr = "Kickr Checkr"
    msg = ("From: {0}\r\nTo: {1}\r\n\r\n{2}").format(fromaddr, toaddr, msg)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(config['default']['email_address'], config['default']['email_password'])
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()


response = requests.get(BASE_URL)

try:
    response.raise_for_status()
except HTTPError:
    print('request returned {}: {}'.format(response.status_code, response.url))
    sys.exit(1)

soup = BeautifulSoup(response.text, 'html.parser')
in_stock = soup.find('div', class_='add-to-cart')

if in_stock:
    send_text(config['default']['phone_number'], "Wahoo Kickr's back in stock!")