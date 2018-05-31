from sys import path
path.insert(0, "../console_ver")
from set_user_name import gui_set_user
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from os.path import isfile
from gui_main import result_loader

class App(Tk):
	def __init__(self):
		Tk.__init__(self)

		self.title("Katalkative GUI Beta")
		self.geometry("600x300+100+100")
		self.resizable(False,False)

		self.container = Frame(self)
		self.container.pack(expand=True,fill=BOTH)
		self.container.grid_rowconfigure(0, weight=1)#research!!!
		self.container.grid_columnconfigure(0, weight=1)

		self.intro = IntroPage(self.container,self)
		self.intro.grid(row=0,column=0,sticky="nsew")
		
		self.intro.tkraise()
 

class IntroPage(Frame):
	def __init__(self, super_frame, controller):
		Frame.__init__(self,super_frame)
		self.controller = controller

		descript_frame = Frame(self)#,bd=2,bg="red") 
		descript_frame.pack(fill=X,padx=10,pady=10)

		intro = Label(descript_frame,text="Katalkative GUI Beta. Select your kakaotalk log file from mobile device.")
		intro.pack(side=LEFT,fill=X)

	#-------------------------------------
		input_frame = Frame(self)#,bd=2,bg="green")
		input_frame.pack(fill=BOTH,padx=10,pady=20)

		path_label = Label(input_frame,text='File path : ')
		path_label.pack(side=LEFT)

		self.path_input = Entry(input_frame,text="default")
		self.path_input.pack(expand=True,fill=X,side=LEFT,padx=10)

		path_select = Button(input_frame,text="Select...",width=10,command=self.file_selector)
		path_select.pack(side=LEFT,padx=20)

	#-------------------------------------
		encoding_select_frame = Frame(self)
		encoding_select_frame.pack(fill=BOTH,padx=10,pady=50)

		encoding_label = Label(encoding_select_frame,text="File encoding : ")
		encoding_label.pack(side=LEFT)

		self.encoding_select = ttk.Combobox(encoding_select_frame, state="readonly")
		self.encoding_select['values'] = ('UTF-8','CP949','euc-kr','ANSI','unicode_escape','ASCII')
		self.encoding_select.current(0)
		self.encoding_select.pack(side=LEFT,padx=10)

		encoding_info_button = Button(encoding_select_frame,text="i",width=2,command=self.encoding_information)
		encoding_info_button.pack(side=LEFT)

	#-------------------------------------
		bottom_frame = Frame(self)#,bd=2,bg="blue")
		bottom_frame.pack(fill=X,side=BOTTOM,pady=10)

		next_button = Button(bottom_frame,text="Next",width=10,command=self.file_exist)#lambda:controller.next_page.tkraise())
		next_button.pack(side=RIGHT,padx=30)

	#-------------------------------------
	def file_selector(self):
		file_path = filedialog.askopenfilename(title="Select file",filetypes=(("Text files", "*.txt"),("all files", "*.*")))
		self.path_input.delete(0,END)
		self.path_input.insert(0,file_path)

	def file_exist(self):
		open_file = self.path_input.get()
		
		if(isfile(open_file)):
			messagebox.showinfo("File check","Opening "+self.path_input.get()+"...")

			try:
				self.next_step(open_file,self.encoding_select.get())
				self.next_page.tkraise()
			
			except UnicodeDecodeError as unicode_error:
				messagebox.showinfo("Error!","Error : "+str(unicode_error)+".\nTry with 'UTF-8' encoding.")

			except ValueError as value_error:
				messagebox.showinfo("Error!","Error : "+str(value_error)+".\nTry with 'UTF-8' encoding.")

		else:
			messagebox.showinfo("File check","Wrong path...")

	def encoding_information(self):
		
		messagebox.showinfo("Encoding tip","Default encoding type of log file of kakaotalk is UTF-8.")

	def next_step(self, file_path, encoding_type):

		self.chat_room = result_loader(file_path, encoding_type)

		if self.chat_room.groupType == 'personal':
			self.next_page = ResultPage(self.controller.container, self.controller, self.chat_room)
		else:
			self.next_page = UserSelectPage(self.controller.container, self.controller, self.chat_room)
		self.next_page.grid(row=0,column=0,sticky="nsew")


class UserSelectPage(Frame):

	def __init__(self,super_frame,controller,chat_room):
		Frame.__init__(self,super_frame)
		self.controller = controller
		self.chat_room = chat_room
		
		select_frame = Frame(self)
		select_frame.pack(fill=BOTH,padx=10,pady=20)

		select_label = Label(select_frame,text="Select your name in the box.")
		select_label.pack(side=LEFT,padx=10)

		name_select_list = ()

		chat_room_members = self.chat_room.memberList

		for box_index in range(len(chat_room_members)):	
			if chat_room_members[box_index].name != '회원님':
				name_select_list += (chat_room_members[box_index].name,)
			else:
				pass

		self.user_name_select = ttk.Combobox(select_frame, state="readonly")
		self.user_name_select['values'] = name_select_list
		self.user_name_select.current(0)
		self.user_name_select.pack(side=LEFT,padx=10)

		result_button = Button(self,text="Next",width=10,command=self.result_step)
		result_button.pack()

	def result_step(self):
		gui_set_user(self.chat_room,self.user_name_select.get())
		self.result = ResultPage(self.controller.container,self.controller,self.chat_room)
		self.result.grid(row=0,column=0,sticky="nsew")
		self.result.tkraise()

class ResultPage(Frame):

	def __init__(self,super_frame,controller,chat_room):
		Frame.__init__(self,super_frame)
		self.chat_room = chat_room

		controller.geometry("1200x500+100+100")
		controller.resizable(True,True)

		info_types = ('Invited date','Talk','Plain texts','Chat length','Emoticons','Images','Internet links','Videos','Hashtags','Etc files','Addresses','Voice records')

		self.result_table = ttk.Treeview(self,columns=info_types,selectmode="extended")

		self.result_table.column('#0',stretch=YES,minwidth=10,width=100)
		self.result_table.heading('#0',text='User name')
		
		for type_set_index in range(len(info_types)):
			self.result_table.column('#'+str(type_set_index+1),stretch=YES,minwidth=20,width=80)
			self.result_table.heading('#'+str(type_set_index+1),text=info_types[type_set_index],anchor=W)
		self.result_table.column('#1',stretch=YES,minwidth=20,width=130)

		for insert_index in range(len(self.chat_room.memberList)):
			info_values = (self.chat_room.memberList[insert_index].invitedDate,)

			for value_index in range(len(self.chat_room.memberList[insert_index].infoList)):
				info_values += (self.chat_room.memberList[insert_index].infoList[value_index],)
			
			self.result_table.insert('','end',text=self.chat_room.memberList[insert_index].name,values=info_values)
	
		self.result_table.pack()
myApp = App()
myApp.mainloop()
