#Import VKML tools
from VKML.gui.tk import Parameter, Parser, Menu
import time, sys, os
import shutil
import tkMessageBox

toolHomeDir = os.path.dirname(os.path.abspath(__file__))

def RunDualfoil(iteration_limit, anode_thickness, sep_thickness, cathode_thickness, anode_collector_thickness,\
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
              current_density, cutoff_condition, segment_mode, low_voltage_cutoff, high_voltage_cutoff, internal_resistance,\
              EbarS1, EbarS3, Ebarkap, EbarD,\
              Ebarka, Ebarkc, Ebarks1a, Ebarks1c,\
              Ebarks2a, Ebarks2c, Ebarks3a, Ebarks3c,\
              Ebarr1, Ebarr3, directory):


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
	internal_resistance = internal_resistance.replace(" ","")
	internal_resistance = internal_resistance.split(",")
	
	if int(current_changes) > 1:
		if len(current_density) != int(current_changes):
			tkMessageBox.showinfo(title='Input Error', message='Warning: A total of %s current/load/power \
			values were specified for %s specified current changes.' % (str(len(current_density)), str(int(current_changes)))) 
			sys.exit()
	else: 
		if len(segment_mode) > 1 or len(current_density) > 1 or len(cutoff_condition) > 1 or len(low_voltage_cutoff) > 1 or len(high_voltage_cutoff) > 1:
			tkMessageBox.showinfo(title='Input Error', message='Not enough current changes were specified for multiple sets of boundary conditions.') 
			sys.exit()
	jsol = 0
	il1 = 1  
	
##---------------------------UPDATE anode_material------------------------------------
	step=0
	nneg_opt = (3, 2, 1, 4, 5, 6, 7)
	while step <= len(AND_OPT):
				if anode_material==AND_OPT[step]:
							  anode_material=nneg_opt [step]
							  step=len(AND_OPT)+1
				else:
							  step=step+1
##---------------------------UPDATE sep_material------------------------------------
	step=0
	nprop_opt = (11, 2, 3, 4, 5, 6, 1, 9, 10, 7, 12, 13)
	while step <= len(SEP_OPT):
				if sep_material==SEP_OPT[step]:
							  sep_material=nprop_opt[step]
							  step=len(SEP_OPT)+1
				else:
							  step=step+1
##---------------------------UPDATE cathode_material------------------------------------
	step=0
	npos_opt = (6, 2, 3, 4, 5, 9, 7, 8, 1, 10, 11, 12)
	while step <= len(CAT_OPT):
				if cathode_material==CAT_OPT[step]:
							  cathode_material=npos_opt[step]
							  step=len(CAT_OPT)+1
				else:
							  step=step+1
##---------------------------UPDATE electrolyte_distribution------------------------------------
	step=0
	lflag_opt = (1, 0)
	while step <= len(ELEC_OPT):
				if electrolyte_distribution==ELEC_OPT[step]:
							  electrolyte_distribution=lflag_opt[step]
							  step=len(ELEC_OPT)+1
				else:
							  step=step+1
##---------------------------UPDATE impedance------------------------------------
	step=0
	while step <= len(IMP_OPT):
				if impedance==IMP_OPT[step]:
							  impedance=step
							  step=len(IMP_OPT)+1
				else:
							  step=step+1
##---------------------------UPDATE segment_mode------------------------------------
	#step=0
	#mc_opt = (2, 1, 0, -1, -2, -3)
	#while step <= len(MODE_OPT):
				#if segment_mode==MODE_OPT[step]:
							  #segment_mode=mc_opt[step]
							  #step=len(MODE_OPT)+1
				#else:
							  #step=step+1
##---------------------------UPDATE heat_transfer_setting------------------------------------
	step=0
	while step <= len(HT_OPT):
				if heat_transfer_setting==HT_OPT[step]:
							  heat_transfer_setting=step
							  step=len(HT_OPT)+1
				else:
							  step=step+1
