#!/usr/bin/env python
"""VKMLgui.py
""" 
 # ###################################################################
 #  FILE: "VKMLgui.py" 
 #
 #  Author: Alex Bartol <nanohub@alexbartol.com>
 #       Copyright 2009
 #
 # 
 # VKMLgui.py is a utility to allow for user input on the fly with a simple
 # understandable GUI or on the command line.
 #
 ## Variable types supported : integer, float, string, boolean, list, tuple, 
 ##                             file
 #
 # Module's graphical user mode can be used by using the --gui flag 
 # No flag is makes the program start run the callback with defaults and close
 #
 # when a parameter is created and given a default value, if the program was
 # run with that variable inputed on command line (--variable=12) then the 
 # default value given will be overriden by the commmand line argument
 # ###################################################################
 #


import inspect, time
from sys import argv as ARGS
from sys import stdout as stdout
from copy import deepcopy
from threading import Thread
import sys

from VKML.gui.tk.Parameter import Parameter
from VKML.gui.tk.Menu import Menu
from VKML.gui.tk.Gui import _GetParams


def RunDualfoilHelp():
	#For ordering parameters

	print '\033[1m'+'-------------------------------------------------\
	\nTo pass in a new value for a parameter, type:\
	\n"python dualfoil.py '+'\033[0m'+'--'+'\033[1m'+'parameter=X"\
	\nwhere X is the desired value for that parameter.\
	\n-------------------------------------------------'
	
	
	#AND_OPT = ('MCMB 2528 graphite (Bellcore)','Carbon (petroleum coke)',\
	              #'Lithium foil', 'TiS2', 'Tungsten oxide',\
	              #'Lonza KS6 graphite', 'Albertus MH (Use for NiMH)')
	#(3, 2, 1, 4, 5, 6, 7)
	
	print '\033[1m'+'------Anode Material Properties------'+'\033[0m'
	
	print '\
	\nanode_material:\
	\n		1 for Lithium foil\
	\n		2 for Carbon (petroleum coke)\
	\n		3 for MCMB 2528 graphite (Bellcore)\
	\n		4 for TiS2\
	\n		5 for Tungsten oxide\
	\n		6 for Lonza KS6 graphite\
	\n		7 for Albertus MH (Use for NiMH)\
	\nanode_film_resistance: Anode film resistance (Ohm-m^2)\
	\nanode_capacity=: Anode coulombic capacity (mAh/g)\
	\nanode_capacitance: Anode insertion material capacitance (F/m^2)\
	\nanode_insertion_density: Anode insertion material density (kg/m^3)\
	\nanode_collector_density\n: Anode current collector material density (kg/m^3)'
	
	
	print '\033[1m'+'------Anode Geometric Parameters------'+'\033[0m'
	
	print '\
	\nanode_thickness: Anode thickness (microns)\
	\nanode_collector_thickness: Anode current collector thickness (microns)\
	\nanode_stoich_parameter: Anode initial stoichiometric parameter (0<x<1)\
	\nanode_particle_radius: Anode particle radius (meters)\
	\nanode_electrolyte_volfrac: Volume fraction of electrolyte in anode\
	\nanode_polymer_volfrac: Volume fraction of polymer in anode\
	\nanode_filler_volfrac: Volume fraction of filler in anode\
	\nanode_gas_volfrac: Volume fraction of gas in anode\n'
	
	
	#Parameters for 'Anode Transport Parameters'
	#MVDC1_OPT = ('No', 'Yes')
	
	
	print '\033[1m'+'------Anode Transport Parameters------'+'\033[0m'
	
	print '\
	\nanode_diff_coef: Diffusion coefficient for negative material (m^2/s)\
	\nanode_vary_diff: Flag for allowing variable diffusion in anode (0=no, 1=yes)\
	\nanode_matrix_conductivity: Conductivity of negative matrix (S/m)\
	\nanode_bulk_rate: Reaction rate of bulk negative material\
	\nanode_rate_side1: Rate of anode side reaction 1\
	\nanode_rate_side2: Rate of anode side reaction 2\
	\nanode_rate_side3: Rate of anode side reaction 3\n'
	
	#Parameters for 'Separator Physical Parameters'
	
	SEP_OPT = ('LiPF6 in EC/DMC and p(VdF-HFP) (Bellcore)',\
	              'Perchlorate in PEO', 'Sodium Triflate in PEO',\
	              'LiPF6 in PC (Sony cell simulation)', \
	              'Perchlorate in PC (West simulation)', 'Triflate in PEO', \
	              'AsF6 in methyl acetate', \
	              'Ideal ion exchange membrane', \
	              'TFSI in PEMO at 40 C (oxymethylene-linked PEO) (LBL)', \
	              'LiPF6 in EC:DMC (liquid)', 'LiTFSI in PEO at 85 C (LBL)', \
	              'Paxton 30% KOH in H2O')
	#(7, 2, 3, 4, 5, 6, 1, 9, 10, 11, 12, 13)
	
	print '\033[1m'+'------Separator Physical Parameters------'+'\033[0m'
	
	print '\
	\nsep_material:\
	\n		1 for AsF6 in methyl acetate\
	\n		2 for Perchlorate in PEO\
	\n		3 for Sodium Triflate in PEO\
	\n		4 for LiPF6 in PC (Sony cell simulation)\
	\n		5 for Perchlorate in PC (West simulation)\
	\n		6 for Triflate in PEO\
	\n		7 for LiPF6 in EC/DMC and p(VdF-HFP) (Bellcore)\
	\n		9 for Ideal ion exchange membrane\
	\n		10 for TFSI in PEMO at 40 C (oxymethylene-linked PEO) (LBL)\
	\n		11 for LiPF6 in EC:DMC (liquid)\
	\n		12 for LiTFSI in PEO at 85 C (LBL)\
	\n		13 for Paxton 30% KOH in H2O\
	\nsep_thickness: Separator thickness (microns)\
	\nsep_density: Separator material density (kg/m^3)\
	\nsep_electrolyte_volfrac: Volume fraction of electrolyte in separator\
	\nelectrolyte_density: Electrolyte density (kg/m^3)\
	\nsep_polymer_volfrac: Volume fraction of polymer in separator\
	\npolymer_density: Polymer density (kg/m^3)\
	\nfiller_density: Inert filler density (kg/m^3)\
	\nsep_gas_volfrac: Volume fraction of gas in separator\n'
	
	
	#Parameters for 'Cathode Material Properties'
	
	CAT_OPT = ('LixMn2O4 (Bellcore)',\
	              'LiyNaCoO2 P2 phase (0.3<y<0.92)', \
	              'LiyMn2O4 Spinel (lower plateau)',\
	              'LiyMn2O4 Spinel (upper plateau)', \
	              'LixWO3 (0<x<0.67)', \
	              'LiyCoO2 (0.5 < y < 0.99)', \
	              'LiyV2O5 (0 < y < 0.95)', \
	              'LiyNi0.8Co0.2O2 Gen-1 (0.4 < y < 0.99)', \
	              'TiS2 (for use with Li foil)', \
	              'LiyV6O13 (0.05 < y < 1.0)', \
	              'LiyAl0.2Mn1.8O4F0.2 Bellcore doped spinel (0.21 < y < 1.0)', \
	              'Albertus NiOOH (Use for NiMH)')
	
	print '\033[1m'+'------Cathode Material Properties------'+'\033[0m'
	
	
	print '\
	\ncathode_material:\
	\ncathode_film_resistance: Cathode film resistance (Ohm-m^2)\
	\ncathode_capacity: Cathode coulombic capacity (mAh/g)\
	\ncathode_capacitance: Cathode insertion material capacitance (F/m^2)\
	\ncathode_insertion_density: Cathode insertion material density (kg/m^3)\
	\ncathode_collector_density: Cathode current collector material density (kg/m^3)\n'
	
	
	print '\033[1m'+'------Cathode Spatial Parameters------'+'\033[0m'
	
	
	print '\
	\ncathode_thickness: Cathode thickness (microns)\
	\ncathode_collector_thickness: Cathode current collector thickness (microns)\
	\ncathode_stoich_parameter: Cathode initial stoichiometric parameter (0<x<1)\
	\ncathode_particle_radius: Cathode particle radius (meters)\
	\ncathode_electrolyte_volfrac: Volume fraction of electrolyte in cathode\
	\ncathode_polymer_volfrac: Volume fraction of polymer in cathode\
	\ncathode_filler_volfrac: Volume fraction of inert filler in cathode\
	\ncathode_gas_volfrac: Volume fraction of gas in cathode\n'
	
	
	print '\033[1m'+'------Cathode Transport Parameters------'+'\033[0m'
	MVDC3_OPT = ('No', 'Yes')
	
	print '\
	\ncathode_diff_coef: Diffusion coefficient for positive material (m^2/s)\
	\ncathode_vary_diff: Flag for allowing variable diffusion in cathode (0=no, 1=yes)\
	\ncathode_matrix_conductivity: Conductivity of positive matrix (S/m)\
	\ncathode_bulk_rate: Reaction rate of bulk positive material\
	\ncathode_rate_side1: Rate of cathode side reaction 1\
	\ncathode_rate_side2: Rate of cathode side reaction 2\
	\ncathode_rate_side3: Rate of cathode side reaction 3\n'
	
	
	
	print '\033[1m'+'------Initial Conditions------'+'\033[0m'
	
	print '\
	\nbattery_temp: Initial battery temperature (K)\
	\ninitial_salt_conc: Initial salt concentration (mol/m^3)\
	\nambient_air_temp: Ambient air temperature (K)\
	\nsystem_heat_capacity: Heat capacity of the system (J/kg-K)\
	\ncells_in_stack: Number of cells in a cell stack\n'
	
	#Parameters for 'Initial Conditions (Cont.)'
	
	##ELECTROLYTE CHEMISTRY DROPDOWN OPTIONS
	ELEC_OPT = ('Uniform distribution', 'Electrolyte in separator only')
	##IMPEDANCE DROPDOWN OPTIONS
	IMP_OPT = ('No Impedance', 'Impedance')
	##HEAT TRANSFER DROPDOWN OPTIONS
	HT_OPT = ('Use coefficient below', 'Calculate real-time coefficient',\
	              'Isothermal')
	##SIDE REACTION DROPDOWN OPTIONS
	NSIDE_OPT = ('No', 'Yes')
	
	print '\033[1m'+'------Initial Conditions (Cont.)------'+'\033[0m'
	
	print '\
	\nheat_transfer_setting: 0 uses heat transfer coef., 1 calculates it,  2 isothermal\
	\nheat_transfer_end: Heat transfer coef. at ends (W/m^2-K)\
	\nelectrolyte_distribution: 0 for electrolyte in sep. only, 1 for uniform\
	\nimpedance: 0 for no impedance, 1 for impedance\
	\nside_reaction_flag: Flag to turn on (1) or off (0) side reactions\n'
	
	print '\033[1m'+'------Boundary Conditions------'+'\033[0m'
	
	##SEGMENT MODE DROPDOWN OPTIONS
	MODE_OPT = ('Galvanostatic to a cutoff potential (in A/m2)', 'Galvanostatic for given time (in A/m2)',\
	              'Potentiostatic (in V)',\
	              'Galvanostatic with tapered current after cutoff potential (in A/m2)',\
	              'Specified power (in W/m2)', 'Specified load (in Ohm-m2)')
	
	print '\
	\nsegment_mode:\
	\n		0 for potentiostatic (in V)\
	\n		1 for Galvanostatic for given time (in A/m2)\
	\n		2 for Galvanostatic to a cutoff potential (in A/m2)\
	\n		-1 for Galvanostatic with tapered current after cutoff potential (in A/m2)\
	\n		-2 for Specified power (in W/m2)\
	\n		-3 for Specified load (in Ohm-m2)\
	\ncurrent_density: Varies depending on segment mode. Default is current density.\
	\n		Current density (A/m^2) for galvanostatic modes\
	\n		Potential (V) for potentiostatic mode\
	\n		Power (W/m^2) for specified power mode\
	\n		Load (Ohm-m^2) for specified load mode\
	\ncurrent_changes: Number of current changes during charge/discharge\
	\ncutoff_condition: Simulation time (min) OR potential cutoff (V)\
	\nlow_voltage_cutoff: Low vaoltage cutoff (V)\
	\nhigh_voltage_cutoff: High voltage cutoff (V)\
	\ninternal_resistance: Internal resistance (Ohm-m^2)\n'
	
	
	
	
	print '\033[1m'+'------Solver and Numerical Parameters------'+'\033[0m'
	
	
	##POWER PEAK DROPDOWN OPTIONS
	PP_OPT = ('Exclude power peaks', 'Include power peaks')
	
	print '\
	\niteration_limit: Limit on number of iterations during calculation\
	\nmax_timestep_size: Maximum time step size (s)\
	\nanode_node_count: Number of nodes in negative electrode\
	\nseparator_node_count: Number of nodes in separator\
	\ncathode_node_count: Number of nodes in positive electrode\
	\nparticle_node_count: Number of nodes in solid particle\
	\nconverge_condition: Number of iterations required for solid phase convergence\
	\npower_peaks: 0 for no power peaks, 1 for power peaks\n'
	
	
	
	print '\033[1m'+'------Activation Energy------'+'\033[0m'
	
	print'\
	\nEbarS1: Solid state diffusion in anode (J/mol)\
	\nEbarS3: Solid state diffusion in cathode (J/mol)\
	\nEbarkap: Electrolyte conductivity (J/mol)\
	\nEbarD: Electrolyte diffusion (J/mol)\
	\nEbarka: Anode kinetics (J/mol)\
	\nEbarkc: Cathode kinetics (J/mol)\
	\nEbarks1a: Negative O2 side reaction (J/mol)\
	\nEbarks1c: Positive O2 side reaction (J/mol)\
	\nEbarks2a: Evol. H2 side reaction (J/mol)\
	\nEbarks2c: Recombination H2 side reaction (J/mol)\
	\nEbarks3a: Negative shuttle side reaction (J/mol)\
	\nEbarks3c: Positive shuttle side reactions (J/mol)\
	\nEbarr1: Anode film resistance (J/mol)\
	\nEbarr3: Cathode film resistance (J/mol)\n'
	
	              
	              
	              
	print '\033[1m'+'------Scheduled Output------'+'\033[0m'
	
	print '\
	\ndirectory: The directory in which the output will be generated\
	\nnode_freq: Save every ith node where i=node_freq\
	\ntime_step_freq: Save every nth time step where n=time_step_freq\n'


