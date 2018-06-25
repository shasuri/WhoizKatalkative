from sys import path
path.insert(0, "../console_ver")
from set_user_name import gui_set_user
from MemberInfo import MemberInfo
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
		self.geometry("600x300+50+125")
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

		next_button = Button(bottom_frame,text="Next",width=10,command=self.file_exist)
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
				if self.encoding_select.get() == "UTF-8":
					messagebox.showinfo("Error!","Error : "+str(value_error)+".\nCheck the log is right to form.")
				else:
					messagebox.showinfo("Error!","Error : "+str(value_error)+".\nCheck the log is right to form, or try with 'UTF-8' encoding.")

			except IndexError as index_error:
				messagebox.showinfo("Error!","Error : "+str(index_error)+".\nCheck the log is right to form.")

		else:
			messagebox.showinfo("File check","Wrong path...")

	def encoding_information(self):
		
		messagebox.showinfo("Encoding tip","Default encoding type of log file of kakaotalk is UTF-8.")

	def next_step(self, file_path, encoding_type):

		self.chat_room = result_loader(file_path, encoding_type)

		if self.chat_room.roomType == 'personal':
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
		try:
			gui_set_user(self.chat_room,self.user_name_select.get())
		except:
			pass
		self.result = ResultPage(self.controller.container,self.controller,self.chat_room)
		self.result.grid(row=0,column=0,sticky="nsew")
		self.result.tkraise()

class ResultPage(Frame):

	def __init__(self,super_frame,controller,chat_room):
		Frame.__init__(self,super_frame)
		self.chat_room = chat_room
		self.controller = controller
		self.controller.geometry("600x375+100+100")
		self.controller.resizable(True,True)
		
		#------------------------------------------
		title_frame = Frame(self)
		title_frame.pack(fill=BOTH,padx=10,pady=10)
		
		if self.chat_room.roomType == 'personal':
			title_label = Label(title_frame,text="You are chatting with : "+self.chat_room.title)
		else:
			title_label = Label(title_frame,text="Chatting room title : "+self.chat_room.title)
		
		title_label.pack(side=LEFT)
		
		#------------------------------------------
		date_frame = Frame(self)
		date_frame.pack(fill=BOTH,padx=10)

		save_date_label = Label(date_frame,text="Log is saved at "+str(self.chat_room.logSaveDate))
		save_date_label.pack(side=LEFT)

		#-------------------------------------------
		bottom_frame = Frame(self)
		bottom_frame.pack(fill=BOTH,padx=10,pady=10)

		#-------------------------------------------
		info_frame = Frame(bottom_frame)
		info_frame.pack(fill=BOTH)


		info_types = ('Invited date','Talk average','Talk','Plain texts','Chat length','Emoticons','Images','Internet links','Videos','Hashtags','Etc. files','Addresses','Voice records')

		self.result_table = ttk.Treeview(info_frame,columns=info_types,selectmode="extended")
		
		table_yscroll = ttk.Scrollbar(info_frame,orient="vertical",command=(self.result_table).yview)
		table_yscroll.pack(side=RIGHT,fill=Y)
		table_xscroll = ttk.Scrollbar(info_frame,orient="horizontal",command=(self.result_table).xview)
		table_xscroll.pack(side=BOTTOM,fill=X)
		
		self.result_table.configure(yscrollcommand=table_yscroll.set,xscrollcommand=table_xscroll.set)

		self.result_table.column('#0',stretch=YES,minwidth=10,width=100)
		self.result_table.heading('#0',text='User name')
		
		for type_set_index in range(len(info_types)):
			self.result_table.column('#'+str(type_set_index+1),stretch=YES,minwidth=20,width=80)
			self.result_table.heading('#'+str(type_set_index+1),text=info_types[type_set_index],anchor=W)
		
		self.result_table.column('#1',stretch=YES,minwidth=20,width=130)

		# Consist table contents.
		for insert_index in range(len(self.chat_room.memberList)):
			info_values = (self.chat_room.memberList[insert_index].invitedDate,)

			if self.chat_room.memberList[insert_index].infoList[MemberInfo.talk.value] != 0 :
				talk_average = float(self.chat_room.memberList[insert_index].infoList[MemberInfo.talkSize.value]) / self.chat_room.memberList[insert_index].infoList[MemberInfo.talk.value]
				talk_average = round(talk_average,2)
			else :
				talk_average = 0.00

			info_values += (talk_average,)
			
			for value_index in range(len(self.chat_room.memberList[insert_index].infoList)):
				info_values += (self.chat_room.memberList[insert_index].infoList[value_index],)
			
			self.result_table.insert('','end',text=self.chat_room.memberList[insert_index].name,values=info_values)

		self.result_table.pack(side=TOP)

		#-----------------------------------------
		exit_frame = Frame(bottom_frame)
		exit_frame.pack(fill=BOTH,side=BOTTOM)
		
		exit_button = Button(exit_frame,text="Exit",width=10,command=self.close_page)
		exit_button.pack(side=RIGHT)

	def close_page(self):
		self.controller.destroy()


Katalkative_beta = App()
Katalkative_beta.mainloop()
