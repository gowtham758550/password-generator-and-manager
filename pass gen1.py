try:
  import string
  import secrets
  from datetime import datetime
except ImportError:
	print("Required Modules Not Found!")
	exit(1)

print("Enter number of characters for password,website name and id or username")

def randompassword():
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits+string.punctuation
    return''.join(secrets.choice(chars) for x in range(0,int(input())))
    
    




with open("C:\password.txt","a") as file:
	file.write("\n\n"+str(datetime.now().strftime("%B-%d-%y\t%H-%M-%S"))+"\nPassword : "+randompassword()+"\nWebsite : "+input()+"\nId : "+input())
