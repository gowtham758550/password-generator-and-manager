import string
import random
from datetime import datetime


print("Enter number of characters for password,website name and id or username")

def randompassword():
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits+string.punctuation
    return''.join(random.choice(chars) for x in range(0,int(input())))
    
    




with open("password.txt","a") as file:
	file.write("\n\n"+str(datetime.now().strftime("%B-%d-%y\t%H-%M-%S"))+"\nPassword : "+randompassword()+"\nWebsite : "+input()+"\nId : "+input())
