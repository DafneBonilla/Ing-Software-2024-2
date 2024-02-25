import pymysql
import random
from cryptoUtils.CryptoUtils import cipher
from hashlib import sha256

'''
Function to connect to the database
'''
def connect_to_database():
    connection = pymysql.connect(host='localhost',
                                 user='lab',
                                 password='Developer123!',
                                 database='lab_software_eng',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

