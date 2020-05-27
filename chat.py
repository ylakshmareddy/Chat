from tkinter import *
from tkinter import messagebox
import requests
import threading
import os

sys.stdout = open(os.devnull, "w")
sys.stderr = open(os.devnull, "w")

def GenerateEntryFields():
	btnSignIn.pack_forget();
	btnSignUp.pack_forget();
	global lblUserName 
	lblUserName = Label(window, text="UserName:");
	lblUserName.pack();
	global txtUserName 
	txtUserName = Entry(window);
	txtUserName.pack();
	global lblPassword 
	lblPassword= Label(window, text="Password:");
	lblPassword.pack();
	global txtPassword 
	txtPassword = Entry(window);
	txtPassword.pack();

def GetUserDetails():
	global UserName, Password
	UserName = txtUserName.get();
	Password = txtPassword.get();

def DestroyEntryWidgets():
	txtUserName.destroy();
	txtPassword.destroy();
	lblUserName.destroy();
	lblPassword.destroy();


def SignUpValidate():
	GetUserDetails();
	URL = "http://165.22.14.77:8080/LakshmaReddy/chat/signup.jsp?UserName={}&Password={}".format(UserName, Password);
	response = requests.get(URL);
	messagebox.showinfo('Response', response.text);
	DestroyEntryWidgets();
	btnRegister.destroy();
	btnSignIn.pack();
	btnSignUp.pack();

def GetActiveUsers():
	URL = "http://165.22.14.77:8080/LakshmaReddy/chat/ActiveUsers.jsp?UserName={}".format(UserName)
	while True:
		response = requests.get(URL)
		txtActiveUsers.delete(1.0, END)
		txtActiveUsers.insert(1.0, response.text.strip().replace('<br>', ''))

def ShowAllMessages():
	URL = "http://165.22.14.77:8080/LakshmaReddy/chat/ShowMessages.jsp?UserName={}".format(UserName)
	while True:
		response = requests.get(URL)
		txtAllMessages.delete(1.0, END)
		txtAllMessages.insert(1.0, response.text.strip());


def SendMessage():
	Message = txtMessage.get()
	txtMessage.delete(0, last=END)
	URL = "http://165.22.14.77:8080/LakshmaReddy/chat/SendMessage.jsp?UserName={}&Message={}".format(UserName, Message);
	response = requests.get(URL);
	if(str(response).find("200") >= 0):
		messagebox.showinfo('status', 'Message sent successfully.')

def SignOut():
	URL = "http://165.22.14.77:8080/LakshmaReddy/chat/SignOut.jsp?UserName={}".format(UserName)
	response = requests.get(URL)
	if(str(response).find("200") >= 0):
		messagebox.showinfo('status', 'Logged out successfully.')
		lblActiveUsers.destroy()
		txtActiveUsers.destroy()
		txtAllMessages.destroy();
		txtMessage.destroy()
		lblAllMessages.destroy()
		btnSignOut.destroy()
		btnSendMessage.destroy()
		btnSignIn.pack()
		btnSignUp.pack()

def SignInValidate():
	GetUserDetails();
	URL = "http://165.22.14.77:8080/LakshmaReddy/chat/signin.jsp?UserName={}&Password={}".format(UserName, Password);
	response = requests.get(URL);
	if(response.text.find("success") >= 0):
		messagebox.showinfo('Response', 'Login Successful.')
		DestroyEntryWidgets();
		btnLogin.destroy();
		global lblActiveUsers, txtActiveUsers, txtAllMessages, txtMessage, lblAllMessages, btnSignOut, btnSendMessage
		lblActiveUsers = Label(window, text="Active Users:")
		lblActiveUsers.pack();
		txtActiveUsers = Text(window, height=10, width=30)
		txtActiveUsers.pack()
		thread1 = threading.Thread(target=GetActiveUsers)
		thread1.start()
		lblAllMessages = Label(window, text="All Messages:")
		lblAllMessages.pack()
		txtAllMessages = Text(window, height=15, width=40)
		txtAllMessages.pack()
		thread2 = threading.Thread(target=ShowAllMessages)
		thread2.start()
		txtMessage = Entry(window)
		txtMessage.pack()
		btnSendMessage = Button(window, text="Send Message", command=SendMessage)
		btnSendMessage.pack()
		btnSignOut = Button(window, text="Sign Out", command=SignOut)
		btnSignOut.pack()
	elif(response.text.find("failed") >= 0):
		messagebox.showinfo('Response', 'Invalid Login Credentials.')
		DestroyEntryWidgets();
		btnLogin.destroy();
		btnSignIn.pack();
		btnSignUp.pack();

def SignIn():
	GenerateEntryFields();
	global btnLogin 
	btnLogin = Button(window, text="SignIn", command=SignInValidate);
	btnLogin.pack();

def SignUp():
	GenerateEntryFields();
	global btnRegister
	btnRegister = Button(window, text="SignUp", command=SignUpValidate);
	btnRegister.pack();

window = Tk();
window.geometry('1000x1000');
window.title("Piper Chat!");

btnSignIn = Button(window, text="SignIn", command=SignIn);
btnSignIn.pack();

btnSignUp = Button(window, text="SignUp", command=SignUp);
btnSignUp.pack();

mainloop();