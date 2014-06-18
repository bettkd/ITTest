#!/usr/bin/python
#Author: Dominic Bett
#Date: 6/4/2014
#Company: Dell Inc

from Tkinter import *
import ttk
import Tix
import os
import ITFunctions
import tkMessageBox

itfx = ITFunctions.ITFunctions()

class InfrastructureTool(Frame):
	
	def populate_tree(self, tree, node):

		path = tree.set(node, 'fullpath')
		tree.delete(*tree.get_children(node))

		parent = tree.parent(node)
		special_dirs = []
		# testt= special_dirs + os.listdir(path) 
		# print testt
		# return
		# print "os.listdir(path)=",os.listdir(path)

		for p in os.listdir(path):
			#ptype = None
			p = os.path.join(path, p).replace('\\', '/')
			#print p 
			if os.path.isdir(p): ptype = 'directory'
			elif os.path.isfile(p): ptype = 'file'
			#print "ptype=", ptype
			fname = os.path.split(p)[1]
			id = tree.insert(node, 'end', text=fname, values=[p, ptype])

			if ptype == 'directory':
				if fname not in ('.', '..'):
					tree.insert(id, 0, text='dummy')
					tree.item(id, text=fname, tags=['#entry'])
			elif ptype == 'file':
				pass
			#	size = os.stat(p).st_size
			#	tree.set(id, 'size', '%d bytes' % size)

	def populate_roots(self, tree):
		#dir = os.path.abspath('.').replace('\\', '/')
		dir = '../pyinstaller'
		node = tree.insert('', 'end', text=dir, open=True, values=[dir, 'directory'])
		self.populate_tree(tree, node)

	def update_tree(self, event):
		tree = event.widget
		self.populate_tree(tree, tree.focus())
	
	def change_dir(self, event):
		tree = event.widget
		node = tree.focus()
		if tree.parent(node):
			path = os.path.abspath(tree.set(node, 'fullpath'))
			if os.path.isdir(path):
				os.chdir(path)
				tree.delete(tree.get_children(''))
				self.populate_roots(tree)
	
	def onTreeClick(self, event):
		tree = event.widget
		item_id = str(tree.focus())
		#item_id = str(tree.has("#entry"))
		print 'Selected item was %s' % item_id
		
		item = tree.item(item_id)
		#flag = "#another_tag" in item['tags']
		#print ' flag = %s' % flag
		#pass
		print item["text"]

	def _addTest(event, host_tree, tests_tree, self):
		host_tree.insert(host_tree.node, end, text="testid")
	'''
	def select_cmd(self, selected):
		print 'Selected items:', selected

	def messagebox(self):
		tkMessageBox.showerror('Warning', 'Test currently in progress will be terminated!')
	'''
	def createWidgets(self):	
	
		'''================Tool Tips================='''
		#Initializing it - we can call it whenever we want to use it
		#toolTip = Baloon(self)

		'''================Buttons==================='''
		#Run Button
		imgRun = PhotoImage(file="imgs/run.gif")
		btnRun = Button(self, text='>', image=imgRun, fg='green', width=50, height=36, command=None)
		btnRun.grid(padx=10, pady=10, row=0, column=0)
		btnRun.image = imgRun #To save the button's image from garbage collection
		#toolTip.bind(btnRun, 'Run Test')

		#Abort Button
		imgAbort = PhotoImage(file="imgs/abort.gif")
		btnAbort = Button(self, text='X', image=imgAbort, fg='red', width=50, height=36, command=None)
		btnAbort.grid(padx=10, pady=10, row=0, column=1)
		btnAbort.image = imgAbort

		#LoadHosts Button
		imgHost = PhotoImage(file="imgs/server.gif")
		btnLoadHosts = Button(self, text='H', image=imgHost, fg='blue', width=50, height=36, command=None)
		btnLoadHosts.grid(padx=10, pady=10, row=0, column=2)
		btnLoadHosts.image = imgHost

		#LoadTests Button
		imgTests = PhotoImage(file="imgs/script.gif")
		btnLoadTests = Button(self, text='T', fg='blue', image=imgTests, width=50, height=36, command=None)
		btnLoadTests.grid(padx=10, pady=10, row=0, column=3)
		btnLoadTests.image = imgTests

		#SaveConfig Button
		imgSaveConf = PhotoImage(file="imgs/save.gif")
		btnSaveConfig = Button(self, text='S', image=imgSaveConf, width=50, height=36, command=None)
		btnSaveConfig.grid(padx=10, pady=10, row=0, column=4)
		btnSaveConfig.image =imgSaveConf

		#LoadSavedConfig Button
		imgOpenConfig = PhotoImage(file="imgs/open.gif")
		btnLoadSavedConfig = Button(self, text='L', image=imgOpenConfig, width=50, height=36, command=None)
		btnLoadSavedConfig.grid(padx=10, pady=10, row=0, column=5)
		btnLoadSavedConfig.image = imgOpenConfig

		'''================TreeViews==================='''
		#Hosts Tree
		host_tree = ttk.Treeview(self)
		host_tree.column('#0', stretch=False, width=180)
		host_tree.heading('#0',text='Hosts', anchor=W)
		for n in xrange(0, len(itfx.hostItem('hostnames'))):
			host_tree.insert('', 'end', 'host'+str(n),
				text=itfx.hostItem('hostnames')[n],
				tag=itfx.hostItem('ips')[n])
		#Place holder children(tests)
		host_tree.insert('host1', 2, text='Test 1')
		host_tree.insert('host2', 4, text='Test 2')
		host_tree.grid(padx=10, pady=10, row =1, column=0, columnspan=3)

		#host_tree.configure(command=self.select_cmd, selectmode='extended')

		#Test Tree
		tests_tree = ttk.Treeview(columns=('fullpath', 'type'), displaycolumns='', selectmode=EXTENDED)
		tests_tree.column('#0', stretch=False, width=180)
		tests_tree.heading('#0', text='Directory Browser', anchor='w')

		self.populate_roots(tests_tree)
		tests_tree.bind('<<TreeviewSelect>>', self.update_tree)
		#tests_tree.bind('<Double-Button-1>', self.change_dir)

		tests_tree.place (x=240, y=72)
		#tests_tree.grid(padx=5, pady=5, row=1, column=3, columnspan=3)

		'''=======More Buttons=================='''
		#Results Button
		btnResults = Button(self, text='Preview Results', relief=FLAT, fg='blue', width=10, height=2)
		btnResults.grid(padx=10, pady=10, row =2, column=0, columnspan=2)

		#btnMoveUp Button
		imgMoveUp = PhotoImage(file="imgs/move_up.gif")
		btnMoveUp = Button(self, text='MU', relief=FLAT, image=imgMoveUp, fg='brown', width=33, height=33)
		btnMoveUp.place(x=128, y=312)
		btnMoveUp.image = imgMoveUp

		#btnMoveDown Button
		imgMoveDown = PhotoImage(file="imgs/move_down.gif")
		btnMoveDown = Button(self, text='MD', relief=FLAT, image=imgMoveDown, fg='brown', width=33, height=33)
		btnMoveDown.place(x=164, y=312)
		btnMoveDown.image = imgMoveDown

		#Add Test Button
		btnAddTest = Button(self, text='<<Add Test', relief=FLAT, fg='blue', width=10, height=2)
		btnAddTest.grid(padx=10, pady=10, row=2, column=3, columnspan=2)
		#btnAddTest.bind('<Button-1>', host_tree, tests_tree, self._addTest)

		#Close Button
		imgClose = PhotoImage(file="imgs/quit.gif")
		btnClose = Button(self, text='Q', image=imgClose, fg='brown', width=45, height=36, command=self.quit)
		btnClose.grid(padx=10, pady=10, row=2, column=5)
		btnClose.image = imgClose


		'''==============Text Area============='''
		txtProgress = Text(width=60, height=12)
		txtProgress.grid(padx=10, pady=10, row=3, column=0, columnspan=6)

		'''=====Selection Test============='''
		tests_tree.tag_bind('#entry', '<1>', self.onTreeClick)
		#tests_tree.tag_bind(item, tests_tree.item, '<1>', [list(item_clicked), %W, %x, %y])
		#test_items = items = map(int, tests_tree.curselection())
		#for item in test_items:
		#	pass

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master.title('Infrastructure Test Tool')
		self.grid()
		self.createWidgets()
		
def main():	
	root = Tk()	
	root.resizable(0, 1)
	root.geometry('+300+300')
	#appIcon = PhotoImage(file='imgs/appIcon.gif')
	#root.Tk.call('wm', 'iconphoto', root._w, appIcon)
	app = InfrastructureTool(root)
	app.mainloop()
		
if __name__ == '__main__':
	main()