def RunVisualizeHelp():
	print 'visualize help info'

class Parser:
    """ Parser is designed to be an easy way to get input from the typical
    user. Instead of relying on the user being able to edit hard-coded
    variables or remembering verbose command line arguments, this class 
    generates a GUI on the fly for the user (or asks for variables
    on the command-line)
    """
    ON = 1
    OFF = -1
    AUTO = 0
    def __init__(self, title='', interactive=ON, update_text='Update', **kwargs):
        """Starts a new Parser
        title is the desired title for the GUI window
        interactive modes are (ON, OFF, and AUTO)
        **kwargs - are potential callback functions
        """
        self.update_text = update_text
        self.params = []
        self.tabs = []
        self.gui_title = title
        self.interactive = interactive
        self.functions = []
        self.pre_functions = []
        self.post_functions = []
        self.ask_quit = True
        self.log = None
        self.log_on = False
        self.text = ''
        self.credits2 = ''
        for arg in kwargs:
            print arg
            if type(arg) == function:
                self.add_command(arg)

    def __call__(self):
        """More versitility
        """
        self.run()
        
    def set_credits(self, credits):
        """This is designed to allow the programmer to set the About menu item
         to include his credits in addition to mine
        """
        self.credits2 = credits
        
    def add(self, param):
        """ This function adds a variable to the parser.
        First argument must be a type of Parameter
        """
        self.params.append(param)

    def add_menu(self, menu):
        """This function adds an entire Menu into the parser
        First argument must be a type of Menu
        """
        self.tabs.append(menu)
        for param in menu.params:
            self.params.append(param)
        
    def add_pre_command(self, function):
        """Adds a command to be done FIRST and never to be repeated
        """
        kwargs = {}
        
        variables = inspect.getargspec(function)[0]
        
        for param in self.params:
            if param.name in variables:
                kwargs[param.name] = param
        self.pre_functions.append(self._command(function, kwargs, 
                                                self.interactive))

    def add_post_command(self, function):
        """Adds a command to be done LAST 
        (right before exit and not before then)
        """
        kwargs = {}
        
        variables = inspect.getargspec(function)[0]
        
        for param in self.params:
            if param.name in variables:
                kwargs[param.name] = param
        self.post_functions.append(self._command(function, kwargs,
                                 interactive=self.interactive))
        
    def run_post_commands(self):
        """runs all the commands designated to be done after the simulation
        takes place
        """
        for func in self.post_functions:
            func(forced=True)
    
    def run_pre_commands(self):
        """runs all of the commands designated to be done before the simulation
        takes place
        """
        for func in self.pre_functions:
            func(forced=True)
        
    def init_auto_mode(self):
        """checks for threashold timing (also runs the normal commands for the
        first time)
        """
        if self.interactive > self.OFF:
            for func in self.functions:
                func.init_call()
            
    def add_command(self, function):
        """function - The callback function
        
        This function determins which parameters are used and creates the 
        callback class accordingly
        """
        kwargs = {}
        
        #print str(len(self.params)) + " Number of args"
        variables = inspect.getargspec(function)[0]
        if inspect.getargspec(function)[2] == 'kwargs':
            for param in self.params:
                if param.type != 'label' and param.type != 'image':
                    kwargs[param.name] = param
                    #print param.name
        else:
            for param in self.params:
                if param.name in variables and param.type != 'label':
                    kwargs[param.name] = param
        
        self.functions.append(self._command(function, kwargs, self.interactive))
       

    def is_gui_mode(self):
        """Returns True/False if the mode is creating a gui or not
        """
        return '--gui' in sys.argv

    def is_text_mode(self):
        """Returns True/False if the mode is text based (no gui)
        """
        return not is_gui_mode(self)

    def get_mode(self):
        """Returns the string gui/text depending on mode
        """
        if self.is_gui_mode():
            return 'gui'
        return 'text'

    def set_mode(self, mode):
        """sets the mode if the mode is the string 'gui'/'text'
        """
        if mode.lower() == 'gui':
            sys.argv.append('--gui')
        if mode.lower() == 'text':
            while '--gui' in sys.argv:
                sys.argv.remove('--gui')

    def update(self, forced=False):
        """Calls the callback for all the functions available
        """
        for func in self.functions:
            func.update(forced=forced)
            
    def update_button(self):
        """This overrides the interactive mode because the button should force 
        an update
        """
        for func in self.functions:
            func()
            
    def __delete_duplicates__(self):
        """Steps through the parser and removes all duplicate entries
        """
        length = len(self.params)
        for i in range(length-1):
            for j in range(i+1, length):
                if i < length and j < length and self.params[i].name == self.params[j].name:
                    del self.params[j]
                    length-=1
        
    
    def run(self):
        """ Starts the GUI, if gui is unavaliable or unwanted, it will start
        asking for commands on the command line instead
        """
        #determines parameters from command line arguments
        self.__delete_duplicates__()
        gui = False
        interactive = True
        command_line = False
        self.run_pre_commands()
        for arg in ARGS:
            if arg.lower() == '--gui':
                gui = True
            elif arg.lower() == '--quit':
                self.ask_quit = False
            elif arg.startswith('--help'):
				if ARGS[0]=='dualfoil.py':
					RunDualfoilHelp()
					sys.exit()
				elif ARGS[0]=='visualize.py':
					RunVisualizeHelp()
				sys.exit()
            elif arg.startswith('--') and '=' in arg:
                arg = arg[2:]
                name = arg.split('=')[0]
                value = arg.split('=')[-1]
                for param in self.params:
                    if name == param.name:
                        if param.type == float or param.type == int or param.type == str:
                            param.default = param.type(value)
                            param.out = param.default
                        if param.type == file:
                            param.filename = value
                            if param.filetype.startswith('o'):
                                param.out = open(param.filename, 'r')
                            elif param.filetype.startswith('s'):
                                param.out = open(param.filename, 'w')
                            else: #direcotry
                                param.out = param.filename
                        if type(param.type) == list:
                            def makeList(ls):
                                #print ls
                                if ls.count('[') == 1 and ls.count(']') == 1:
                                    ls = ls.replace('[', '').replace(']', '')
                                    rtn = ls.split(',')
                                    for i in range(len(rtn)):
                                        try:
                                            rtn[i] = int(rtn[i])
                                        except:
                                            try:
                                                rtn[i] = float(rtn[i])
                                            except:
                                                pass
                                    return rtn
                                bc = 0
                                rtn = []
                                for i in range(len(ls)):
                                    if ls[i] == '[':
                                        bc += 1
                                    if ls[i] == ']':
                                        bc -= 1
                                    if ls[i] == ',' and bc == 1:
                                       # print 'tick'
                                        ls = ls[:i] + '`' + ls[i+1:]
                                if bc != 0:
                                    print 'Incorrect format for type List'
                                    sys.exit()
                                ls = ls[1:]
                                ls = ls[:-1]
                                for i in ls.split('`'):
                                    rtn.append(makeList(i))
                                return rtn
                                
                            out = makeList(value)
                            param.out, param.default = out, out
        if gui:
            self.init_auto_mode()
            gui = _GetParams(self.tabs, parser=self, credits=self.credits2, title=self.gui_title, update_text=self.update_text)
            gui.get_result()
        else:
            #calls callback function before returning
            self.update(forced=True)
            return
            
    class _command:
        """Internal class designed to handle all callback functions
        """
        def __init__(self, func, kwargs, interactive):
            """func is the function that needs to be called
            kwargs is the dictionary that holds the the parameters
            interactive is the variable that states how often this should be updated 
            """
            self.f = func
            self.kwargs = kwargs
            self.last = {}
            self.interactive = interactive
            self.wid = -1
            self.time_threashold = 100
            self.last_time = 0
            self.asked = False
            self.out = None
            self.duration = 0
            for arg in self.kwargs.items():
                self.last[arg[0]] = arg[1]
           
        def update(self, forced=False):
            """Checks what mode it is currently in and runs functions 
            accordingly
            """
            if forced:
                self.force_run()
                return
            if self.interactive == Parser.ON or \
                    (self.interactive == Parser.AUTO and \
                    self.duration < self.time_threashold):
				self()
		#self.start()
            elif self.duration >= self.time_threashold and not self.asked:
                self.asked = True
                self.interactive = False      
                    
        def set_last(self):
            """Records the previous values
            """
            for item in self.kwargs:
                if not self.kwargs[item].type == file:
                    #print self.last[item]()
                    self.last[item] = deepcopy(self.kwargs[item]())
                else: #FILE
                    self.last[item] = self.kwargs[item]()
                #print self.last[item]
                                
        def changed(self):
            """checks if there is a change, if change occurs returns True 
            """
            rtn = False
            for item in self.kwargs:
                if self.kwargs[item]() == self.last[item]:
                    continue
                else:
                    
                    self.set_last()
                    rtn = True
            self.set_last
            #self.update()
            return rtn
        
        def init_call(self): 
            """Calls the function (to start the gui in some cases), in order
            to establish a time that the simulation will take. 
            """
            self.changed() #needed to set self.last
            start_time = time.time()
            self.out = self.f(**self.last)
            self.duration = time.time() - start_time
            
        def run(self):
            self()
        
        def force_run(self):
            self(forced=True)
            
        def __call__(self, forced=False):
            """calls the function with arguments
            """
            if self.changed() or forced:
                self.out = self.f(**self.last)
                return self.out
                                                       
if __name__ == '__main__':
    """The following code is only a sample/test case for my software
    """
    P = Parser(title='Sample GUI', interactive=-1)
    
    t1 = Menu(title='tab1', parser=P)
    t2 = Menu(title='tab2', parser=P)
 
    def strfunc(**kwargs):
        for arg in kwargs:
            print kwargs[arg]

    Parameter(name='string', menu=t1, default='text goes here', variable=str)
    Parameter(name='matrix1', menu=t2, default=[[1,2,3],[1,2,3],[1,2,3]], variable=list)
    Parameter(name='integer1', menu=t2, default=10, variable=int, 
                interval=(-100, 100))
    
    Parameter(name='bool1', default=False, menu=t1, variable=bool)

    P.add_command(strfunc)
                                        
    P()
    
    
