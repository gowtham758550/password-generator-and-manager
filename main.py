#Password Generator and Manager version 1.0

# Copyright (C) Gowtham 2019-2020 <gowtham758550@gmail.com>
# Copyright (C) 2019-2020 M.Anish <aneesh25861@gmail.com>
# Copyright (C) T.Raagul 2019-2020 <raagul26@gmail.com>

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
import string
import getpass
import sys
import platform
import urllib.request
import binascii
import hashlib
import time



#clear screen
def clear_screen():
	x = input("\n\nPress enter to continue")
	os.system('clear' if os.name == 'posix' else 'cls')
	
	
#check internet connection
def check_connection():
	try:
		urllib.request.urlopen("https://google.com")
	except:
		print("You have no active internet connection\n\nIf you get no active internet even when you connected to internet please try to install the module manually\nModule is pyAesCrypt\nSorry for this inconvinience")
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
password = ""
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
			hash = sha256_hash_msg(password1)
			#open the file to store new master password
			with open("mp.txt", "a") as file:
				file.write(hash)
			file.close()
			break
		else:
			print("\n\nWarning!!!!!!!!!!!!!!!")
			print("Passwords are not matching (ᗒᗣᗕ)՞")
			x = input("\n\nPress enter to create again")



#function to hash	
def sha256_hash_msg(str):
	return hashlib.sha256(str.encode('utf-8')).hexdigest()	 	
	
def md5_hash_msg(str):
	return hashlib.md5(str.encode('utf-8')).hexdigest()		   
			
			
#Function to fetch the key for decryption
def get_key():
	#temporary string variable to get a key
	temp_str1 = ""
	#opens the key text file as key_file
	try:
		with open("key.txt", "r") as key_file:
			for i in key_file:
				#concatenate everything in the key file to the temp_str1
				temp_str1 += i
		key_file.close()
	except:
		print("\n\nKey file not found!!!!!!")
		exit(1)
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
	global password
	password = ""
	a1 = string.ascii_uppercase
	a2 = string.ascii_lowercase
	a3 = string.digits
	a4 = string.punctuation
	list = [a1,a2,a3,a4]
	secrets.SystemRandom().shuffle(list)
	q = no//4
	rem = no%4
	for i in range(q):
		password += secrets.choice(list[0])
		password += secrets.choice(list[1])
		password += secrets.choice(list[2])
		password += secrets.choice(list[3])
	if rem == 0:
		print("\n\nPassword generated : ",end = "")
		anime(password)
	else:
		for i in range(rem):
			password += secrets.choice(a1+a2+a3+a4)
		print("\n\nPassword generated : ",end = "")
		anime(password)

#id = 1 for fetch passwords
#id = 2 for check if u already created password for that site				
def check_file(website_name,id):
	password = ""
	with open("temp.txt", "r") as file:
		for line in file.readlines():
			if website_name in line and id == 2:
				password = line.strip(website_name)
			
			elif website_name in line and id == 1:
				return True
				clear_screen()
			
			else:
				pass
	file.close()
				

#fetch master password
def fetch_master_password():
	with open("temp.txt", "r") as file:
		#temporary variable to store master password fetched from the text file
		global temp_str2
		temp_str2 = ""
		for i in file:
			temp_str2 += i
	file.close()
	os.remove("temp.txt")
	return temp_str2
	
	
									
def get_character():
	while(True):
		try:
			global character
			character = int(input("\n\nEnter no of characters for your password : "))
			if character>5:
				break
			else:
				print("\n\nPassword requires minimum 6 charactersʕ•ᴥ•ʔ")
		except:
			print("\n\nNo of character must be a numerical value ಠ_ಠ")


while(True):
	try:
		print("GENERATE AND MANAGE".center(os.get_terminal_size().columns))
	except:
		print("GENERATE AND MANAGE")
	print(" _____       ___   _____   _____   _          __  _____   _____    _____  ")
	print("|  _  \     /   | /  ___/ /  ___/ | |        / / /  _  \ |  _  \  |  _  \ ")
	print("| |_| |    / /| | | |___  | |___  | |  __   / /  | | | | | |_| |  | | | | ")
	print("|  ___/   / / | | \___  \ \___  \ | | /  | / /   | | | | |  _  /  | | | | ")
	print("| |      / /  | |  ___| |  ___| | | |/   |/ /    | |_| | | | \ \  | |_| | ")
	print("|_|     /_/   |_| /_____/ /_____/ |___/|___/     \_____/ |_|  \_\ |_____/ ")
	
	
	if os.path.isfile("mp.txt.aes"):
		master_password = getpass.getpass("\n\nEnter your password : ")
		hash = sha256_hash_msg(master_password)
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
					hash = md5_hash_msg(website_name)
					if os.path.isfile('secret.txt.aes'):
						decrypt_file('secret.txt.aes',key)
						if check_file(hash,1):
							print("\n\nYou already create a password for this website(ᗒᗣᗕ)՞")
							os.remove("temp.txt")
						else:
							get_character()
							generate_password(character)
							#save the password in a file
							with open("temp.txt", "a") as file:
								#write both website name and password in the text file
								file.write(hash+ "\t" + password + "\n")
							file.close()
							os.rename("temp.txt", "secret.txt")
							encrypt_file("secret.txt", key)
					else:
						get_character()
						generate_password(character)
						with open("secret.txt","a") as file:
							file.write(hash+password+"\n")
						file.close()
						
						#call the function to encrypt the file
						encrypt_file("secret.txt",key)
					clear_screen()
				
				#Fetch password	
				elif choice == '2':
					website_name = input("\n\nEnter website name to fetch password : ").lower()
					hash = md5_hash_msg(website_name)
					if os.path.isfile("secret.txt.aes"):
						#call the function to decrypt the file containing passwords
						decrypt_file("secret.txt.aes",key)
						check_file(hash,2)
						os.remove("temp.txt")
						if len(password) == 0:
							print("\n\nNo passwords created for this website")
							clear_screen()
						else:
							print("\n\nFetched passwords : ",end = "")
							anime(password)
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
		
		
