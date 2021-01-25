 # ############################################################################
 # FILE: dualfoil.py
 #
 #  Authors: Lucas Darby Robinson, R. Edwin García
 #       Copyright 2015
 #  Author: Jonas A. Krieger <econversion@empa.ch>
 #       Copyright 2021
 # 
 # ############################################################################
#Import VKML tools
from VKML.gui.tk import Parameter, Parser, Menu, DropDownMenu
import time, sys, os
import shutil
import tkinter.messagebox as tkMessageBox
import tkinter as tk

import visualize
	

toolHomeDir = os.path.dirname(os.path.abspath(__file__))

def write_input_file(iteration_limit, anode_thickness, sep_thickness, cathode_thickness, anode_collector_thickness,\
              cathode_collector_thickness, anode_node_count, separator_node_count, cathode_node_count, particle_node_count,\
              anode_vary_diff, cathode_vary_diff, converge_condition, battery_temp,\
              initial_salt_conc, cathode_stoich_parameter, anode_stoich_parameter, max_timestep_size, anode_diff_coef, \
              cathode_diff_coef, anode_particle_radius, cathode_particle_radius, anode_electrolyte_volfrac, anode_polymer_volfrac,\
              anode_filler_volfrac, anode_gas_volfrac, sep_electrolyte_volfrac, sep_polymer_volfrac,\
              sep_gas_volfrac, cathode_electrolyte_volfrac, cathode_polymer_volfrac, cathode_filler_volfrac, cathode_gas_volfrac,\
              anode_matrix_conductivity, cathode_matrix_conductivity, anode_bulk_rate, cathode_bulk_rate, anode_film_resistance,\
              cathode_film_resistance, anode_capacity, cathode_capacity, electrolyte_density, anode_insertion_density,\
              cathode_insertion_density, filler_density, polymer_density, sep_density, anode_collector_density, cathode_collector_density,\
              heat_transfer_end, system_heat_capacity, ambient_air_temp, cells_in_stack, heat_transfer_setting,\
              node_freq, time_step_freq, electrolyte_distribution, impedance,\
              anode_capacitance, cathode_capacitance, power_peaks, side_reaction_flag,\
              anode_rate_side1, cathode_rate_side1, anode_rate_side2, cathode_rate_side2, anode_rate_side3,\
              cathode_rate_side3, anode_material, sep_material, cathode_material, current_changes,\
              current_density, cutoff_condition, segment_mode, low_voltage_cutoff, high_voltage_cutoff, \
              EbarS1, EbarS3, Ebarkap, EbarD,\
              Ebarka, Ebarkc, Ebarks1a, Ebarks1c,\
              Ebarks2a, Ebarks2c, Ebarks3a, Ebarks3c,\
              Ebarr1, Ebarr3, directory, jsol,filename='dualfoil5.in',**kwargs):


	current_density = current_density.replace(" ", "")
	current_density = current_density.split(",")
	cutoff_condition = cutoff_condition.replace(" ", "")
	cutoff_condition = cutoff_condition.split(",")
	low_voltage_cutoff = low_voltage_cutoff.replace(" ", "")
	low_voltage_cutoff = low_voltage_cutoff.split(",")
	high_voltage_cutoff = high_voltage_cutoff.replace(" ", "")
	high_voltage_cutoff = high_voltage_cutoff.split(",")
	segment_mode = segment_mode.replace(" ","")
	segment_mode = segment_mode.split(",")
	
	if int(current_changes) > 1:
		if len(current_density) != int(current_changes):
			tkMessageBox.showinfo(title='Input Error', message='Warning: A total of %s current/load/power \
			values were specified for %s specified current changes.' % (str(len(current_density)), str(int(current_changes)))) 
			sys.exit()
	else: 
		if len(segment_mode) > 1 or len(current_density) > 1 or len(cutoff_condition) > 1 or len(low_voltage_cutoff) > 1 or len(high_voltage_cutoff) > 1:
			tkMessageBox.showinfo(title='Input Error', message='Not enough current changes were specified for multiple sets of boundary conditions.') 
			sys.exit()
            
	il1 = 1  


      
	#CREATE WORKING DIRECTORY FOR THIS RUN
	if sys.platform=='win32':
		if not os.path.isdir('%s'%(directory)):
			os.system('mkdir %s' % (directory))
	else:
		os.system('mkdir -p %s' % (directory))
	time.sleep(.005)
	

	#CREATE LI-ION.IN INPUT FILE
	owd = os.getcwd()
	os.chdir('%s' % directory)
	f = open(filename,'w+')
	VarList = [iteration_limit, anode_thickness, sep_thickness, cathode_thickness, anode_collector_thickness,\
		cathode_collector_thickness, anode_node_count, separator_node_count, cathode_node_count, particle_node_count,\
		anode_vary_diff, cathode_vary_diff, converge_condition, battery_temp,\
		initial_salt_conc, anode_stoich_parameter, cathode_stoich_parameter, max_timestep_size, anode_diff_coef, \
		cathode_diff_coef, anode_particle_radius, cathode_particle_radius, anode_electrolyte_volfrac, anode_polymer_volfrac,\
		anode_filler_volfrac, anode_gas_volfrac, sep_electrolyte_volfrac, sep_polymer_volfrac,\
		sep_gas_volfrac, cathode_electrolyte_volfrac, cathode_polymer_volfrac, cathode_filler_volfrac, cathode_gas_volfrac,\
		anode_matrix_conductivity, cathode_matrix_conductivity, anode_bulk_rate, cathode_bulk_rate, anode_film_resistance,\
		cathode_film_resistance, anode_capacity, cathode_capacity, electrolyte_density, anode_insertion_density,\
		cathode_insertion_density, filler_density, polymer_density, sep_density, anode_collector_density, cathode_collector_density,\
		heat_transfer_end, system_heat_capacity, ambient_air_temp, cells_in_stack, heat_transfer_setting,\
		il1, node_freq, time_step_freq, electrolyte_distribution, impedance,\
		anode_capacitance, cathode_capacitance, power_peaks, jsol, side_reaction_flag,\
		anode_rate_side1, cathode_rate_side1, anode_rate_side2, cathode_rate_side2, anode_rate_side3,\
		cathode_rate_side3, anode_material, sep_material, cathode_material, current_changes]

	SegmentParameters = [current_density, cutoff_condition, segment_mode, low_voltage_cutoff, high_voltage_cutoff]
    
	
	for y in VarList:
		f.write('%s\n' % y)
	if int(current_changes) == 1:
			f.write('%s ' % current_density[0])
			f.write('%s ' % cutoff_condition[0])
			f.write('%s ' % segment_mode[0])
			f.write('%s ' % low_voltage_cutoff[0])
			f.write('%s ' % high_voltage_cutoff[0])
