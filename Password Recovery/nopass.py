
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
import binascii

#check internet connection
def check_connection():
	try:
		urllib.request.urlopen("https://google.com")
	except:
		print("You have no active internet connection\n\n")
		x = input("press enter to exit")
		sys.exit(1)

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
       sys.exit(1)
 print("Installation completed :)\n")
 print('Restart the program to finish installation!\nPress any key to continue...')
 x=input()
 sys.exit(1)


#buffer size for encryption and decryption
buffer_size = 64*1024
temp_str2 = ""
password = ""			
			
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
	
if os.path.isfile("mp.txt.aes"):
		#master_password = getpass.getpass("\n\nEnter your password : ")
		#get_key function returns the key for decryption
 print('Scanning for passwords...')
 key = get_key()
		#call decrypt_file() function 
 decrypt_file("mp.txt.aes",key)
 os.rename('temp.txt','masterpasswordplaintext.txt')
 print('Recovered Masterpassword hash saved as masterpasswordplaintext.txt')
 decrypt_file("secret.txt.aes",key)
 os.rename('temp.txt','userpasswordsplaintext.txt')
 print('Recovered Userpasswords saved as userpasswordsplaintext.txt')
 print('Done')

