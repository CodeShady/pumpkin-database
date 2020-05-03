import os
import sys
import time


"""
                  ___
               ___)__|_
          .-*'          '*-,
         /      /|   |\     \   	Pumpkin DB
        ;      /_|   |_\     ;      By: CodeShady
        ;   |\           /|  ;
        ;   | ''--...--'' |  ;
         \  ''---.....--''  /
          ''*-.,_______,.-*' 
"""



# # ENCRYPTION AND DECRYPTION
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return bytes.decode(base64.b64encode(iv + cipher.encrypt(raw))) 
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))



class PumpkinDB:
	# Variables

	# SWITCH THIS TO TRUE FOR LOGS
	logsEnabled = False
	
	# Other Variables I wouldn't mess with.
	currentDB = ""
	PUMPKIN_PASS = ""
	

	def use(self, database, password):
		self.currentDB = database
		PUMPKIN_PASS = self.PUMPKIN_PASS
		logsEnabled = self.logsEnabled

		if logsEnabled:
			print("Switched To - " + database)
		# print("YOU ARE USING: " + database)

	def create(self, name, password):
		logsEnabled = self.logsEnabled
		if logsEnabled:
			print("[!] Created Database - " + name + "\nWith Password: " + "*" * len(password))
		newDB = open(name + ".pumpkin", "w")
	
	def add(self, key, value):
		currentDB = self.currentDB
		PUMPKIN_PASS = self.PUMPKIN_PASS

		if currentDB == "":
			print("Pumpkin Error! - No Pumpkin Selected!")
			sys.exit(0)
		else:
			# Write data
			dbFile = open(currentDB + ".pumpkin", "a+")
			data_key = encrypt(key, PUMPKIN_PASS)
			data_value = encrypt(value, PUMPKIN_PASS)
			data_timestamp = encrypt(str(time.time()), PUMPKIN_PASS)
			data_hash = encrypt(hashlib.sha256(bytes(str(data_key) + str(data_value) + str(data_timestamp), "utf-8")).hexdigest(), PUMPKIN_PASS)
			dbFile.write(f'{str(data_key)}|{str(data_value)}|{data_timestamp}|{str(data_hash)}\n')
			# dbFile.write(f'["{str(key)}", "{str(value)}"]\n')

	def fetchall(self, data_row):

		currentDB = self.currentDB
		PUMPKIN_PASS = self.PUMPKIN_PASS

		if data_row == "":
			print("Pumpkin Error! - Return Data Value (Only Paramater In .fetchall()) must be ether - 'key', 'value', 'timestamp', 'hash', or '*'!")

		else:
			dbFile = open(currentDB + ".pumpkin", "r")

			returnDataList = []

			for line in dbFile.readlines():
				dataList = []

				# Split the line into a list
				lineData = list(line.split("|"))

				for data in lineData:
					dataList.append(decrypt(data, PUMPKIN_PASS).decode("utf-8"))

				if data_row == "*":
					returnDataList.append(dataList)
				elif data_row == "key":
					returnDataList.append(dataList[0])
				elif data_row == "value":
					returnDataList.append(dataList[1])
				elif data_row == "timestamp":
					returnDataList.append(dataList[2])
				elif data_row == "hash":
					returnDataList.append(dataList[3])

			return returnDataList


	def fetch(self, key, data_row):
		currentDB = self.currentDB
		PUMPKIN_PASS = self.PUMPKIN_PASS

		# Make sure a pumpkin database was selected
		if currentDB == "":
			print("Pumpkin Error! - No Pumpkin Selected!")
			sys.exit(0)
		elif data_row == "":
			print("Pumpkin Error! - No Row Specified!")
			sys.exit(0)
		elif data_row != "key" and data_row != "value" and data_row != "timestamp" and data_row != "hash" and data_row != "*":
			print("Pumpkin Error! - Return Data Value (3rd Paramater In .fetch()) must be ether - 'key', 'value', 'timestamp', 'hash', or '*'!")
			sys.exit(0)
		else:

			# Open pumpkin file for reading
			dbFile = open(currentDB + ".pumpkin", "r")

			
			dbFile = dbFile.readlines()

			# Return List
			returnValue = []

			for line in dbFile:
				# Grab each key from pumpkin file
				lineKey = line[:len(encrypt(key, PUMPKIN_PASS))]
				# Decrypt the key for reading
				lineKey = decrypt(lineKey, PUMPKIN_PASS).decode("utf-8")

				if lineKey == key:
					# Loop over all keys and values
					line = line.strip()

					# Convert line into a list
					lineData = list(line.split("|"))

					# 0 = key
					# 1 = value
					# 2 = timestamp
					# 3 = hash

					# Choose what to send back to the user
					if data_row == "key":
						returnValue.append(decrypt(lineData[0], PUMPKIN_PASS).decode("utf-8"))
					elif data_row == "value":
						returnValue.append(decrypt(lineData[1], PUMPKIN_PASS).decode("utf-8"))
					elif data_row == "timestamp":
						returnValue.append(decrypt(lineData[2], PUMPKIN_PASS).decode("utf-8"))
					elif data_row == "hash":
						returnValue.append(decrypt(lineData[3], PUMPKIN_PASS).decode("utf-8"))
					elif data_row == "*":
						pumpkin_key_data = []
						for item in lineData:
							pumpkin_key_data.append(decrypt(item, PUMPKIN_PASS).decode("utf-8"))
						
						returnValue.append(pumpkin_key_data)


					line = decrypt(line[:len(encrypt(key, PUMPKIN_PASS))], PUMPKIN_PASS).decode("utf-8")
					

			return returnValue

	def delete(self, key):

		currentDB = self.currentDB

		# Make sure a pumpkin database is selected
		if currentDB == "":
			print("Pumpkin Error! No Pumpkin Selected!")
		else:
			# User didn't enter a hash

			if len(key) == 64:
				# User has entered a hash instead of a key name, so find the hash instead... And remove it!!

				# Open pumpkin file for reading
				dbFile = open(currentDB + ".pumpkin", "r").readlines()

				updatedContents = ""

				for line in dbFile:
					line = line.strip()

					lineData = list(line.split("|"))

					lineHash = decrypt(lineData[3], self.PUMPKIN_PASS).decode("utf-8")

					if lineHash != key:
						updatedContents += line + "\n"

				dbFile = open(currentDB + ".pumpkin", "w")
				dbFile.write(updatedContents)

			else:
				# Open pumpkin file for reading
				dbFile = open(currentDB + ".pumpkin", "r").readlines()

				updatedContents = ""

				for line in dbFile:
					line = line.strip()

					lineData = list(line.split("|"))


					lineKey = line[2:][:len(encrypt(key, self.PUMPKIN_PASS))]
					lineName = decrypt(lineData[0], self.PUMPKIN_PASS).decode("utf-8")

					if lineName != key:
						updatedContents += line + "\n"

				dbFile = open(currentDB + ".pumpkin", "w")
				dbFile.write(updatedContents)