#			f.write('%s' % internal_resistance[0])
	else:
		segment_number = int(current_changes)
		for x in range(0, segment_number):
				try:
					f.write('%s ' % current_density[x])
					f.write('%s ' % cutoff_condition[x])
					f.write('%s ' % segment_mode[x])
					f.write('%s ' % low_voltage_cutoff[x])
					f.write('%s ' % high_voltage_cutoff[x])
					f.write('\n')

				except:
					tkMessageBox.showinfo(title='Input Error', message='For each segment change, you must specify:\n\n' 
					+ 'Segment Mode \nCurrent denisty/Load/Power \nSegment Time/Cutoff Potential \nLow Voltage Cutoff \nHigh Volatge Cutoff \nInternal Resistance')
					sys.exit()
	f.close()
	
	ion_ebar='li-ion-ebar.in'
	if filename !='dualfoil5.in' and filename !='li-ion.in':
		ion_ebar=filename.rstrip('.in')+'-ion.in'
	ebar = open(ion_ebar, 'w+')
	ActList = [EbarS1, EbarS3, Ebarkap, EbarD,\
		Ebarka, Ebarkc, Ebarks1a, Ebarks1c,\
		Ebarks2a, Ebarks2c, Ebarks3a, Ebarks3c,\
		Ebarr1, Ebarr3]
	
	for z in ActList:
		ebar.write('%s\n' % z)
	ebar.close()
	os.chdir(owd)
    
    
def RunSimulation(directory):
	owd = os.getcwd()
	os.chdir('%s' % directory)
	print( 'Now Running Dualfoil...')
	solve_status.entry.config(text='Calculation in progress...')
	solve_status.entry.master.update_idletasks()
	if not hasattr(sys,"frozen"):
		code_dir=os.path.join(toolHomeDir,'dualfoil')
	else:
		code_dir=os.path.join(sys.prefix,'dualfoil')
	if sys.platform=='win32':
		os.system('"%s"' %(os.path.join(code_dir,'dualfoil.exe')))
	if sys.platform=='linux':
		os.system('"%s"' %(os.path.join(code_dir,'dualfoil.o')))
	print( 'Done.')
	solve_status.entry.config(text='Calculation done!')
	solve_status.entry.master.update_idletasks()
	os.chdir(owd)
	visualize.main()


def RunDualfoil(**kwargs):
    '''Write input file and then run simulation'''
    write_input_file(**kwargs)
    directory=kwargs['directory']
    RunSimulation(directory)



#Create functions
    
def Save_Input_As(**kwargs):
    owd = os.getcwd()
    initdir=owd
    try:  
        dir_=directory.get_widget_value()
        os.chdir('%s' % dir_)
        initdir=os.getcwd()
    except Exception: pass
    
    options={}
    options['filetypes'] = [('input files','.in'),('all files','.*')]
    options['initialfile'] = 'dualfoil5.in'
    options['title']='Save input file'
    options['initialdir']= initdir
    filename = tk.filedialog.asksaveasfilename(**options)
    if filename=='':
        os.chdir(owd)
        return #choosing was aborted
    path,file=os.path.split(filename)
    
    kwargs['directory']=path
    write_input_file(filename=file,**kwargs)
    
    os.chdir(owd)
  
       
