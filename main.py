#Generate and manage your passwords
#import required modules
import os
import secrets
import re
import string
import getpass
import sys
import subprocess
import platform
import urllib.request


#check internet connection
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
	import binascii
#exception arises if modules are not installed
except ImportError:
	print("Requires modules are not found. Wait a minute for installation.\n")
	#install the missing modules
	#install pyAesCrpt
	subprocess.check_call([sys.executable, "-m", "pip", "install", "pyAesCrypt"])
	#install binascii
	subprocess.check_call([sys.executable, "-m", "pip", "install", "binascii"])
	print("Installation completed :)\n")
	print('Restart the program to finish installation!\nPress any key to continue...')
	x=input()
	exit(1)
		
#buffer size for encryption and decryption
buffer_size = 64*1024
temp_str2 = ""
password = ""

#function to create master password
def create_master_password():
	password1 = getpass.getpass("\n\nCreate your master password\n Enter password : ")
	password2 = getpass.getpass("\nConfirm password : ")
	if password1 == password2:
		#delete the old password file 
		#when you create password for first time this condition will be false and continue
		if os.path.isfile("mp.txt.aes"):
			os.remove("mp.txt.aes")
		#open the file to store new mastee password
		with open("mp.txt", "a") as file:
			file.write(password1)
		file.close()
			
			
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
def generate_password(website,no):
	#stores alphabets in uppercase and lower case, digits and punctuations(symbols)
	str = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
	global password
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
	return temp_str2
	#delete the temp text file
	os.remove("temp.txt")
			
									
print("********************Password-Manager*******************")


while(True):
	if os.path.isfile("mp.txt.aes"):
		master_password = getpass.getpass("\n\nEnter your password : ")
		#get_key function returns the key for decryption
		key = get_key()
		#call decrypt_file() function 
		decrypt_file("mp.txt.aes",key)
		#call the function to read password from temp file
		fetch_master_password()
		#then check the password is right or wrong
		if temp_str2 == master_password:
			while(True):
				print("\n\n1. Generate password\n2. Fetch Password\n3. Exit\n\n")
				choice = input("Enter your choice(1,2,3) : ")
				#Generate password
				if int(choice) == 1 :
					print("\n\n*note : website name is important and you can fetch the password with website name only")
					#ask user input for website name
					website_name = input("\n\nEnter website name : ").lower()
					#ask no of characters to generate password
					character = int(input("\n\nEnter no of characters for your password : "))
					generate_password(website_name,character)
					#now we need to store the generated password for later use
					#save the password in a file
					with open("secret.txt", "a") as file:
						#write both website name and password in the text file
						file.write(website_name + password + "\n")
					file.close()
					#call the function to encrypt the file
					encrypt_file("secret.txt",key)
					print("\n\nPassword generated : ",password)
					x = input("\n\npress enter to continue")
				
				#Fetch password	
				elif int(choice) == 2:
					website_name = input("\n\nEnter website name to fetch password : ").lower()
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
					#delete the file after fetch the password
					os.remove("temp.txt")
					#check if password is fetched or not
					if len(temp_str3) == 0:
						print("\n\nNo passwors you created for this website or You may enter the wrong website name")
					else:
						print("\n\nFetched passwords : ",temp_str3)
					x = input("\n\npress enter to continue")
		
				
				#Exit 
				elif int(choice) == 3:
					exit(1)
					
				#any other choices
				else:
					print("\n\nEnter correct choice")
		
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
		print("\n\nMaster password is created succesfully :)")
