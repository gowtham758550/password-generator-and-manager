#Password Generator and Manager version 0.0.4.1

# Copyright (c) Gowtham 2019-2020
# Copyright (C) 2018-2020 M.Anish <aneesh25861@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#import required modules
import os
import secrets
import re
import string
import getpass
import sys
import platform
import urllib.request
import binascii
import hashlib
import time

#check internet connection
def check_connection():
	try:
		urllib.request.urlopen("https://google.com")
	except:
		print("You have no active internet connection\n\n")
		x = input("press enter to exit")
		exit(1)

#import pypi modules
#check the modules are already installed
try:
	import pyAesCrypt
#exception arises if modules are not installed
except ImportError:
 print("\nRequired modules are not found. Wait a minute for installation.\n")
 check_connection()
	#install the missing modules
 if platform.system().lower()=='windows':
        x=os.system('py -m pip install pyAesCrypt')
 else:
       x=os.system('python3 -m pip install pyAesCrypt')
       if (x!=0):
        x=os.system('python -m pip install pyAesCrypt')
 if x!=0:    
       print('\nInstallation Failed!')
       x=input('\nPress any key to continue...')
       exit(1)
 print("Installation completed :)\n")
 print('Restart the program to finish installation!\nPress any key to continue...')
 x=input()
 exit(1)

#buffer size for encryption and decryption
buffer_size = 64*1024
temp_str2 = ""

#anime the print to make attention for some alert message
def anime(msg):
	for char in msg:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(.25)
		
		
#function to create master password
def create_master_password():
	while(True):
		while(True):
			password1 = getpass.getpass("\n\nCreate your master password\n Enter password : ")
			if len(password1) > 7:
				break
			else:
				print("\n\nWarning!!!!!!!!!!!!!!")
				print("Master password requires minimum 8 characters")
				x = input("\n\nPress enter to create again")
		password2 = getpass.getpass("\nConfirm password : ")
		if password1 == password2:
			hash_password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
			#open the file to store new master password
			with open("mp.txt", "a") as file:
				file.write(hash_password)
			file.close()
			break
		else:
			print("\n\nWarning!!!!!!!!!!!!!!!")
			print("Passwords are not matching (ᗒᗣᗕ)՞")
			x = input("\n\nPress enter to create again")



#function to hash	
def hash_msg(str):
	return hashlib.sha256(str.encode('utf-8')).hexdigest()	 			   
			
			
#Function to fetch the key for decryption
def get_key():
	#temporary string variable to get a key
	temp_str1 = ""
	#opens the key text file as key_file
	with open("key.txt", "r") as key_file:
		for i in key_file:
			#concatenate everything in the key file to the temp_str1
			temp_str1 += i
	key_file.close()
	#returns the key
	return str(temp_str1)


#function to encrypt the file
def encrypt_file(file, key):
	#open the file has password to encrypt
	with open(file, "rb") as FileIn:
		#file encrypted into .aes format
		with open(file + ".aes", "wb") as FileOut:
			pyAesCrypt.encryptStream(FileIn, FileOut, key,buffer_size)
		#close the encrypted file
		FileOut.close()
	#close the text file
	FileIn.close()
	#delete the text file after encryption
	os.remove(file)
						
					
#function to decrypt the file	
def decrypt_file(file,key):
	#get encrypted file size
	mp_file_size = os.stat(file).st_size
	#decrypt the file and create the temp text file
	with open(file, "rb") as FileIn:
		with open("temp.txt", "wb") as FileOut:
			#create the original file with key, buffer size and encryoted file size
			pyAesCrypt.decryptStream(FileIn, FileOut, key, buffer_size, mp_file_size)
		#close temp text file
		FileOut.close()
	#close the encrypted file
	FileIn.close()
	

#function to generate password
def generate_password(no):
	#stores alphabets in uppercase and lower case, digits and punctuations(symbols)
	str = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
	global password
	password = ''
	#loop to get random password
	for i in range(no):
		#secrets.choice(str) get the random characters from the variable str
		password += secrets.choice(str)
		
	

#fetch master password
def fetch_master_password():
	with open("temp.txt", "r") as file:
		#temporary variable to store master password fetched from the text file
		global temp_str2
		for i in file:
			temp_str2 += i
	file.close()
	os.remove("temp.txt")
	return temp_str2
	
	

#clear screen
def clear_screen():
	x = input("\n\nPress enter to continue")
	os.system('clear' if os.name == 'posix' else 'cls')
									