def choose_cwd():
    options={}
    options['title']='Choose working directory'
    options['initialdir']= os.getcwd()
    dirname = tk.filedialog.askdirectory(**options)
    if dirname=='':return #choosing was aborted
    try:  
        os.chdir('%s' % dirname)
    except Exception: 
        tkMessageBox.showinfo(title='Input Error', message="Error, couldn't change working directory to {} .".format({dirname}))
        return #failed
    select_cwd.label.config(text='{}'.format(os.getcwd()))
    select_cwd.label.master.update_idletasks()
    
 
def Open_Input():
    owd = os.getcwd()
    initdir=owd
    try:  
        dir_=directory.get_widget_value()
        os.chdir('%s' % dir_)
        initdir=os.getcwd()
    except Exception: pass

    
    il1 = None 
    
    VarList = [iteration_limit, anode_thickness, sep_thickness, cathode_thickness, anode_collector_thickness,\
		cathode_collector_thickness, anode_node_count, separator_node_count, cathode_node_count, particle_node_count,\
		anode_vary_diff, cathode_vary_diff, converge_condition, battery_temp,\
		initial_salt_conc, anode_stoich_parameter, cathode_stoich_parameter, max_timestep_size, anode_diff_coef, \
		cathode_diff_coef, anode_particle_radius, cathode_particle_radius, anode_electrolyte_volfrac, anode_polymer_volfrac,\
		anode_filler_volfrac, anode_gas_volfrac, sep_electrolyte_volfrac, sep_polymer_volfrac,\
		sep_gas_volfrac, cathode_electrolyte_volfrac, cathode_polymer_volfrac, cathode_filler_volfrac, cathode_gas_volfrac,\
		anode_matrix_conductivity, cathode_matrix_conductivity, anode_bulk_rate, cathode_bulk_rate, anode_film_resistance,\
		cathode_film_resistance, anode_capacity, cathode_capacity, electrolyte_density, anode_insertion_density,\
		cathode_insertion_density, filler_density, polymer_density, sep_density, anode_collector_density, cathode_collector_density,\
		heat_transfer_end, system_heat_capacity, ambient_air_temp, cells_in_stack, heat_transfer_setting,\
		il1, node_freq, time_step_freq, electrolyte_distribution, impedance,\
		anode_capacitance, cathode_capacitance, power_peaks, jsol, side_reaction_flag,\
		anode_rate_side1, cathode_rate_side1, anode_rate_side2, cathode_rate_side2, anode_rate_side3,\
		cathode_rate_side3, anode_material, sep_material, cathode_material, current_changes]
    SegmentParameters = [current_density, cutoff_condition, segment_mode, low_voltage_cutoff, high_voltage_cutoff]
    ActList = [EbarS1, EbarS3, Ebarkap, EbarD,\
		Ebarka, Ebarkc, Ebarks1a, Ebarks1c,\
		Ebarks2a, Ebarks2c, Ebarks3a, Ebarks3c,\
		Ebarr1, Ebarr3]
    options={}
    options['filetypes'] = [('input files','.in'),('all files','.*')]
    options['initialfile'] = 'dualfoil5.in'
    options['title']='Load input file'
    options['initialdir']= initdir
    filename=tk.filedialog.askopenfilename(**options)
    if filename=='':
        os.chdir(owd)
        return#choosing aborted
    with open(filename,'r') as f:
        lines=f.readlines()
        if len(lines)<30: #Assume this is the li-ion-ebar.in file ..
            for linenumber, line in enumerate(lines):
               if linenumber<len(ActList):
                   Param=ActList[linenumber]
                   if Param==None:continue #parameter unused, e.g. il1
                   Param.set_widget_value(value=line.rstrip('\n'))
        else:#Assume this is the dualfoil5.in file
            segparams=[]
            for linenumber, line in enumerate(lines):
               if linenumber<len(VarList):
                   Param=VarList[linenumber]
                   if Param==None:continue #parameter unused, e.g. il1
                   Param.set_widget_value(value=line.rstrip('\n'))
               elif  linenumber < len(VarList)+int(current_changes.get_widget_value()): #SegmentParameters
                   segparams.append(line.rstrip('\n').rstrip('\t').rstrip(' ').split(' '))
            if len(segparams)>0:
                segparams_parse=segparams[0]
                for j in range(len(segparams_parse)):
                    for i in range(1,len(segparams)):
                        segparams_parse[j]+=','+segparams[i][j]
                    Param=SegmentParameters[j]
                    if Param==None:continue #parameter unused, e.g. il1
                    Param.set_widget_value(value=segparams_parse[j])
                
    os.chdir(owd)
    
 
    
#Create parser
p=Parser(title='Dualfoil Battery Simulation')


#Create Menus:
    