##---------------------------UPDATE side_reaction_flag------------------------------------
	step=0
	while step <= len(NSIDE_OPT):
				if side_reaction_flag==NSIDE_OPT[step]:
							  side_reaction_flag=step
							  step=len(NSIDE_OPT)+1
				else:
							  step=step+1
##---------------------------UPDATE anode_vary_diff------------------------------------
	step=0
	while step <= len(MVDC1_OPT):
				if anode_vary_diff==MVDC1_OPT[step]:
							  anode_vary_diff=step
							  step=len(MVDC1_OPT)+1
				else:
							  step=step+1
##---------------------------UPDATE cathode_vary_diff------------------------------------
	step=0
	while step <= len(MVDC3_OPT):
				if cathode_vary_diff==MVDC3_OPT[step]:
							  cathode_vary_diff=step
							  step=len(MVDC3_OPT)+1
				else:
							  step=step+1
##---------------------------UPDATE power_peaks------------------------------------
	step=0
	while step <= len(PP_OPT):
				if power_peaks==PP_OPT[step]:
							  power_peaks=step
							  step=len(PP_OPT)+1
				else:
							  step=step+1 


      
	#CREATE WORKING DIRECTORY FOR THIS RUN
	os.system('mkdir -p %s' % (directory))
	time.sleep(.005)
	
	#CREATE FILE WITH ALL DIRECTORIES
	
	if os.path.isfile('directories.txt') == True:
		check = open('directories.txt' , 'r')
		check_dirs_hold = check.readlines()
		check_dirs = [l.strip('\n') for l in check_dirs_hold]
		check.close()
		d = open('directories.txt' , 'a')
		check_bool = False
		for line in check_dirs:
			if line==directory:
				check_bool = True  	  
		if check_bool == False:
			d.write('%s\n' % directory)
			d.close()
	else:
		d = open('directories.txt' , 'a')
		d.write('%s\n' % directory)
		d.close()
				
              

              

	
	#CREATE LI-ION.IN INPUT FILE
	owd = os.getcwd()
	os.chdir('%s' % directory)
	f = open('li-ion.in','w+')
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
	SegmentParameters = [current_density, cutoff_condition, segment_mode, low_voltage_cutoff, high_voltage_cutoff, internal_resistance]
	
	for y in VarList:
		f.write('%s\n' % y)
	if int(current_changes) == 1:
			f.write('%s ' % current_density[0])
			f.write('%s ' % cutoff_condition[0])
			f.write('%s ' % segment_mode[0])
			f.write('%s ' % low_voltage_cutoff[0])
			f.write('%s ' % high_voltage_cutoff[0])
			f.write('%s' % internal_resistance[0])
	else:
		segment_number = int(current_changes)
		for x in range(0, segment_number):
				try:
					f.write('%s ' % current_density[x])
					f.write('%s ' % cutoff_condition[x])
					f.write('%s ' % segment_mode[x])
					f.write('%s ' % low_voltage_cutoff[x])
					f.write('%s ' % high_voltage_cutoff[x])
					f.write('%s\n' % internal_resistance[x])
				except:
					tkMessageBox.showinfo(title='Input Error', message='For each segment change, you must specify:\n\n' 
					+ 'Segment Mode \nCurrent denisty/Load/Power \nSegment Time/Cutoff Potential \nLow Voltage Cutoff \nHigh Volatge Cutoff \nInternal Resistance')
					sys.exit()
	f.close()
	
	ebar = open('li-ion-ebar.in', 'w+')
	ActList = [EbarS1, EbarS3, Ebarkap, EbarD,\
		Ebarka, Ebarkc, Ebarks1a, Ebarks1c,\
		Ebarks2a, Ebarks2c, Ebarks3a, Ebarks3c,\
		Ebarr1, Ebarr3]
	
	for z in ActList:
		ebar.write('%s\n' % z)
	ebar.close()
	print 'Now Running Dualfoil...'
	os.system('dualfoil.x')
	print 'Done.'
	os.chdir(owd)
	visCommand = "python %s --gui & > error_log.txt" % (os.path.join(toolHomeDir,'visualize.py'))
	os.system(visCommand)
	





