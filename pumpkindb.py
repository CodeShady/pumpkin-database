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
			print("Created Database - " + name + "\nWith Password: " + "*" * len(password))
		newDB = open(name + ".pumpkin", "w")
	
	def add(self, key, value):
		currentDB = self.currentDB
		PUMPKIN_PASS = self.PUMPKIN_PASS

		if currentDB == "":
			print("Pumpkin Error! No Pumpkin Selected!")
		else:
			# Write data
			dbFile = open(currentDB + ".pumpkin", "a+")
			key = encrypt(key, PUMPKIN_PASS)
			value = encrypt(value, PUMPKIN_PASS)
			dbFile.write(f'["{str(key)}", "{str(value)}"]\n')

	def fetch(self, key):
		currentDB = self.currentDB

		# Make sure a pumpkin database was selected
		if currentDB == "":
			print("Pumpkin Error! No Pumpkin Selected!")
		else:

			PUMPKIN_PASS = self.PUMPKIN_PASS

			# Open pumpkin file for reading
			dbFile = open(currentDB + ".pumpkin", "r")

			# If the key was "*", then read everything. 
			if key == "*":
				return dbFile.read()
			else:
				
				dbFile = dbFile.readlines()

				# Return List
				returnValue = []

				for line in dbFile:
					# Grab each key from pumpkin file
					lineKey = line[2:][:len(encrypt(key, PUMPKIN_PASS))]
					# Decrypt the key for reading
					lineKey = decrypt(lineKey, PUMPKIN_PASS).decode("utf-8")

					if lineKey == key:
						# Loop over all keys and values
						line = line.strip()
						# Replace all of this trash
						line = line.replace("[", "")
						line = line.replace("]", "")
						line = line.replace(",", "")
						line = line.replace("\"", "")

						line = decrypt(line[len(encrypt(key, PUMPKIN_PASS)) + 1:], PUMPKIN_PASS).decode("utf-8")
						
						# Add the value to a list for later use in the users program.
						returnValue.append(line)
					else:
						print("Didn't match..")

				return returnValue

	def delete(self, key):

		currentDB = self.currentDB

		# Make sure a pumpkin database is selected
		if currentDB == "":
			print("Pumpkin Error! No Pumpkin Selected!")
		else:
			# Open pumpkin file for reading
			dbFile = open(currentDB + ".pumpkin", "r").readlines()

			updatedContents = ""

			for line in dbFile:
				line = line.strip()

				lineKey = line[2:][:len(encrypt(key, self.PUMPKIN_PASS))]

				# print(line)

				# print(decrypt(lineKey, self.PUMPKIN_PASS).decode("utf-8"))

				if decrypt(lineKey, self.PUMPKIN_PASS).decode("utf-8") != key:
					updatedContents += line + "\n"
					
			dbFile = open(currentDB + ".pumpkin", "w")
			dbFile.write(updatedContents)