#Filemenu:
mFile=DropDownMenu(title='File', parser=p)
mFile.add(func=lambda **kwargs:Save_Input_As(**kwargs),label='Save As')
mFile.add(func=lambda **kwargs:Open_Input(),label='Load')
mFile.add(func=lambda **kwargs: choose_cwd(),label='Change directory')
mFile.add(func=lambda **kwargs:p.gui.close(),label='Quit')

mVis=DropDownMenu(title='Visualize', parser=p)
mVis.add(func=lambda **kwargs:visualize.main(),label='Visualize')

#Create Tabs
Menu(title=    'Anode                                            ', parser=p,disabled=True)
mAp = Menu(title=    ' - Material Properties                    ', parser=p)
mAs = Menu(title=    ' - Spatial Parameters                    ', parser=p)
mAt = Menu(title=    ' - Transport Parameters                ', parser=p)
Menu(title=    'Separator                                       ', parser=p,disabled=True)
mSep = Menu(title=   ' - Physical Parameters                  ', parser=p)
Menu(title=    'Cathode                                         ', parser=p,disabled=True)
mCp = Menu(title=    ' - Material Properties                    ', parser=p)
mCs = Menu(title=    ' - Spatial Parameters                    ', parser=p)
mCt = Menu(title=    ' - Transport Parameters                ', parser=p)
mIp = Menu(title=    'Initial Conditions                           ', parser=p)
mSs = Menu(title=    'Boundary Conditions                     ', parser=p)
mNp = Menu(title=    'Solver and Numerical Parameters', parser=p)
mEa = Menu(title=    'Activation Energies                       ', parser=p)
mlaunch = Menu(title='Simulation Setup                           ', parser=p)


#PARAMETERS FOR WELCOME MENU

#Parameters for 'Anode Material Properties'

AND_OPT = {'MCMB 2528 graphite (Bellcore)':3,
           'Carbon (petroleum coke)':2,
              'Lithium foil':1,
              'TiS2':4,
              'Tungsten oxide':5,
              'Lonza KS6 graphite':6,
              'Albertus MH (Use for NiMH)':7}
    
 

Parameter(name='', menu=mAp, variable='label')
Parameter(name='Anode Material Properties', menu=mAp, variable='label')
Parameter(name='', menu=mAp, variable='label')
anode_material=Parameter(name='anode_material', display_name='Choose material:', variable=dict,\
              menu=mAp, default=(AND_OPT))
anode_film_resistance=Parameter(name='anode_film_resistance', display_name='Film resistance (Ohm-m2):',\
              variable=str, menu=mAp, default='0.01')
anode_capacity=Parameter(name='anode_capacity', display_name='Coulombic capacity of negative material (mAh/g):',\
              variable=str, menu=mAp, default='372.0')
anode_capacitance=Parameter(name='anode_capacitance', display_name='Capacitance (F/m2):',\
              variable=str, menu=mAp, default='0.0')
anode_insertion_density=Parameter(name='anode_insertion_density', display_name='Density of insertion material (kg/m3):',\
              variable=str, menu=mAp, default='2266.0')
anode_collector_density=Parameter(name='anode_collector_density', display_name='Density of current collector (kg/m3):',\
              variable=str, menu=mAp, default='8954.0')
Parameter(name='', menu=mAp, variable='label')


#Parameters for 'Anode Spacial Parameters'

Parameter(name='', menu=mAs, variable='label')
Parameter(name='Anode Geometric Parameters', menu=mAs, variable='label')
Parameter(name='', menu=mAs, variable='label')
anode_thickness=Parameter(name='anode_thickness', display_name='Thickness (m):', variable=str,\
              menu=mAs, default='100.0e-6')
anode_collector_thickness=Parameter(name='anode_collector_thickness', display_name='Thickness of current collector (m):',\
              variable=str,parser=p, default='10e-6', menu=mAs)
anode_stoich_parameter=Parameter(name='anode_stoich_parameter', display_name='Initial stoichiometric parameter',\
              variable=str, menu=mAs, default='0.8')
anode_particle_radius=Parameter(name='anode_particle_radius', display_name='Radius of particles (m):',\
              variable=str, menu=mAs, default='5.0e-6')
anode_electrolyte_volfrac=Parameter(name='anode_electrolyte_volfrac', display_name='Volume fraction of electrolyte:',\
              variable=str, menu=mAs, default='0.3')
anode_polymer_volfrac=Parameter(name='anode_polymer_volfrac', display_name='Volume fraction of polymer:',\
              variable=str, menu=mAs, default='0.05')
anode_filler_volfrac=Parameter(name='anode_filler_volfrac',display_name='Volume fraction of inert filler:',\
              variable=str, menu=mAs, default='0.0')
anode_gas_volfrac=Parameter(name='anode_gas_volfrac', display_name='Volume fraction of gas:',\
              variable=str, menu=mAs, default='0.0')
Parameter(name='', menu=mAs, variable='label')