#Create functions
#def callback():

#Create parser
p=Parser(title='Dualfoil Battery Simulation')

#Create menus
#welcome = Menu(title='Welcome', parser=p)
mAp = Menu(title='Anode Material Properties', parser=p)
mAs = Menu(title='Anode Spatial Parameters', parser=p)
mAt = Menu(title='Anode Transport Parameters', parser=p)
mSep = Menu(title='Separator Physical Parameters', parser=p)
mCp = Menu(title='Cathode Material Properties', parser=p)
mCs = Menu(title='Cathode Spatial Parameters', parser=p)
mCt = Menu(title='Cathode Transport Parameters', parser=p)

mIp = Menu(title='Initial Conditions', parser=p)
mIp2 = Menu(title='Initial Conditions (Cont.)', parser=p)
mSs = Menu(title='Boundary Conditions', parser=p)
mNp = Menu(title='Solver and Numerical Parameters', parser=p)
mEa = Menu(title='Activation Energies', parser=p)
mlaunch = Menu(title='Simulation Setup', parser=p)


#PARAMETERS FOR WELCOME MENU

#Parameters for 'Anode Material Properties'

AND_OPT = ('MCMB 2528 graphite (Bellcore)','Carbon (petroleum coke)',\
              'Lithium foil', 'TiS2', 'Tungsten oxide',\
              'Lonza KS6 graphite', 'Albertus MH (Use for NiMH)')

Parameter(name='', menu=mAp, variable='label')
Parameter(name='Anode Material Properties', menu=mAp, variable='label')
Parameter(name='', menu=mAp, variable='label')
anode_material=Parameter(name='anode_material', display_name='Choose material:', variable=tuple,\
              menu=mAp, default=(AND_OPT))
anode_film_resistance=Parameter(name='anode_film_resistance', display_name='Film resistance (Ohm-m2):',\
              variable=str, menu=mAp, default='0.35e-2')
anode_capacity=Parameter(name='anode_capacity', display_name='Coulombic capacity of negative material (mAh/g):',\
              variable=str, menu=mAp, default='372.26')
anode_capacitance=Parameter(name='anode_capacitance', display_name='Capacitance (F/m2):',\
              variable=str, menu=mAp, default='0.0')
anode_insertion_density=Parameter(name='anode_insertion_density', display_name='Density of insertion material (kg/m3):',\
              variable=str, menu=mAp, default='1800.0')
anode_collector_density=Parameter(name='anode_collector_density', display_name='Density of current collector (kg/m3):',\
              variable=str, menu=mAp, default='8954.0')
Parameter(name='', menu=mAp, variable='label')


#Parameters for 'Anode Spacial Parameters'

Parameter(name='', menu=mAs, variable='label')
Parameter(name='Anode Geometric Parameters', menu=mAs, variable='label')
Parameter(name='', menu=mAs, variable='label')
anode_thickness=Parameter(name='anode_thickness', display_name='Thickness (m):', variable=str,\
              menu=mAs, default='96.0e-6')
anode_collector_thickness=Parameter(name='anode_collector_thickness', display_name='Thickness of current collector (m):',\
              variable=str,parser=p, default='10e-6', menu=mAs)
anode_stoich_parameter=Parameter(name='anode_stoich_parameter', display_name='Initial stoichiometric parameter',\
              variable=str, menu=mAs, default='0.8')
anode_particle_radius=Parameter(name='anode_particle_radius', display_name='Radius of particles (m):',\
              variable=str, menu=mAs, default='8.0e-6')
anode_electrolyte_volfrac=Parameter(name='anode_electrolyte_volfrac', display_name='Volume fraction of electrolyte:',\
              variable=str, menu=mAs, default='0.4')
anode_polymer_volfrac=Parameter(name='anode_polymer_volfrac', display_name='Volume fraction of polymer:',\
              variable=str, menu=mAs, default='0.0')
anode_filler_volfrac=Parameter(name='anode_filler_volfrac',display_name='Volume fraction of inert filler:',\
              variable=str, menu=mAs, default='0.06')
