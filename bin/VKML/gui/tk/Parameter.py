""""Parameter.py
"""
 # ############################################################################
 # FILE: Parameter.py
 #
 #
 #  Author: Alex Bartol <nanohub@alexbartol.com>
 #       Copyright 2009
 #  Author: Jonas A. Krieger <econversion@empa.ch>
 #       Copyright 2021
 # 
 # ############################################################################
from sys import argv as ARGS
import tkinter
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as  tkFileDialog
from VKML.gui.tk.Menu import Menu

class Parameter:
    """ Simple class to keep things straight as parameters are passed into the
    Parser
    """	
    def __init__(self, name, display_name='', menu=None, parser=None, variable=str, default='', 
                    interval=(None, None), precision=1, filetype='open',button_text='Run'):
        """
        name - Varaible name
        menu - the Menu this should be added to (trumps parser)
        parser - the Parser instance this is added to
        variable - the *type* variable should be returned in
        default - the defaulted value for this variable
        interval - the range for integers/floats (None, None) -> infinate range
        filetype - should only be used for type of file (acceptable values are 'open', 'save' and 'directory')
        precision - the persision of a float value (if integer this is ignored and assumed '1')
            precision is measured in decimal points (1 == '0.0', 2 == '0.00' and so on)
        button_text - string, optional: Text on function button
        
        <Parameter>() returns the current value for given variable
        """
        try:
            self.parser = menu.Parser
        except AttributeError:
            if parser == None:
                tkMessageBox.showerror(title='Variable Error', 
                       message='Parameter: ' + name +' needs a Parser or Menu')
                import sys
                sys.exit(0)
            else:
                self.parser = parser
                self.parser.add(self)
        self.name = name
        if display_name == '':
            self.display_name = self.name
        else:
            self.display_name = display_name
        self.type = variable
        self.default = default
        self.out = default
        if self.type == tuple:
            self.out = self.out[0]
        if self.type == dict:
            self.out = self.out[list(self.out.keys())[0]]
        self.range = interval
        self.entry = None
        self.label = None
        self.button_text=button_text
        self.boolstatus = True
        self.entry_special = None
        self.top = None
        self.precision = precision
        
        if self.type == 'image':
            pass #put stuff here for image stuff
        if self.type == list:
            self.type = []
            for i in range(len(self.default)):
                if type(self.default[i]) != list:
                    self.type.append(type(self.default[i]))
                else:
                    tmp = []
                    for j in range(len(self.default[i])):
                        tmp.append(type(self.default[i][j]))
                    self.type.insert(len(self.type), tmp)

        if len(self.parser.tabs) == 0:
            default = Menu(self.parser, title='default')
        if menu == None:
            for tab in self.parser.tabs:
                if tab.title == 'default':
                    tab.add(self)
        else:
            menu.add(self)
        
    def withinrange(self, value):
        """Returns True if the value is within the range given to the parameter
        
        None as the left hand limit is considered negative infinity and None as
        the right hand limit is considered positive infinity
        """
        try:
            value = self.type(value)
            if self.range == (None, None):
                return True
            elif self.range[1] == None and self.range[0] <= value:
                return True
            elif self.range[0] == None and self.range[1] >= value:
                return True
            elif value >= self.range[0] and value <= self.range[1]:
                return True
        except (AttributeError, ValueError):
            return False
        return False
        

    def update(self, value=None):
        """Updates the callback functions
        Changes the internal variables
        shows error messages if neccessary
        
        if a value is give to update, it updates the special widget, if not
        it updates the standard widget
        """
        if value == None:
            if self.type != bool:
                self.out = self.entry.get()
                self.entry_special['text'] = self.out
            else:
                self.out = self.boolstatus
        else:
            if self.type == str:
                self.out = self.entry.get()
            elif self.withinrange(value):
                self.out = value
                self.entry_special['text'] = self.out
                self.entry.set(self.out)
            else:
                tkMessageBox.showerror(message="Value Error for Variable: " + 
                                       self.name + "\nExpected value from:\n" +
                                       self.getrange() + '\nWith type: ' + 
                                       str(self.type), title="Value Error")
        self.parser.update()

    def get_Label(self,top,row,column):
        if self.label ==None:
            self.label=tkinter.Label(top, text=self.display_name)
            self.label.grid(row=row,column=column)
        return self.label
    
    def get_widget(self, top, row_number=0):
        """Returns the widget for the specified parameter
        lists return a button that links to the window
        
        top is the tkinter toplevel window
        row_number is the row number
        """
        self.top = top


        self.boolstatus = False
        if self.type == bool:
            def on_press():
                """swaps the status of the boolean linked to the checkbox"""
                self.boolstatus = not self.boolstatus
                self.update()
            #The name argument is currently necessary due to a bug in tkinter
            #see https://bugs.python.org/issue29402
            alnum_name=''.join(e for e in self.name if e.isalnum())
            self.entry = tkinter.Checkbutton(top,command=on_press,name='!checkbutton_{}'.format(alnum_name))
            if self.out == True:
                self.entry.select()
                on_press() #changes boolstatus
            else:
                self.entry.deselect()
            self.entry.grid(row=row_number, column=1, sticky=tkinter.E)
        elif type(self.type) == list or self.type == list:
            self.entry = tkinter.Button(top, text='MODIFY', 
                              command=(lambda i=0: _show_list_window(self) ))
            self.entry.grid(row=row_number, column=1, sticky=tkinter.E)
        elif self.type == float:
            self.entry = tkinter.Scale(top, from_=self.range[0], 
                              to=self.range[1], orient=tkinter.HORIZONTAL,
                              showvalue=False, 
                              command=(lambda i=0 : self.update()), 
                              resolution=1.0/(10**self.precision))
            self.entry.set(self.out)
            self.entry.grid(row=row_number, column=1, sticky=tkinter.E)
        elif self.type == int:
            self.entry = tkinter.Scale(top, from_=self.range[0], 
                                     to=self.range[1], showvalue=False,
                                     orient=tkinter.HORIZONTAL, 
                                     command=(lambda i=0 : self.update()),)
            self.entry.set(self.out)
            self.entry.grid(row=row_number, column=1, sticky=tkinter.E)
            
        elif self.type == str:
            self.entry = tkinter.Entry(top)
            self.entry.grid(row=row_number, column=1)
            self.entry.bind('<KeyRelease>', self.update)
            self.entry.insert(0, self.out)
        
        elif self.type == 'label':
            if self.default.lower().endswith('.jpg') or self.default.lower().endswith('.gif'):
                try:
                    #import ImageTk
                    self.photo = tkinter.PhotoImage(file=self.default)
                    self.entry = tkinter.Canvas(top, width=self.photo.width(), height=self.photo.height())
                    self.entry.create_image(0,0,image=self.photo, anchor=tkinter.NW)   
                except tkinter.TclError:
                    self.entry = tkinter.Label(top, text="Error Loading Image: " + self.default)
                except ImportError:
                    self.entry = tkinter.Label(top, text='Image Error with image: ' + self.default + '\nPython imageTk must be installed to display images')

            else:
                self.entry = tkinter.Label(top, text=self.default)
            self.entry.grid(row=row_number, column=1)
            
        elif self.type == 'image':
            def viewimage(event=None):
                root = tkinter.Toplevel()
                root.title(self.default)
                frame = tkinter.Frame(root, colormap="new", visual='truecolor').pack()
                try:
                    img = tkinter.PhotoImage(file=self.default)
                    #OH GOD! DON'T TOUCH IT!!!
                    root.geometry("%dx%d%+d%+d" % (img.width(),img.height(), int(top.geometry().split('+')[-2])+int(top.geometry().split('x')[0]), int(top.geometry().split('+')[-1])))
                    c = tkinter.Canvas(root, width=img.width(), height=img.height())
                    c.place(x=0,y=0)
                
                    def die(event=None):
                        root.destroy()
                    c.create_image(0, 0, image=img, anchor=tkinter.NW)
                    c.bind('<Button-1>', die)
                except tkinter.TclError:
                    l = tkinter.Label(root, text='Image Error with image: ' + self.default + '\nImage may be missing or of incompatable type')
                    l.pack()
                except ImportError:
                    l = tkinter.Label(root, text='Image Error with image: ' + self.default + '\nPython imageTk must be installed to display images')
                    l.pack()
                    
                root.mainloop()
            self.entry = tkinter.Button(top, text='Display', command=viewimage)
            self.entry.grid(row=row_number, column=1)

        elif self.type == 'function':
            
            kwargs = {}
            kwgs = False
            import inspect
            variables = inspect.getargspec(self.default)[0]
            if inspect.getargspec(self.default)[2] == 'kwargs':
                kwgs = True
                for param in self.parser.params:
                    if param.type != 'label':
                        kwargs[param.name] = param
        
            for param in self.parser.params:
                if param.name in variables and \
                        param.type != 'label' and \
                        param.type != 'function':
                    kwargs[param.name] = param
                    
            f = self.parser._command(self.default, kwargs, -1)
            
            self.entry = tkinter.Button(top, text=self.button_text, command=f.force_run)
            self.entry.grid(row=row_number, column=1)
            
        elif self.type == tuple:
            var = tkinter.StringVar(top)
            #This was originally var.set(self.default[0]) -L.R.
            var.set(self.out)
            self.entry = tkinter.OptionMenu(*((top, var) + tuple(self.default)))
            def u(a=None, b=None, c=None):
                self.out = var.get()
                self.update
                self.parser.update()
            var.trace_variable('w', u)
            self.entry.grid(row=row_number, column=1)
                        
        elif self.type == dict:
            self.dict_var = tkinter.StringVar(top)
            #This was originally var.set(self.default[0]) -L.R.
            invdict=dict((v, k) for k, v in self.default.items())
            self.dict_var.set(invdict[self.out])
            self.entry = tkinter.OptionMenu(*((top, self.dict_var) + tuple(self.default.keys())))
            def u(a=None, b=None, c=None):
                self.out = self.default[self.dict_var.get()]
                self.update
                self.parser.update()
            self.dict_var.trace_variable('w', u)
            self.entry.grid(row=row_number, column=1)
        
        
            
        
        if self.type == float or self.type == int:
            self.entry_special = tkinter.Label(top, text=str(self.out))
            self.entry_special.grid(row=row_number, column=2, sticky=tkinter.E,
                                    ipadx=20)
            self.entry_special.bind(sequence='<Button-1>', 
                                    func=self.start_entry)
        return self.entry
        
    def kill_special(self):
        """Destroys the special widget for integers/floats/files
        """
        if self.entry_special != None:
            self.entry_special.destroy()
        
    def start_entry(self, event):
        """Creates a popup Entry box that covers the Label
        """
        class EntryBox(tkinter.Toplevel):
            """Internal class used to make the Label's 'editable
            """
            def __init__(self, command=None, type=None):
                """Instanciates the EntryBox
                command is the command that updates the Label
                type is the necessary type for the label
                """
                self.command = command
                tkinter.Toplevel.__init__(self)
                
                self.overrideredirect(1)
                self.type = type
                self.entry = None
                self.bind('<ButtonPress-1>', self._press)
                self.bind('<ButtonPress>', self._close)
                self.bind('<Double-Button-1>', self._close)
                self.bind('<Return>', self._close)
                self.bind('<KeyPress-Escape>', self._close)
                self.bind('<KP_Enter>', self._close)
                self.up = 0

            def popup(self, parameter):
                """parameter is the parameter that was clicked on.
                
                This meathod actually starts the window (and disables window
                management fyi) 
                """
                self.entry = tkinter.Entry(self, width=10)
                self.entry.insert(0, str(parameter.out))
                self.entry.bind('<Return>', self._close)
                self.entry.bind('<KP_Enter>', self._close)
                self.entry.pack()
                self.entry.selection_clear()
                
                onto = parameter.entry_special
                rootx = onto.winfo_rootx()
                rooty = onto.winfo_rooty()
                self.geometry('+%d+%d' % (rootx, rooty))
                self.deiconify()
                self.up = 1
                
                try:
                    self.grab_set_global()
                    
                except tkinter.TclError:
                    pass

            def _close(self, event=None):
                """shuts off the special widget
                """
                self.grab_release()
                self.overrideredirect(0)
                self.withdraw()
                self.up = 0
                self._update()
                self.destroy()

            def _update(self, event=None):
                """Updates the widget
                """
                self.out = self.entry.get()
                if self.out == '':
                    return
                
                if self.command is not None:
                    self.command(self.type(self.out))
                    
            def _press(self, event):
                """Detects mouse clicks and determines if within current window
                if not then it closes the special widget
                """
                x, y = self.winfo_pointerxy()
                xo, yo = self.entry.winfo_rootx(), self.entry.winfo_rooty()
                window = self.winfo_containing(x, y)
                if window is None or window.winfo_toplevel() != self:
                    self._close()
                    
        EntryBox(self.update, self.type).popup(self)
        
        
    def list_works(self, test):
        """Assuming self.type is a list then this method returns None if the
        list has correct values. If not, this function returns the string used
        to notify the user where the error is (which cell)
        """
        assert type(test) == list == type(self.out)
        try:
            for i in range(len(test)):
                if type(test[i]) == list:
                    for j in range(len(test[i])):
                        self.type[i][j](test[i][j])
                else:
                    self.type[i](test[i])
            return None
        except (TypeError , ValueError):
            if type(test[0]) != list:
                return '\tCell ' + chr(ord('A')+i) + " : " + str(j) +\
                       '\n\nExpected ' + str(self.type[i]) + ', Recieved "' +\
                       str(test[i]) + '"'
            return "\tCell " + chr(ord('A')+j) + " : " + str(i) +\
                   '\n\nExpected ' + str(self.type[i][j]) + ', Recieved "'+\
                   str(test[i][j]) + '"'
                   
    def get_widget_value(self):
        """returns the value for the widget
        for lists it *assumes* it is correct because lists are checked later
        
        files are automatically flushed at this step
        """
        if self.type == 'label':
            return None
        try: #string
            return self.entry.get()
        except AttributeError:
            if self.type == bool:
                return self.boolstatus
            elif type(self.type) == list:
                return self.out
        raise AttributeError
        
                
    def set_widget_value(self, value=None):
        """
        Set the value of the widget
        """
        if value == None: #Nothing to set
            return
        try:
            if self.type==str: #Tkinter Entry widget:
                self.out=value
                self.entry.delete(0,tkinter.END)#Delete content
                self.entry.insert(0,self.out)
            elif self.type==dict: #Tkinter OptionMenu widget:
                invdict=dict((str(v), k) for k, v in self.default.items())
                self.out=value
                self.dict_var.set(invdict[self.out])
            elif self.type==bool:
                self.out=value
                if value:
                    self.entry.select()
                else:
                    self.entry.deselect()
            elif self.withinrange(value):
                self.out=value
                if hasattr(self.entry_special,'keys') and 'text' in self.entry_special.keys():
                    self.entry_special['keys']=self.out
                print(self.entry)
                self.entry.set(self.out)
            self.parser.update()
            return
        except Exception: pass
        tkMessageBox.showerror(message="Value Error for Variable: " + 
                                        self.name + "\nExpected value from:\n" +
                                        self.getrange() + '\nWith type: ' + 
                                        str(self.type), title="Value Error")

        
    def getrange(self):
        """Returns a string of the range available and adjusts for the variable
        type.
        type=bool -> 'NONE'
        type=str  -> 'NONE'
        type=file -> 'NONE'
        type=int  -> <int> : <int>
        type=float -> <float> : <float>
        
        for integers and floats it converts None to +/- infinity
        """
        tmp = self.range
        if tmp[0] == None:
            tmp = ('-Infinity', tmp[1])
        if tmp[1] == None:
            tmp = (tmp[0], 'Infinity')
        if self.type == float or self.type == int:
            return str(tmp[0]) + ' to ' + str(tmp[1])
        else:
            return 'NONE'

    def __call__(self):
        """<Parameter>() is returned as self.out
        """
        return self.out

    def __str__(self):
        """This is a debug tool
        """
        return "%s (%s): %s" % (self.name, self.type, str(self.out))