#Parameters for 'Anode Transport Parameters'
MVDC1_OPT = {'No':0, 'Yes':1}


Parameter(name='', menu=mAt, variable='label')
Parameter(name='Anode Transport Parameters', menu=mAt, variable='label')
Parameter(name='', menu=mAt, variable='label')
anode_diff_coef=Parameter(name='anode_diff_coef', display_name='Solid diffusion coefficient (m^2/s):',\
              variable=str, menu=mAt, default='1.0e-13')
anode_vary_diff=Parameter(name='anode_vary_diff', display_name='Allow diffusion coeff. to vary?', variable=dict,\
              menu=mAt, default=(MVDC1_OPT))
anode_matrix_conductivity=Parameter(name='anode_matrix_conductivity', display_name='Conductivity of matrix (S/m):',\
              variable=str, menu=mAt, default='0.5')
anode_bulk_rate=Parameter(name='anode_bulk_rate', display_name='Rate constant for bulk reaction (m^2/s):',\
              variable=str, menu=mAt, default='3.0e-9')
anode_rate_side1=Parameter(name='anode_rate_side1', display_name='Rate constant side reaction 1 (m^2/s):', variable=str,\
              menu=mAt, default='0.0')
anode_rate_side2=Parameter(name='anode_rate_side2', display_name='Rate constant side reaction 2 (m^2/s):', variable=str,\
              menu=mAt, default='0.0')
anode_rate_side3=Parameter(name='anode_rate_side3', display_name='Rate constant side reaction 3 (m^2/s):', variable=str,\
              menu=mAt, default='0.0')
Parameter(name='', menu=mAt, variable='label')

#Parameters for 'Separator Physical Parameters'

SEP_OPT = {'LiPF6 in EC:DMC (liquid)':11,
              'Perchlorate in PEO':2,
              'Sodium Triflate in PEO':3,
              'LiPF6 in PC (Sony cell simulation)':4, 
              'Perchlorate in PC (West simulation)':5,
              'Triflate in PEO':6, 
              'AsF6 in methyl acetate':1, 
              'Ideal ion exchange membrane':9, 
              'TFSI in PEMO at 40 C (oxymethylene-linked PEO) (LBL)':10, 
              'LiPF6 in EC/DMC and p(VdF-HFP) (Bellcore)':7,
              'LiTFSI in PEO at 85 C (LBL)':12, 
              'Paxton 30% KOH in H2O':13}

   
                              
Parameter(name='', menu=mSep, variable='label')
Parameter(name='Separator Physical Parameters', menu=mSep, variable='label')
Parameter(name='', menu=mSep, variable='label')
sep_material=Parameter(name='sep_material', display_name='Choose material:', variable=dict,\
              menu=mSep, default=(SEP_OPT))
sep_thickness=Parameter(name='sep_thickness', display_name='Thickness (m):', variable=str,\
              menu=mSep, default='25.0e-6')
sep_density=Parameter(name='sep_density', display_name='Density of inert separator material  (kg/m3):', variable=str,\
              menu=mSep, default='900.0')
sep_electrolyte_volfrac=Parameter(name='sep_electrolyte_volfrac', display_name='Volume fraction of electrolyte:', variable=str,\
              menu=mSep, default='0.4')
electrolyte_density=Parameter(name='electrolyte_density', display_name='Density of electrolyte (kg/m3):', variable=str,\
              menu=mSep, default='1324.0')
sep_polymer_volfrac=Parameter(name='sep_polymer_volfrac', display_name='Volume fraction of polymer:', variable=str,\
              menu=mSep, default='0.6')
polymer_density=Parameter(name='polymer_density', display_name='Density of polymer material (kg/m3):', variable=str,\
              menu=mSep, default='900.0')
filler_density=Parameter(name='filler_density', display_name='Density of inert filler (kg/m3):', variable=str,\
              menu=mSep, default='1800.0')
sep_gas_volfrac=Parameter(name='sep_gas_volfrac', display_name='Volume fraction of gas:', variable=str,\
              menu=mSep, default='0.0')
Parameter(name='', menu=mSep, variable='label')

#Parameters for 'Cathode Material Properties'

CAT_OPT = {'LiyCoO2 (0.5 < y < 0.99)':6,
              'LiyNaCoO2 P2 phase (0.3<y<0.92)':2, 
              'LiyMn2O4 Spinel (lower plateau)':3,
              'LiyMn2O4 Spinel (upper plateau)':4, 
              'LixWO3 (0<x<0.67)':5, 
              'LixMn2O4 (Bellcore)':9, 
              'LiyV2O5 (0 < y < 0.95)':7, 
              'LiyNi0.8Co0.2O2 Gen-1 (0.4 < y < 0.99)':8, 
              'TiS2 (for use with Li foil)':1, 
              'LiyV6O13 (0.05 < y < 1.0)':10, 
              'LiyAl0.2Mn1.8O4F0.2 Bellcore doped spinel (0.21 < y < 1.0)':11, 
              'Albertus NiOOH (Use for NiMH)':12}

