from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from os.path import isfile

class App(Tk):
	def __init__(self):
		Tk.__init__(self)

		self.title("Katalkative GUI Beta")
		self.geometry("600x300+100+100")
		self.resizable(False,False)

		container = Frame(self)
		container.pack(expand=True,fill=BOTH)
		container.grid_rowconfigure(0, weight=1)#research!!!
		container.grid_columnconfigure(0, weight=1)

		self.intro = IntroPage(container,self)
		self.intro.grid(row=0,column=0,sticky="nsew")

		self.result = ResultPage(container,self)
		self.result.grid(row=0,column=0,sticky="nsew")
		
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
		input_frame.pack(fill=BOTH,padx=10,pady=50)

		file_path_label = Label(input_frame,text='File path : ')
		file_path_label.pack(side=LEFT)

		self.file_path_input = Entry(input_frame,text="default")
		self.file_path_input.pack(expand=True,fill=X,side=LEFT,padx=10)

		file_select_button = Button(input_frame,text="Select...",width=10,command=self.file_selector)
		file_select_button.pack(side=LEFT,padx=20)

	#-------------------------------------
		bottom_frame = Frame(self)#,bd=2,bg="blue")
		bottom_frame.pack(fill=X,side=BOTTOM,pady=10)

		next_button = Button(bottom_frame,text="Next",width=10,command=self.file_exist)#lambda:controller.result.tkraise())
		next_button.pack(side=RIGHT,padx=30)

	#-------------------------------------
	def file_selector(self):
		file_path = filedialog.askopenfilename(title="Select file",filetypes=(("Text files", "*.txt"),("all files", "*.*")))
		self.file_path_input.delete(0,END)
		self.file_path_input.insert(0,file_path)

	def file_exist(self):
		open_file = self.file_path_input.get()
		
		if(isfile(open_file)):
			messagebox.showinfo("File check","Opening "+self.file_path_input.get()+"...")
			self.controller.result.tkraise()
		else:
			messagebox.showinfo("File check","Nah...")

class ResultPage(Frame):

	def __init__(self,super_frame,controller):
		Frame.__init__(self,super_frame)
		self.controller = controller
		result_label = Label(self, text="Result!")
		result_label.pack()

myApp = App()
myApp.mainloop()