anode_gas_volfrac=Parameter(name='anode_gas_volfrac', display_name='Volume fraction of gas:',\
              variable=str, menu=mAs, default='0.0')
Parameter(name='', menu=mAs, variable='label')

#Parameters for 'Anode Transport Parameters'
MVDC1_OPT = ('No', 'Yes')


Parameter(name='', menu=mAt, variable='label')
Parameter(name='Anode Transport Parameters', menu=mAt, variable='label')
Parameter(name='', menu=mAt, variable='label')
anode_diff_coef=Parameter(name='anode_diff_coef', display_name='Solid diffusion coefficient (m^2/s):',\
              variable=str, menu=mAt, default='7.0e-14')
anode_vary_diff=Parameter(name='anode_vary_diff', display_name='Allow diffusion coeff. to vary?', variable=tuple,\
              menu=mAt, default=(MVDC1_OPT))
anode_matrix_conductivity=Parameter(name='anode_matrix_conductivity', display_name='Conductivity of matrix (S/m):',\
              variable=str, menu=mAt, default='100.0')
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

SEP_OPT = ('LiPF6 in EC:DMC (liquid)',\
              'Perchlorate in PEO', 'Sodium Triflate in PEO',\
              'LiPF6 in PC (Sony cell simulation)', \
              'Perchlorate in PC (West simulation)', 'Triflate in PEO', \
              'AsF6 in methyl acetate', \
              'Ideal ion exchange membrane', \
              'TFSI in PEMO at 40 C (oxymethylene-linked PEO) (LBL)', \
              'LiPF6 in EC/DMC and p(VdF-HFP) (Bellcore)', 'LiTFSI in PEO at 85 C (LBL)', \
              'Paxton 30% KOH in H2O')

Parameter(name='', menu=mSep, variable='label')
Parameter(name='Separator Physical Parameters', menu=mSep, variable='label')
Parameter(name='', menu=mSep, variable='label')
sep_material=Parameter(name='sep_material', display_name='Choose material:', variable=tuple,\
              menu=mSep, default=(SEP_OPT))
sep_thickness=Parameter(name='sep_thickness', display_name='Thickness (m):', variable=str,\
              menu=mSep, default='25.0e-6')
sep_density=Parameter(name='sep_density', display_name='Density of inert separator material  (kg/m3):', variable=str,\
              menu=mSep, default='552.0')
sep_electrolyte_volfrac=Parameter(name='sep_electrolyte_volfrac', display_name='Volume fraction of electrolyte:', variable=str,\
              menu=mSep, default='4.0')
electrolyte_density=Parameter(name='electrolyte_density', display_name='Density of electrolyte (kg/m3):', variable=str,\
              menu=mSep, default='1324.0')
sep_polymer_volfrac=Parameter(name='sep_polymer_volfrac', display_name='Volume fraction of polymer:', variable=str,\
              menu=mSep, default='0.0')
polymer_density=Parameter(name='polymer_density', display_name='Density of polymer material (kg/m3):', variable=str,\
              menu=mSep, default='1780.0')
filler_density=Parameter(name='filler_density', display_name='Density of inert filler (kg/m3):', variable=str,\
              menu=mSep, default='1800.0')
sep_gas_volfrac=Parameter(name='sep_gas_volfrac', display_name='Volume fraction of gas:', variable=str,\
              menu=mSep, default='0.0')
Parameter(name='', menu=mSep, variable='label')

#Parameters for 'Cathode Material Properties'

CAT_OPT = ('LiyCoO2 (0.5 < y < 0.99)',\
              'LiyNaCoO2 P2 phase (0.3<y<0.92)', \
              'LiyMn2O4 Spinel (lower plateau)',\
              'LiyMn2O4 Spinel (upper plateau)', \
              'LixWO3 (0<x<0.67)', \
              'LixMn2O4 (Bellcore)', \
              'LiyV2O5 (0 < y < 0.95)', \
              'LiyNi0.8Co0.2O2 Gen-1 (0.4 < y < 0.99)', \
              'TiS2 (for use with Li foil)', \
              'LiyV6O13 (0.05 < y < 1.0)', \
              'LiyAl0.2Mn1.8O4F0.2 Bellcore doped spinel (0.21 < y < 1.0)', \
              'Albertus NiOOH (Use for NiMH)')