Parameter(name='', menu=mCp, variable='label')
Parameter(name='Cathode Material Properties', menu=mCp, variable='label')
Parameter(name='', menu=mCp, variable='label')
cathode_material=Parameter(name='cathode_material', display_name='Choose material:', variable=dict,\
              menu=mCp, default=(CAT_OPT))
cathode_film_resistance=Parameter(name='cathode_film_resistance', display_name='Film resistance (Ohm-m2):', variable=str,\
              menu=mCp, default='0.0')
cathode_capacity=Parameter(name='cathode_capacity', display_name='Coulombic capacity of positive material (mAh/g):', variable=str,\
              menu=mCp, default='274.0')
cathode_capacitance=Parameter(name='cathode_capacitance', display_name='Capacitance (F/m2):', variable=str,\
              menu=mCp, default='0.0')
cathode_insertion_density=Parameter(name='cathode_insertion_density', display_name='Density of insertion material (kg/m3):', variable=str,\
              menu=mCp, default='5010.0')
cathode_collector_density=Parameter(name='cathode_collector_density', display_name='Density of current collector (kg/m3):', variable=str,\
              menu=mCp, default='2707.0')
Parameter(name='', menu=mCp, variable='label')

#Parameters for 'Cathode Spatial Parameters'

Parameter(name='', menu=mCs, variable='label')
Parameter(name='Cathode Spatial Parameters', menu=mCs, variable='label')
Parameter(name='', menu=mCs, variable='label')
cathode_thickness=Parameter(name='cathode_thickness', display_name='Thickness (m):', variable=str,\
              menu=mCs, default='100.0e-6')
cathode_collector_thickness=Parameter(name='cathode_collector_thickness', display_name='Thickness of current collector (m):', variable=str,\
              menu=mCs, default='10.0e-6')
cathode_stoich_parameter=Parameter(name='cathode_stoich_parameter', display_name='Initial stoichiometric parameter:', variable=str,\
              menu=mCs, default='0.2')
cathode_particle_radius=Parameter(name='cathode_particle_radius', display_name='Radius of particles (m):', variable=str,\
              menu=mCs, default='5.0e-6')
cathode_electrolyte_volfrac=Parameter(name='cathode_electrolyte_volfrac', display_name='Volume fraction of electrolyte:', variable=str,\
              menu=mCs, default='0.3')
cathode_polymer_volfrac=Parameter(name='cathode_polymer_volfrac', display_name='Volume fraction of polymer:', variable=str,\
              menu=mCs, default='0.05')
cathode_filler_volfrac=Parameter(name='cathode_filler_volfrac', display_name='Volume fraction of inert filler:', variable=str,\
              menu=mCs, default='0.05')
cathode_gas_volfrac=Parameter(name='cathode_gas_volfrac', display_name='Volume fraction of gas:', variable=str,\
              menu=mCs, default='0.0')

#Parameters for 'Cathode Transport Properties'
MVDC3_OPT = {'No':0, 'Yes':1}

Parameter(name='', menu=mCt, variable='label')
Parameter(name='Cathode Transport Parameters', menu=mCt, variable='label')
Parameter(name='', menu=mCt, variable='label')
cathode_diff_coef=Parameter(name='cathode_diff_coef', display_name='Solid diffusion coefficient (m2/s):', variable=str,\
              menu=mCt, default='5.0e-15')
cathode_vary_diff=Parameter(name='cathode_vary_diff', display_name='Allow diffusion coeff. to vary?', variable=dict,\
              menu=mCt, default=(MVDC3_OPT))
cathode_matrix_conductivity=Parameter(name='cathode_matrix_conductivity', display_name='Conductivity in matrix (S/m):', variable=str,\
              menu=mCt, default='0.5')
cathode_bulk_rate=Parameter(name='cathode_bulk_rate', display_name='Rate constant for bulk reaction (m^2/s):', variable=str,\
              menu=mCt, default='3.0e-9')
cathode_rate_side1=Parameter(name='cathode_rate_side1', display_name='Rate constant side reaction 1 (m^2/s):', variable=str,\
              menu=mCt, default='0.0')
cathode_rate_side2=Parameter(name='cathode_rate_side2', display_name='Rate constant side reaction 2 (m^2/s):', variable=str,\
              menu=mCt, default='0.0')
cathode_rate_side3=Parameter(name='cathode_rate_side3', display_name='Rate constant side reaction 3 (m^2/s):', variable=str,\
              menu=mCt, default='0.0')
Parameter(name='', display_name='', variable='label',\
              menu=mCt)


#Parameters for 'Initial Conditions'



Parameter(name='', menu=mIp, variable='label')
Parameter(name='Initial Conditions', menu=mIp, variable='label')
Parameter(name='', menu=mIp, variable='label')
battery_temp=Parameter(name='battery_temp', display_name='Battery temperature (K):', variable=str,\
              menu=mIp, default='298.15')
