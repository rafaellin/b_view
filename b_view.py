

init_sleep_sec=8
play_time_sec=60
_round=1000  # 0 for unlimited

db_file = "./view.db"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import random
import sqlite3
from sqlite3 import Error
import sys


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

url_list = []
url_file_name = sys.argv[1]
with open(url_file_name) as f:
    url_list = [line.rstrip() for line in f]

print(url_list)
print(len(url_list))


random.shuffle(url_list)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--mute-audio")

conn = create_connection(db_file)

def insert_record(url):
  try:
    sql = ''' INSERT INTO view(url, time) VALUES(?,?) '''
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    cur = conn.cursor()
    cur.execute(sql, (url, dt_string))
    conn.commit()
  except Error as e:
    print(e)


def view_url(url):
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  time.sleep(init_sleep_sec)
  try:
    elem = driver.find_element_by_css_selector(".bilibili-player-dm-tip-wrap")
    elem.click()
  except:
    print("Play error.")
    driver.close()
    return
  time.sleep(play_time_sec)
  driver.close()
  insert_record(url)

if _round == 0:
  while True:
    for u in url_list:
      try:
        view_url(u)
      except Exception as e:
        print(e)
else:
  for i in range(_round):
    for u in url_list:
      try:
        view_url(u)
      except Exception as e:
        print(e)