Parameter(name='', menu=mCp, variable='label')
Parameter(name='Cathode Material Properties', menu=mCp, variable='label')
Parameter(name='', menu=mCp, variable='label')
cathode_material=Parameter(name='cathode_material', display_name='Choose material:', variable=tuple,\
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
              menu=mCs, default='60.0e-6')
cathode_collector_thickness=Parameter(name='cathode_collector_thickness', display_name='Thickness of current collector (m):', variable=str,\
              menu=mCs, default='10.0e-6')
cathode_stoich_parameter=Parameter(name='cathode_stoich_parameter', display_name='Initial stoichiometric parameter:', variable=str,\
              menu=mCs, default='0.6')
cathode_particle_radius=Parameter(name='cathode_particle_radius', display_name='Radius of particles (m):', variable=str,\
              menu=mCs, default='5.0e-6')
cathode_electrolyte_volfrac=Parameter(name='cathode_electrolyte_volfrac', display_name='Volume fraction of electrolyte:', variable=str,\
              menu=mCs, default='0.36')
cathode_polymer_volfrac=Parameter(name='cathode_polymer_volfrac', display_name='Volume fraction of polymer:', variable=str,\
              menu=mCs, default='0.186')
cathode_filler_volfrac=Parameter(name='cathode_filler_volfrac', display_name='Volume fraction of inert filler:', variable=str,\
              menu=mCs, default='0.106')
cathode_gas_volfrac=Parameter(name='cathode_gas_volfrac', display_name='Volume fraction of gas:', variable=str,\
              menu=mCs, default='0.0')

#Parameters for 'Cathode Transport Properties'
MVDC3_OPT = ('No', 'Yes')

Parameter(name='', menu=mCt, variable='label')
Parameter(name='Cathode Transport Parameters', menu=mCt, variable='label')
Parameter(name='', menu=mCt, variable='label')
cathode_diff_coef=Parameter(name='cathode_diff_coef', display_name='Solid diffusion coefficient (m2/s):', variable=str,\
              menu=mCt, default='3.0e-13')