def _show_list_window(param):
    """Creates a GUI window for a param type list
    """
    global persistant
    persistant = False
    def destroy(event=None):
        """Collects data & destroys the popup window """
        curr = 0
        for i in range(len(param.out)):
            if type(param.out[i]) == list:
                for j in range(len(param.out[i])):
                    param.out[i][j] = param.type[i][j](boxes[curr].get())
                    curr += 1
            else:
                param.out[i] = boxes[curr].get()
                curr += 1
        param.parser.update()
        if not persistant:
            cancel()
    def cancel(event=None):
        """Simply closes the box without saving the values
        """
        tmptop.destroy()
        tmpwindow.destroy()

    tmpwindow = tkinter.Tk()
    tmpwindow.withdraw()
    tmptop = tkinter.Toplevel(tmpwindow)
    tmptop.title(param.name)
    param.out = param.default
    boxes = []
    for i in range(len(param.default)):
        if type(param.default[i]) == list:
            for j in range(len(param.out[i])):
                tkinter.Label(tmptop, text=chr(ord('A')+i)).grid(row=0, 
                                                                column=i+1)
                tkinter.Label(tmptop, text=str(j)).grid(row=j+1, column=0)
                boxes.append( tkinter.Entry(tmptop) )
                boxes[-1].insert(0, param.out[i][j])
                boxes[-1].grid(row=i+1, column=j+1)
        else:
            tkinter.Label(tmptop, text=chr(ord('A')+i)).grid(row=0, 
                                                             column=i+1)
            boxes.append(tkinter.Entry(tmptop))
            boxes[-1].insert(0, param.out[i])
            boxes[-1].grid(row=1, column=i+1)
            tkinter.Label(tmptop, text='0').grid(row=1, column=0)
    def swap():
        global persistant
        persistant = not persistant
    c_box = tkinter.Checkbutton(tmptop, command=swap, 
text="Persistent")
    c_box.grid(row=len(param.default)+1, column=len(param.default[0]) )
    
    u_button = tkinter.Button(tmptop, text='Update', 
                   command=destroy)
    u_button.grid(row=len(param.default)+1, column=0, 
                    columnspan=len(param.default[0]))
    u_button.bind('<Return>', destroy)
    c_button = tkinter.Button(tmptop, text='Cancel',
                   command=cancel)
    c_button.grid(row=len(param.default)+1,
                  column=1+len(param.default[0])/2)
    c_button.bind('<Return>', cancel)

        
