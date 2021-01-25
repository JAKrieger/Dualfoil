"""Menu.py
"""
 # ############################################################################
 # FILE: Menu.py
 #
 #
 #  Author: Alex Bartol <nanohub@alexbartol.com>
 #       Copyright 2009
 #  Author: Jonas A. Krieger <econversion@empa.ch>
 #       Copyright 2021
 #
 # 
  
import tkinter

class Menu:
    """Menu is a class that holds parameters
    
    The Menu class should be used to organize <Parameter>s in any way the user
    see's fit
    """
    def __init__(self, parser, title='New Tab', update_button=True,disabled=False,scrollable=False):
        """The <Menu> needs the parser because it automatically adds itself to
        it.
        
        parser - the parser the program is using
        title - the desired title for the Menu
        """
        self.update_button=update_button
        self.Parser = parser
        self.title = title
        self.disabled =disabled
        self.scrollable=scrollable
        self.params = []
        self.entries = []
        self.labels = []
        self.Parser.add_tab(self)
        self.top=None #keep track of which should be the top object.

    def add(self, param):
        """This function adds param to the Menu
        
        param - a <Parameter> type
        """
        self.params.append(param)
        self.Parser.params.append(param)
        
    def remove(self, param):
        """This function removes param to the Menu
        
        param - a <Parameter> type
        """
        if param in self.params:
            self.params.remove(param)
        if param in self.Parser.params:
            self.Parser.params.remove(param)
            
    def clear(self):
        """Resets the menu, removing all parameters contained insides
        """
        self.hide()
        for param in self.params:self.remove(param)
        self.params = []
        
        
    def show(self, top=None):
        """This function shows this Menu
        
        The Menu can be either shown or hidden depending on the user's current
        selection
        """
        if top!=None:
            self.top=top
        if not len(self.params):return -1
        
        for i, param in enumerate(self.params):
            label=param.get_Label(self.top,row=i+3, column=0)
            self.labels.append(label)
            self.entries.append(param.get_widget(self.top, row_number=i+3))
        if self.update_button:
	        return i+1
        return -1
        
    def hide(self):
        """This function hides the menu from the GUI
        
        Hiding a menu effectively temporarily destorys each parameter widget
        """
        for e in self.entries:
            e.destroy()
        for l in self.labels:
            l.destroy()
        for p in self.params:
            p.kill_special()
        self.entries = []
        self.labels = []
    

class DropDownMenu:
    """Menu is a class that holds parameters
    
    The Menu class should be used to organize Tkinter menus in any way the user
    see's fit
    """
    def __init__(self, parser, title='New Menu'):
        """The <Menu> needs the parser because it automatically adds itself to
        it.
        
        parser - the parser the program is using
        title - the desired title for the Menu
        """
        self.Parser = parser
        self.title = title
        self.functions = []
        self.labels = []
        self.Parser.add_menu(self)

    def add(self, func=None,label=''):
        """This function adds func to the Menu
        
        func - a function type
        """
        if func !=None:
            self.functions.append(func)
            self.labels.append(label)