cathode_vary_diff=Parameter(name='cathode_vary_diff', display_name='Allow diffusion coeff. to vary?', variable=tuple,\
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
Parameter(name='', display_name=':', variable='label',\
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
ELEC_OPT = ('Uniform distribution', 'Electrolyte in separator only')
##IMPEDANCE DROPDOWN OPTIONS
IMP_OPT = ('No Impedance', 'Impedance')
##HEAT TRANSFER DROPDOWN OPTIONS
HT_OPT = ('Use coefficient below', 'Calculate real-time coefficient',\
              'Isothermal')
##SIDE REACTION DROPDOWN OPTIONS
NSIDE_OPT = ('No', 'Yes')

Parameter(name='', menu=mIp2, variable='label')
Parameter(name='Initial Conditions (Cont.)', menu=mIp2, variable='label')
Parameter(name='', menu=mIp2, variable='label')
heat_transfer_setting=Parameter(name='heat_transfer_setting', display_name='Heat transfer:', variable=tuple,\
              menu=mIp2, default=(HT_OPT))
heat_transfer_end=Parameter(name='heat_transfer_end', display_name='Heat transfer coeff. at end (W/m2K):',\
              variable=str, menu=mIp2, default='0.0')
electrolyte_distribution=Parameter(name='electrolyte_distribution', display_name='Electrolyte distribution:', variable=tuple,\
              menu=mIp2, default=(ELEC_OPT))
impedance=Parameter(name='impedance', display_name='Impedance:', variable=tuple,\
              menu=mIp2, default=(IMP_OPT))
side_reaction_flag=Parameter(name='side_reaction_flag', display_name='Calculate side reactions?', variable=tuple,\
              menu=mIp2, default=(NSIDE_OPT))

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
              menu=mSs, default='17.5')
cutoff_condition=Parameter(name='cutoff_condition', display_name='Simulation time (min) OR potential cutoff (V):', variable=str,\
              menu=mSs, default='1')
low_voltage_cutoff=Parameter(name='low_voltage_cutoff', display_name='Low voltage cutoff value (V):', variable=str,\
              menu=mSs, default='2.0')
high_voltage_cutoff=Parameter(name='high_voltage_cutoff', display_name='High voltage cutoff value (V):', variable=str,\
              menu=mSs, default='4.7')
internal_resistance=Parameter(name='internal_resistance', display_name='Internal resistance of foils, tabs, etc. (ohm-m2):', variable=str,\
              menu=mSs, default='0.0')
Parameter(name='', display_name='', variable='label',\
              menu=mSs)



#Parameters for 'Solver and Numerical Parameters'

Parameter(name='', menu=mNp, variable='label')
Parameter(name='Solver and Numerical Parameters', menu=mNp, variable='label')
Parameter(name='', menu=mNp, variable='label')

##POWER PEAK DROPDOWN OPTIONS
PP_OPT = ('Exclude power peaks', 'Include power peaks')

Parameter(name='', display_name=':', variable='label',\
              menu=mNp)
iteration_limit=Parameter(name='iteration_limit', display_name='Limit on number of iterations:', variable=str,\
              menu=mNp, default='460')
max_timestep_size=Parameter(name='max_timestep_size', display_name='Maximum time step size (s)', variable=str,\
              menu=mNp, default='1.02')
anode_node_count=Parameter(name='anode_node_count', display_name='Number of nodes in anode (0 if using foil):', variable=str,\
              menu=mNp, default='40')
separator_node_count=Parameter(name='separator_node_count', display_name='Number of nodes in separator:', variable=str,\
              menu=mNp, default='40')
cathode_node_count=Parameter(name='cathode_node_count', display_name='Number of nodes in cathode:', variable=str,\
              menu=mNp, default='80')
particle_node_count=Parameter(name='particle_node_count', display_name='Number of nodes in solid particle:', variable=str,\
              menu=mNp, default='100')
converge_condition=Parameter(name='converge_condition', display_name='Number of iterations for solid phase convergence:', variable=str,\
              menu=mNp, default='10')
power_peaks=Parameter(name='power_peaks', display_name='Power peaks:', variable=tuple,\
              menu=mNp, default=(PP_OPT))
Parameter(name='', display_name=':', variable='label',\
              menu=mNp)


#Parameters for menu 6 (Activation Energies)


Parameter(name='', display_name=':', variable='label',\
              menu=mEa)
Parameter(name='', display_name='Activation Energy', variable='label',\
              menu=mEa)
Parameter(name='', display_name=':', variable='label',\
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
Parameter(name='', display_name=':', variable='label',\
              menu=mEa)
              
              
              
#Parameters for 'Scheduled Output'
Parameter(name='', display_name='', variable='label',\
              menu=mlaunch)
Parameter(name='', display_name='Scheduled Output', variable='label', menu=mlaunch)
Parameter(name='', display_name='', variable='label',\
              menu=mlaunch)

directory=Parameter(menu=mlaunch, name='directory', display_name='Output Directory:',\
              variable=str, default='Output')
node_freq=Parameter(name='node_freq', display_name='Save every ith node where i=', variable=str,\
              menu=mlaunch, default='10')
time_step_freq=Parameter(name='time_step_freq', display_name='Save every nth time step where n=', variable=str,\
              menu=mlaunch, default='10')
Parameter(name='', display_name='', variable='label',\
              menu=mlaunch)
run_function=Parameter(name='SOLVE', variable='function', default=RunDualfoil,\
				menu=mlaunch)
Parameter(name='', display_name='', variable='label',\
              menu=mlaunch)

if __name__=="__main__":
	if p.is_gui_mode()==False:
		p.add_command(RunDualfoil)
	else:
		pass
	p()

	
	
	