initial_salt_conc=Parameter(name='initial_salt_conc', display_name='Initial salt concentration (mol/m3):', variable=str,\
              menu=mIp, default='1000.0')
ambient_air_temp=Parameter(name='ambient_air_temp', display_name='Ambient air Temperature (K):', variable=str,\
              menu=mIp, default='298.15')
system_heat_capacity=Parameter(name='system_heat_capacity', display_name='Heat capacity of system (J/kg-K):', variable=str,\
              menu=mIp, default='500.0')
cells_in_stack=Parameter(name='cells_in_stack', display_name='Number of cells in stack:', variable=str,\
              menu=mIp, default='1')

#Parameters for 'Initial Conditions (Cont.)'

##ELECTROLYTE CHEMISTRY DROPDOWN OPTIONS
ELEC_OPT = {'Uniform distribution':1, 'Electrolyte in separator only':0}
##IMPEDANCE DROPDOWN OPTIONS
IMP_OPT = {'No Impedance':0, 'Impedance':1}
##HEAT TRANSFER DROPDOWN OPTIONS
HT_OPT = {'Use coefficient below':0, 'Calculate real-time coefficient':1,\
              'Isothermal':2}
##SIDE REACTION DROPDOWN OPTIONS
NSIDE_OPT = {'No':0, 'Yes':1}


heat_transfer_setting=Parameter(name='heat_transfer_setting', display_name='Heat transfer:', variable=dict,\
              menu=mIp, default=(HT_OPT))
heat_transfer_end=Parameter(name='heat_transfer_end', display_name='Heat transfer coeff. at end (W/m2K):',\
              variable=str, menu=mIp, default='0.0')
electrolyte_distribution=Parameter(name='electrolyte_distribution', display_name='Electrolyte distribution:', variable=dict,\
              menu=mIp, default=(ELEC_OPT))
impedance=Parameter(name='impedance', display_name='Impedance:', variable=dict,\
              menu=mIp, default=(IMP_OPT))
side_reaction_flag=Parameter(name='side_reaction_flag', display_name='Calculate side reactions?', variable=dict,\
              menu=mIp, default=(NSIDE_OPT))

#Parameters for 'Boundary Conditions'

##SEGMENT MODE DROPDOWN OPTIONS
MODE_OPT = ('Galvanostatic to a cutoff potential (in A/m2)', 'Galvanostatic for given time (in A/m2)',\
              'Potentiostatic (in V)',\
              'Galvanostatic with tapered current after cutoff potential (in A/m2)',\
              'Specified power (in W/m2)', 'Specified load (in ohm-m2)')
Parameter(name='', menu=mSs, variable='label')
Parameter(name='Boundary Conditions', menu=mSs, variable='label')
Parameter(name='', menu=mSs, variable='label')
current_changes=Parameter(name='current_changes', display_name='Number of segments in this simulation:', variable=str,\
              menu=mSs, default='1')
Parameter(name='In the following, use comma separated lists to specify multiple segments', menu=mSs, variable='label')
Parameter(name='', menu=mSs, variable='label')
segment_mode=Parameter(name='segment_mode', display_name='Mode of segment(s):', variable=str,\
              menu=mSs, default='2')
Parameter(name='', menu=mSs, variable='label', display_name='--------------------------------------------------------------------------------\
----------------------')
Parameter(name='', menu=mSs, variable='label', display_name='2 for Galvanostatic to a cutoff potential (in A/m2)\n\
1 for Galvanostatic for given time (in A/m2)\n\
0 for Potentiostatic (in V)\n\
-1 for Galvanostatic with tapered current after cutoff potential (in A/m2)\n\
-2 for Specified power (in W/m2)\n\
-3 for Specified load (in ohm-m2)')
Parameter(name='', menu=mSs, variable='label', display_name='------------------------------------------------------------\
------------------------------------------')
current_density=Parameter(name='current_density', display_name='Segment current/potential/power/load:', variable=str,\
              menu=mSs, default='20')
cutoff_condition=Parameter(name='cutoff_condition', display_name='Simulation time (min) OR potential cutoff (V):', variable=str,\
              menu=mSs, default='2')
low_voltage_cutoff=Parameter(name='low_voltage_cutoff', display_name='Low voltage cutoff value (V):', variable=str,\
              menu=mSs, default='2.0')
high_voltage_cutoff=Parameter(name='high_voltage_cutoff', display_name='High voltage cutoff value (V):', variable=str,\
              menu=mSs, default='4.5')

Parameter(name='', display_name='', variable='label',\
              menu=mSs)



#Parameters for 'Solver and Numerical Parameters'

Parameter(name='', menu=mNp, variable='label')
Parameter(name='Solver and Numerical Parameters', menu=mNp, variable='label')
Parameter(name='', menu=mNp, variable='label')

##POWER PEAK DROPDOWN OPTIONS
PP_OPT = {'Exclude power peaks':0, 'Include power peaks':1}