while(True):
	print("GENERATE AND MANAGE".center(os.get_terminal_size().columns))
	print(" _____       ___   _____   _____   _          __  _____   _____    _____  ")
	print("|  _  \     /   | /  ___/ /  ___/ | |        / / /  _  \ |  _  \  |  _  \ ")
	print("| |_| |    / /| | | |___  | |___  | |  __   / /  | | | | | |_| |  | | | | ")
	print("|  ___/   / / | | \___  \ \___  \ | | /  | / /   | | | | |  _  /  | | | | ")
	print("| |      / /  | |  ___| |  ___| | | |/   |/ /    | |_| | | | \ \  | |_| | ")
	print("|_|     /_/   |_| /_____/ /_____/ |___/|___/     \_____/ |_|  \_\ |_____/ ")
	
	
	if os.path.isfile("mp.txt.aes"):
		master_password = getpass.getpass("\n\nEnter your password : ")
		hash = hash_msg(master_password)
		#get_key function returns the key for decryption
		key = get_key()
		#call decrypt_file() function 
		decrypt_file("mp.txt.aes",key)
		#call the function to read password from temp file
		fetch_master_password()
		#then check the password is right or wrong
		if temp_str2 == hash:
			while(True):
				print("\n\n1. Generate password\n2. Fetch Password\n3. Exit\n\n")
				choice = input("Enter your choice(1,2,3) : ")
				#Generate password
				if choice == '1':
					print("\n\n*note : website name is important and you can fetch the password with website name only")
					#ask user input for website name
					website_name = input("\n\nEnter website name : ").lower()
					#ask no of characters to generate password
					while(True):
						try:
							character = int(input("\n\nEnter no of characters for your password : "))
							break
						except:
							print("\n\nNo of character must be a numerical value ಠ_ಠ")
							clear_screen()
							
					generate_password(character)
					#now we need to store the generated password for later use
					#check if u already created a encrypted file
					if os.path.isfile('secret.txt.aes'):

						decrypt_file('secret.txt.aes',key)
						#save the password in a file
						with open("temp.txt", "a") as file:
							#write both website name and password in the text file
							file.write(website_name+ password + "\n")
						file.close()
						os.rename("temp.txt", "secret.txt")
						encrypt_file("secret.txt", key)
					else:
						with open("secret.txt","a") as file:
							file.write(website_name+password+"\n")
						file.close()
						
						#call the function to encrypt the file
						encrypt_file("secret.txt",key)
					print("\n\nPassword generated : ",end = '')
					anime(password)
					clear_screen()
				
				#Fetch password	
				elif choice == '2':
					website_name = input("\n\nEnter website name to fetch password : ").lower()
					if os.path.isfile("secret.txt.aes"):
						#call the function to decrypt the file containing passwords
						decrypt_file("secret.txt.aes",key)
						#create a variable to store the password that we are going to fetch from the file
						temp_str3 = ""
						#now the temp file is created
						with open("temp.txt", "r") as file:
							#check line by line
							for line in file.readlines():
								#match the pattern that we stored in the file
								if re.search(rf"{website_name}*", line, re.I):
									#if the pattern matches then we strip the website name and store the password
									temp_str3 = line.strip(website_name)
						file.close()
						os.remove("temp.txt")
						if len(temp_str3) == 0:
							print("\n\nNo passwords created for this website")
							clear_screen()
						else:
							print("\n\nFetched passwords : ",end = '')
							anime(temp_str3)
							clear_screen()
					else:
						print("\n\nNo passwords are created yet (ᗒᗣᗕ)")
						clear_screen()
						
					
		
				
				#Exit 
				elif choice == '3':
					exit(1)
					
				#any other choices
				else:
					print("\n\nEnter correct choice ಠ_ಠ ")
					clear_screen()
		
		#incorrect password					
		else:
			print("\n\n*****Incorrect password*****")
			break
		
	#file not found
	#if there is no file named mp.txt.aes 
	#it was the first time you run this program
	#so create master password	
	else:
		#function call to create a master password
		create_master_password()
		#generate a key for encryption and decryption
		key = binascii.b2a_hex(os.urandom(100))
		#write the key in a text file for later use
		with open("key.txt", "ab") as file:
			#write the key into the file
			file.write(key)
		#close the file
		file.close()
		#now encrypt the master password file
		encrypt_file("mp.txt", key.decode())
		print("\n\nMaster password is created succesfully (•̀ᴗ•́)")
		clear_screen()
		
		
