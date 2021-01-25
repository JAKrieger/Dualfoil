"""Gui.py
"""
 # ############################################################################
 # FILE: Gui.py
 #
 #
 #  Author: Alex Bartol <nanohub@alexbartol.com>
 #       Copyright 2009
 #  Author: Jonas A. Krieger <econversion@empa.ch>
 #       Copyright 2021
 #
 # ############################################################################
 
import tkinter
import tkinter.messagebox as tkMessageBox
from tkinter import ttk 
import sys,os
import inspect

class _GetParams:
    """GetParams takes in a list of variables that it puts into GUI form
    The class only modifies the <Parameter>.out variable
    """
    def __init__(self, menus, parser, credits='', title='', update_text='Update'):
        """initializes variables and starts the GUI window
        
        Initialization Information:
        __init__(self, )
       
        menus - a list of type Menu that should be in the GUI
        parser - the parser that the program is using
        title - a string that will be the title bar for the GUI
        """
        self.results = []
        
        self.args = []
        self.update_text = update_text
        self.credits = credits
        for arg in self.args:
            self.results.append(arg.out)
        self.top = tkinter.Tk()
        self.tabs = menus
        self.parser = parser
        self.entries = [] #the list of gui text boxes
        #set style
        style = ttk.Style(self.top)
        if sys.platform=='win32':
               
            #Set the main icon (https://stackoverflow.com/questions/9929479/embed-icon-in-python-script )
            main_icon='main_icon.ico'
            if not hasattr(sys, "frozen"):
                main_icon='../../../main_icon.ico'
                main_icon = os.path.join(os.path.dirname(__file__), main_icon) 
            else:  
                main_icon = os.path.join(sys.prefix, main_icon)
            self.top.iconbitmap(main_icon)
            style.theme_use('winnative')
        elif sys.platform=='linux':   
            style.theme_use('classic')
        self.title = title
        if len(menus) == 1:
            self.top.title(self.title)
        else:
            try:
                self.top.title(self.title) #sets title
       	    except IndexError:
       	        self.top.title(self.title)
        self.boolstatus = [] #keeps track of boolean values
        
        self._setup_menubar()
        self._setup_gui()
        
        
        
    def _setup_menubar(self):
        """Creates the Menubar and Tabsbar and adds them to the GUI
        """
        
        self.menubar = tkinter.Menu(self.top)
        
        for menu in self.parser.menus:
            curr_menu=tkinter.Menu(self.menubar, tearoff=0)
            if len(menu.labels)!=1:
                for j in range(len(menu.labels)):
                    func=menu.functions[j]
                    kwargs = {}
                    variables = inspect.getargspec(func)[0]
                    if inspect.getargspec(func)[2] == 'kwargs':
                        for param in self.parser.params:
                            if param.type != 'label':
                                kwargs[param.name] = param
                    else:
                        for param in self.parser.params:
                            if param.name in variables and \
                                    param.type != 'label' and \
                                    param.type != 'function':
                                kwargs[param.name] = param
                            
                    f = self.parser._command(func, kwargs, -1)
                    curr_menu.add_command(label=menu.labels[j], command=f.force_run)
                self.menubar.add_cascade(label=menu.title, menu=curr_menu)
            else:
                func=menu.functions[0]
                kwargs = {}
                variables = inspect.getargspec(func)[0]
                if inspect.getargspec(func)[2] == 'kwargs':
                    for param in self.parser.params:
                        if param.type != 'label':
                            kwargs[param.name] = param
                else:
                    for param in self.parser.params:
                        if param.name in variables and \
                                param.type != 'label' and \
                                param.type != 'function':
                            kwargs[param.name] = param
                                
                f = self.parser._command(func, kwargs, -1)
                self.menubar.add_command(label=menu.labels[0], command=f.force_run)
                
            
            
        License="Copyright (c) 2015, Lucas Darby Robinson, R. Edwin García\n\
All rights reserved.\n\
\n\
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:\n\
\n\
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.\n\
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.\n\
Neither the name of the Purdue University nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.\n\
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
        def show_help():
            tkMessageBox.showinfo(title='Help', message='Switch between' +\
            'the tabs to configure the parameters.')
        def show_disclaimer():
            tkMessageBox.showinfo(title='Disclaimer', message='Please note: We have slightly modified the fortran code of dualfoil.f to ensure numerical stability. But we do not guarantee that the resutls calculated with this GUI are accurate or consistent with the original version of the code.')
        def show_about():
            about=tkinter.Toplevel()
            about.title('About')
            about_text=tkinter.Label(about, text =
            'Dualfoil.f Fortran code by John Newman, see\n'+\
            ' M. Doyle, T. F. Fuller, and  J. Newman, J.  Electrochem.  Soc.,  140  (1993),  1526-1533.\n T. F. Fuller, M. Doyle, and John Newman, J. Electrochem. Soc., 141 (1994), 1-10.\n T.  F.  Fuller,  M.  Doyle,  and  John  Newman,  J.  Electrochem.  Soc.,  141  (1994),  982-990.\n'+\
            'Dualfoil.f copyright John Newman 1998\n\n'+\
            'Dualfoil wrapper created by: Lucas D. Robinson and R. Edwin Garcia.'+\
                             '\nVKML GUI created by: Alex Bartol\nCopyright 2009, Purdue University' + \
                             '\navailable online: https://nanohub.org/tools/dualfoil'+\
                             '\n\nGUI modified by J. A. Krieger, Empa, Laboratory Materials for Energy Conversion 2020\nwww.empa.ch/econversion , econversion@empa.ch \n\n License from nanohub:',justify=tkinter.LEFT) # , font = "30"
            about_text.pack() 
 
            licframe = ttk.Frame(about)
            licframe.pack(padx=10,pady=10)
            licscroll = tkinter.Scrollbar(licframe)
            licscroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            lictext = tkinter.Text(licframe)
            lictext.pack()
            lictext.insert(tkinter.END, License)
            lictext.config(yscrollcommand=licscroll.set)
            licscroll.config(command=lictext.yview)
            
        helpmenu = tkinter.Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label='Help', command=show_help)
        helpmenu.add_command(label='Disclaimer',command=show_disclaimer)
        helpmenu.add_command(label='About', command=show_about)
        self.menubar.add_cascade(label='Help', menu=helpmenu)
        
        self.top.config(menu=self.menubar)
        
        
        #Create Tabs
        style = ttk.Style(self.top)
        style.configure('lefttab.TNotebook', tabposition='wn')
        style.map("lefttab.TNotebook.Tab",foreground=[("disabled","#333333")])
        self.tabsbar = ttk.Notebook(self.top, style='lefttab.TNotebook')
        



        for tab in self.tabs:  
            tabframe = ttk.Frame(self.tabsbar,padding=20) 
            tabframe.pack(fill=tkinter.BOTH,expand=True)
            
            if tab.scrollable:
                self.tabsbar.add(tabframe, text=tab.title) 
                canvas=tkinter.Canvas(tabframe)#,height=self.top.winfo_screenheight()/3
                scroll=tkinter.Scrollbar(tabframe,command=canvas.yview)
                canvas.config(yscrollcommand=scroll.set)
                canvas.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)
                scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y,expand=False)
                scrollframe=ttk.Frame(canvas)
                canvaswindow=canvas.create_window(0,0,window=scrollframe,anchor=tkinter.CENTER)
                #Ensure proper resizing:
                def onScrollFrameConfig(event):
                    canvas.configure(scrollregion=canvas.bbox("all"))
                    canvas.yview_moveto(0)
                scrollframe.bind("<Configure>",onScrollFrameConfig)
                tab.show(scrollframe)
            else:
                self.tabsbar.add(tabframe, text=tab.title,sticky=tkinter.N) 
                tab.show(tabframe)
            if tab.disabled:
                self.tabsbar.tab(len(self.tabsbar.tabs())-1,state='disabled')
            try:
                self.u_button.destroy()
            except:
                pass

        if len(self.tabs) > 1:
#            self.menubar.add_cascade(label='Menus', menu=tabmenu)        
            self.tabsbar.pack(expand = 1, fill ="both")
            #select first tab:
            self.tabsbar.select(self.tabsbar.tabs()[0])

  

    
    def get_result(self):
        """*Waits for the GUI window to close* and sets the value of 
        <Parameter>.out (or <Parameter>() ) to the desired value
        
        All illogical values are set to default
        """
        self.top.mainloop() #wait on window to close
        for i in range(len(self.results)):
            #TODO:
            if type(self.args[i].type) != list:
                if self.args[i].withinrange(self.args[i].type(self.results[i])):
                    self.results[i] = self.args[i].type(self.results[i])
            else:
                self.results[i] = self.args[i].out
        i = 0
        for arg in self.args:
            arg.out = self.results[i]
            i += 1
    
    def _setup_gui(self):
        """sets up the GUI based on the number and name of each
        parameters
        
        NOTE: All variable types are handled uniquely
        """
        

        self.top.bind("<Control-q>", self.close)

        self.boolstatus.append(False) #needed to adjust for label row

    
    def _update(self):
        """This code is run whenever anything changes in the GUI
        
        It forwards the updates to the parser's callback function which runs
        each respective callback function if necessary
        """
        i = 0
        if len(self.results) == 0:
            for arg in self.args:
                self.results.append( arg.type(arg.get_widget_value()) )
        else:
            for i in range(len(self.args)):
                self.results[i] = self.args[i].type(
                                    self.args[i].get_widget_value())
        
        self.parser.update() #runs callbacks
        
    def _update_button(self, e=None):
        """This is used to bypass the interactive mode and force an update
        
        The callback functions are also informed of the update
        """
        i = 0
        if len(self.results) == 0:
            for arg in self.args:
                self.results.append( arg.type(arg.get_widget_value()) )
                print(self.results)
        else:
            for i in range(len(self.args)):
                self.results[i] = self.args[i].type(self.args[i].get_widget_value())  
                print(self.results[i] )                   
        for i,x in enumerate(self.results):
            self.args[i].out = x
        self.parser.update_button() #forces an update on callback functions
        
    def close(self, e=None):
        """This method is run when the GUI should be destroyed
        """
        if self.parser.ask_quit:
            if not tkMessageBox.askyesno(title='Quit Confirmation', 
                                    message='Do you really want to quit?') == 1:
                return
        self.parser.run_post_commands()
        try: #might already be closed
            self.top.destroy()
        except Exception:pass

