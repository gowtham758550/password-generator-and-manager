try:
 import pyAesCrypt
 import getpass
 import os
 import binascii
 import string
 import re
 import secrets
except ImportError:
	print('Critical Modules Not Found!\nPress any key to continue...')
	x=input()
	exit(1)

print("********************____PASSWORD MANAGER____********************\n\n")
while(True):
	if os.path.isfile("mp.txt.aes"):
		print("\n\n*note : While you type in password fields, passwords are not printed on the screen for security purpose don't worry about it")
		master_password = getpass.getpass("Enter your password : ")
		with open("pass.txt") as file:
			temp_str = ""
			for i in file:
				temp_str += i
		file.close()
		with open("mp.txt.aes","rb") as FileIn:
			with open("new.txt","wb") as FileOut:
				buffer_size = 64*1024
				encfilesize = os.stat("mp.txt.aes").st_size
				pyAesCrypt.decryptStream(FileIn,FileOut,temp_str,buffer_size,encfilesize)
			FileOut.close()
		FileIn.close()
		with open("new.txt","r") as file:
			temp_pass = ""
			for i in file:
				temp_pass += i
		file.close()
		os.remove("new.txt")
		if temp_pass == master_password:
			print("\n1. Generate password\n2. Fetch password\n3. Change master password(COMMING SOON)")
			choice = int(input("\nEnter your choice (1,2) : "))
			if choice == 1:
				website_name = input("*\nnote : you can retrieve the passwords with the website name you entered\n\nEnter website name : ").lower()
				generated_pass = ""
				str = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation  
				generated_pass = ''.join(secrets.choice(str) for i in range(int(input("\nEnter number of characters for your password : "))))	
				print("Generated password for you : ",generated_pass)
				print("\nDon't worry about password complexity you can fetch the password by this tool.")
				with open("null.txt","a") as file:
					file.write(website_name+generated_pass+"\n")
					file.close()
				with open("null.txt","rb") as FileIn:
					with open("null.txt.aes","wb") as FileOut:
						pyAesCrypt.encryptStream(FileIn,FileOut,temp_pass,buffer_size)
					FileOut.close()
				FileIn.close()
				os.remove("null.txt")
                                print("press any key to exit")
                                x = input()
                                exit(1)
			elif choice == 2:
				website_name = input("\nEnter the website name to fetch password : ").lower()
				encfilesize = os.stat("null.txt.aes").st_size
				with open("null.txt.aes","rb") as FileIn:
					with open("null.txt","wb") as FileOut:
						pyAesCrypt.decryptStream(FileIn,FileOut,temp_pass,buffer_size,encfilesize)
					FileOut.close()
				FileIn.close()
				fetch_pass = ""
				with open("null.txt","r") as file:
					for line in file.readlines():
						if re.search(rf"{website_name}*",line,re.I):
							fetch_pass = line.strip(website_name)
				if len(fetch_pass) == 0:
					print("\nNo passwords found for this website name or you may enter wrong website name")
				else:
					print("\nPassword Fetched : ",fetch_pass)
				os.remove("null.txt")
                                print("press any key to exit")
                                x = input()
                                exit(1)			
		else:
			print("**********Incorrect password**********")
		break
	
	else:
		print("Welcome to password manager\nCreate your master password.\n*note : You can generate and fetch passwords by using this master password only.\n\n*note : While you enter password in passwors fields, passwords are not printed in screen it is only for your security purpose don't worry about it")
		while(True):
			master_password = getpass.getpass("Create master password: ")
			confirm_master = getpass.getpass("Retype your password : ")
			if master_password == confirm_master:
				break
			else:
				print("\n\npassword are not matching do again")
		password = binascii.b2a_hex(os.urandom(20))
		buffer_size = 64*1024
		with open("pass.txt","ab") as file:
			file.write(password)
		file.close()
		with open("mp.txt","ab") as file:
			file.write(master_password.strip().encode())
		with open("mp.txt","rb") as FileIn:
			with open("mp.txt.aes","wb") as FileOut:
				pyAesCrypt.encryptStream(FileIn,FileOut,password.decode(),buffer_size)
			FileOut.close()
		FileIn.close()
		os.remove("mp.txt")
                print("your master password created you can use the password to use this tool :)")
			
			
		
	
		
		
	