Parameter(name='', display_name='', variable='label',\
              menu=mNp)
iteration_limit=Parameter(name='iteration_limit', display_name='Limit on number of iterations:', variable=str,\
              menu=mNp, default='50')
max_timestep_size=Parameter(name='max_timestep_size', display_name='Maximum time step size (s)', variable=str,\
              menu=mNp, default='10')
anode_node_count=Parameter(name='anode_node_count', display_name='Number of nodes in anode (0 if using foil):', variable=str,\
              menu=mNp, default='80')
separator_node_count=Parameter(name='separator_node_count', display_name='Number of nodes in separator:', variable=str,\
              menu=mNp, default='40')
cathode_node_count=Parameter(name='cathode_node_count', display_name='Number of nodes in cathode:', variable=str,\
              menu=mNp, default='80')
jsol=Parameter(name='jsol', display_name='Save profile in solid particle at node n=', variable=str,\
              menu=mNp, default='0')
particle_node_count=Parameter(name='particle_node_count', display_name='Number of nodes inside the solid particle:', variable=str,\
              menu=mNp, default='100')
converge_condition=Parameter(name='converge_condition', display_name='Number of iterations for solid phase convergence:', variable=str,\
              menu=mNp, default='10')
power_peaks=Parameter(name='power_peaks', display_name='Power peaks:', variable=dict,\
              menu=mNp, default=(PP_OPT))
Parameter(name='', display_name='', variable='label',\
              menu=mNp)


#Parameters for menu 6 (Activation Energies)


Parameter(name='', display_name='', variable='label',\
              menu=mEa)
Parameter(name='', display_name='Activation Energy', variable='label',\
              menu=mEa)
Parameter(name='', display_name='', variable='label',\
              menu=mEa)
EbarS1=Parameter(name='EbarS1', display_name='Solid state diffusion in anode (J/mol):', variable=str,\
              menu=mEa, default='0.0')
EbarS3=Parameter(name='EbarS3', display_name='Solid state diffusion in cathode (J/mol):', variable=str,\
              menu=mEa, default='0.0')
Ebarkap=Parameter(name='Ebarkap', display_name='Electrolyte conductivity (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
EbarD=Parameter(name='EbarD', display_name='Electrolyte diffusion (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarka=Parameter(name='Ebarka', display_name='Anode kinetics (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarkc=Parameter(name='Ebarkc', display_name='Cathode kinetics (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarks1a=Parameter(name='Ebarks1a', display_name='Negative O2 side reaction (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarks1c=Parameter(name='Ebarks1c', display_name='Positive O2 side reaction (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarks2a=Parameter(name='Ebarks2a', display_name='Evol. H2 side reaction (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarks2c=Parameter(name='Ebarks2c', display_name='Recombination H2 side reaction (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarks3a=Parameter(name='Ebarks3a', display_name='Negative shuttle side reaction (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarks3c=Parameter(name='Ebarks3c', display_name='Positive shuttle side reactions (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarr1=Parameter(name='Ebarr1', display_name='Anode film resistance (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Ebarr3=Parameter(name='Ebarr3', display_name='Cathode film resistance (J/mol):', variable=str,\
              menu=mEa, default='4000.0')
Parameter(name='', display_name='', variable='label',\
              menu=mEa)
              
              
              
#Parameters for 'Scheduled Output'
Parameter(name='', display_name='', variable='label',\
              menu=mlaunch)
Parameter(name='', display_name='Scheduled Output', variable='label', menu=mlaunch)
Parameter(name='', display_name='', variable='label',\
              menu=mlaunch)
    
Parameter(name='', display_name='Working directory:', variable='label',\
              menu=mlaunch)
# label_cwd=Parameter(name='', display_name='{}'.format(os.getcwd()), variable='label',\
#               menu=mlaunch)
 
select_cwd=Parameter(name='', display_name='{}'.format(os.getcwd()), variable='function', default=choose_cwd,	menu=mlaunch,button_text='Select working directory')

Parameter(name='', display_name='', variable='label',\
              menu=mlaunch)
    
directory=Parameter(menu=mlaunch, name='directory', display_name='Output Directory:',\
              variable=str, default='Output')
node_freq=Parameter(name='node_freq', display_name='Save every ith node where i=', variable=str,\
              menu=mlaunch, default='10')
time_step_freq=Parameter(name='time_step_freq', display_name='Save every nth time step where n=', variable=str,\
              menu=mlaunch, default='2')
Parameter(name='', display_name='', variable='label',\
              menu=mlaunch)
run_function=Parameter(name='SOLVE', variable='function', default=RunDualfoil,\
				menu=mlaunch)
solve_status=Parameter(name='', display_name='', variable='label',\
              menu=mlaunch,default='')


if __name__=="__main__":
	sys.argv.append('--gui')
	if p.is_gui_mode()==False:
		p.add_command(RunDualfoil)
	else:
		pass
	p()

	
	
	
