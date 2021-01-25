from matplotlib import pyplot as plt
from VKML.gui.tk import Parameter, Parser, Menu
from pylab import *
import tkMessageBox
import re, os, sys
import os.path



def GetDirectories():
	if os.path.isfile('directories.txt') == True:
		f = open('directories.txt' , 'r')
		data = f.readlines()
		dirs = ()
		for line in data:
			lst = line.split('\n')
			dirs = dirs + (lst[0],)
		return dirs
	else:
		print 'No data to visualize. Please run a simulation.'
		sys.exit(0)

def IsNumeric(lst):
	#FOR EACH VALUE FROM 0 TO LENGTH OF LINE
	for x in (0, len(lst)):
		try:
			#TRUE IF NUMERICAL
			float(lst[x])
			return True	
		except ValueError:
			#FALSE IF NOT NUMERICAL
			return False			

def Ragone(all_energy, all_power):
	
	#GET DIRECTORIES
	dirs = GetDirectories()
	power = ()
	energy = ()
		
	for x in dirs:
		dirdict_hold = dirdict[x]()
		#DETERMINE WHICH BOOLS WERE SELECTED
		if dirdict_hold == True:
			#OPEN FILE INSIDE SLECTED DIRECTORY
			f = open('%s/dualfoil5.out' % x, 'r+')
			data = f.readlines()
			f.close()
			#LOOP THROUGH ALL DATA LINES
			for line in data:
				#REMOVE ALL WHITESPACE/0'S AND SPLIT
				lst = line
				lst = lst.strip()
				lst = lst.split(',')
				#CHECK FIRST ELEMENT FOR 'ENERGY' AND 'POWER'
				hold = lst[0]
				hold = hold.split(" ")
				if hold[0]=='energy':
					lst_new = filter(None, hold)											
					all_energy[x] = all_energy[x] + (lst_new[2],)
				elif hold[0]=='power':
					lst_new = filter(None, hold)						
					all_power[x] = all_power[x] + (lst_new[2],)

	
	#GENERATE FLOAT LIST FOR SCATTER PLOT
	step=0
	for x in all_energy:
			energy_hold = all_energy[x]
			if all_energy[x]:
				energy = energy + (float(energy_hold[0]),)
				step = step + 1
	step=0
	for x in all_power:
			power_hold = all_power[x]
			if all_power[x]:
				power = power + (float(power_hold[0]),)
				step = step + 1

	#GENERATE PLOT AND RETURN IT TO EXTRACTDATA
	f2 = plt.figure()
	ax2 = f2.add_subplot(111)
	ax2.scatter(energy, power)
	plt.ylabel('Energy Density (W-h/kg)')
	plt.xlabel('Power Density (W/kg)')
	return plt

def ExtractProfiles(profdir, conc_profile, j_profile, overpot_profile):
	
	#OPEN FILE INSIDE SLECTED DIRECTORY
	if os.path.isdir('%s/Conc_Profiles' % profdir)==False:
		os.system('mkdir %s/Conc_Profiles' % profdir)
	if os.path.isdir('%s/ButlerVolmer_Profiles' % profdir)==False:
		os.system('mkdir %s/ButlerVolmer_Profiles' % profdir)
	if os.path.isdir('%s/Overpotential_Profiles' % profdir)==False:
		os.system('mkdir %s/Overpotential_Profiles' % profdir)
	f = open('%s/profiles.out' % profdir, 'r+')
	profiles = f.readlines()
	f.close()
	
	count = 0
	#CREATE DICTIONARIES TO HOLD EACH PROFILE
	thickness = {}
	concentration = {}
	jmain = {}
	overpot = {}
	
	
	#COUNT NUMBER OF PROFILES
	pcount = 1
	for line in profiles:
		lst = line
		lst = lst.strip()
		lst = lst.replace(" ","")
		lst = lst.replace("-0.0","0.0")
		lst = lst.split(',')
		if IsNumeric(lst)==True:
			tuple(lst)
			
			#EXTRACT PROFILES
			if lst[0]=='.0':
				key = 'profile_%s' % (str(pcount).zfill(4))
				thickness[key] = ()
				concentration[key] = ()
				jmain[key] = ()
				overpot[key] = ()
				pcount=pcount+1
				thickness[key] = thickness[key] + (lst[0],)
				concentration[key] = concentration[key] + (lst[1],)
				overpot[key] = overpot[key] + (lst[3],)
				jmain[key] = jmain[key] + (lst[6],)
			else:
				#key = 'profile_%s' % str(pcount).zfill(4)
				thickness[key] = thickness[key] + (lst[0],)
				concentration[key] = concentration[key] + (lst[1],)
				jmain[key] = jmain[key] + (lst[6],)
				overpot[key] = overpot[key] + (lst[3],)
			
	#print max(overpot['profile_0800']) #IS NOT PRINTING ACTUAL MAX

	
	
	#GENERATE .PNG PROFILE SNAPSHOTS
	z = range(1, pcount)
	
	conc_maxes = ()
	conc_mins = ()
	jmain_maxes = ()
	jmain_mins = ()
	overpot_maxes = ()
	overpot_mins = ()
	
	#FIND MAXES/MINS IN EACH KEY
	#NEed to go through dictionary using the dictionary thing
	for x in z:
		conc_maxes = conc_maxes + (max(concentration['profile_%s' % str(x).zfill(4)]),)
		conc_mins = conc_mins + (min(concentration['profile_%s' % str(x).zfill(4)]),)
		jmain_maxes = jmain_maxes + (max(jmain['profile_%s' % str(x).zfill(4)]),)
		jmain_mins = jmain_mins + (min(jmain['profile_%s' % str(x).zfill(4)]),)
		overpot_maxes = overpot_maxes + (max(overpot['profile_%s' % str(x).zfill(4)]),)
		overpot_mins = overpot_mins + (min(overpot['profile_%s' % str(x).zfill(4)]),)
	


	
	
	
	overpot_max = float(max(overpot['profile_0001']))
	for x in z:
		for y in overpot['profile_%s' % str(x).zfill(4)]:
			if overpot_max < float(y):
				overpot_max = float(y)
	overpot_max = overpot_max + (overpot_max*0.05)
	
	overpot_min = float(min(overpot['profile_0001']))
	for x in z:
		for y in overpot['profile_%s' % str(x).zfill(4)]:
			if overpot_min > float(y):
				overpot_min = float(y)
	overpot_min = overpot_min - (overpot_min*0.05)
	
	conc_max = float(max(concentration['profile_0001']))
	for x in z:
		for y in concentration['profile_%s' % str(x).zfill(4)]:
			if conc_max < float(y):
				conc_max = float(y)
	conc_max = conc_max + (conc_max*0.05)
	
	conc_min = float(min(concentration['profile_0001']))
	for x in z:
		for y in concentration['profile_%s' % str(x).zfill(4)]:
			if conc_min > float(y):
				conc_min = float(y)
	conc_min = conc_min - (conc_min*0.05)
	
	jmain_max = float(max(jmain['profile_0001']))
	for x in z:
		for y in jmain['profile_%s' % str(x).zfill(4)]:
			if jmain_max < float(y):
				jmain_max = float(y)
	jmain_max = jmain_max + (jmain_max*0.05)
	
	jmain_min = float(min(jmain['profile_0001']))
	for x in z:
		for y in jmain['profile_%s' % str(x).zfill(4)]:
			if jmain_min > float(y):
				jmain_min = float(y)
	jmain_min = jmain_min - (jmain_min*0.05)
	
			
	
	#print overpot_max
	#print overpot_min
	#print conc_max
	#print conc_min
	#print jmain_max
	#print jmain_min
	
	thick_len = len(thickness['profile_%s' % str(1).zfill(4)])
	thick_max_hold = thickness['profile_%s' % str(1).zfill(4)]
	thick_max = float(thick_max_hold[thick_len-1])
	
	owd = os.getcwd()
		
	if overpot_profile==True:
		for x in z[::3]:
			a = x
			x = plt.figure()
			ax = x.add_subplot(111)
			ax.plot(thickness['profile_%s' % str(a).zfill(4)], overpot['profile_%s' % str(a).zfill(4)], linewidth=3.0)
			plt.xlabel('Thickness (microns)')
			plt.ylabel('Overpotential (V)')
			plt.ylim([float(overpot_min), float(overpot_max)])
			plt.xlim([0.0, thick_max])
			x.savefig('%s/Overpotential_Profiles/profile_%s.png' % (profdir, str(a).zfill(4)))
			plt.close(x)
		os.chdir('%s/Overpotential_Profiles' % profdir)
		os.system('convert -delay 10 profile*.png overpotential_profile.mpeg')
		os.chdir(owd)
	
	
	
	if conc_profile==True:	
		for x in z[::3]:
			a = x
			x = plt.figure()
			ax = x.add_subplot(111)
			ax.plot(thickness['profile_%s' % str(a).zfill(4)], concentration['profile_%s' % str(a).zfill(4)], linewidth=3.0)
			plt.xlabel('Thickness (microns)')
			plt.ylabel('Concentration (mol/m3)')
			plt.ylim([float(conc_min), float(conc_max)])
			plt.xlim([0.0, thick_max])
			x.savefig('%s/Conc_Profiles/profile_%s.png' % (profdir, str(a).zfill(4)))
			plt.close(x)
		
		#CONVERT SNAPSHOTS TO VIDEO
		os.chdir('%s/Conc_Profiles' % profdir)
		os.system('convert -delay 10 profile*.png conc_profile.mpeg')
		os.chdir(owd)
		
		
	if j_profile==True:
		for x in z[::3]:
			a = x
			x = plt.figure()
			ax = x.add_subplot(111)
			ax.plot(thickness['profile_%s' % str(a).zfill(4)], jmain['profile_%s' % str(a).zfill(4)], linewidth=3.0)
			plt.xlabel('Thickness (microns)')
			plt.ylabel('Current Density (A/m2)')
			plt.ylim([float(jmain_min), float(jmain_max)])
			plt.xlim([0.0, thick_max])
			#plt.ylim([-60, float(jmain_max)])
			#plt.xlim([0.0, thick_max])
			x.savefig('%s/ButlerVolmer_Profiles/profile_%s.png' % (profdir, str(a).zfill(4)))
			plt.close(x)
		#CONVERT SNAPSHOTS TO VIDEO
		os.chdir('%s/ButlerVolmer_Profiles' % profdir)
		os.system('convert -delay 10 profile*.png j_profile.mpeg')	
		os.chdir(owd)			


def ExtractData(xvar, yvar, ragone, conc_profile, j_profile, profdir, overpot_profile):
	#GET DIRECTORIES
	dirs = GetDirectories()	
	
	#INITIALIZE OUTPUT DICTIONARIES
	all_time = {}
	for x in dirs:
		all_time[x] = ()
	all_potential = {}
	for x in dirs:
		all_potential[x] = ()
	all_cath = {}
	for x in dirs:
		all_cath[x] = ()
	all_anode = {}
	for x in dirs:
		all_anode[x] = ()
	all_energy = {}
	for x in dirs:
		all_energy[x] = ()		
	all_power = {}
	for x in dirs:
		all_power[x] = ()
	all_current = {}
	for x in dirs:
		all_current[x] = ()
	all_capacity = {}
	for x in dirs:
		all_capacity[x] = ()
	norm_cap = {}
	for x in dirs:
		norm_cap[x] = ()
	all_maxes = ()
		
	
	#LOOP THROUGH DIRECTORIES
	for x in dirs:
		dirdict_hold = dirdict[x]()
		#DETERMINE WHICH BOOLS WERE SELECTED
		if dirdict_hold == True:
			#OPEN FILE INSIDE SLECTED DIRECTORY
			f = open('%s/dualfoil5.out' % x, 'r+')
			data = f.readlines()
			f.close()
			#LOOP THROUGH ALL DATA LINES
			for line in data:
				#REMOVE ALL WHITESPACE/0'S AND SPLIT
				lst = line
				lst = lst.strip()
				lst = lst.split(',')
				#DETERMINE IF ALL STRINGS IN LIST ARE NUMERICAL
				if IsNumeric(lst)==True:
					#BUILD DATA
					all_time[x] = all_time[x] + (lst[0],)
					all_anode[x] = all_anode[x] + (lst[1],) 
					all_cath[x] = all_cath[x] + (lst[2],) 
					all_potential[x] = all_potential[x] + (lst[3],)
					all_current[x] = all_current[x] + (lst[5],)
					capacity = (float(lst[0]) * float(lst[5]))/60
					all_capacity[x] = all_capacity[x] + (str(capacity),)
			
				
				else:
					#CHECK FIRST ELEMENT FOR 'ENERGY' AND 'POWER'
					hold = lst[0]
					hold = hold.split(" ")

					if hold[0]=='energy':
						lst_new = filter(None, hold)											
						all_energy[x] = all_energy[x] + (lst_new[2],)
					elif hold[0]=='power':
						lst_new = filter(None, hold)						
						all_power[x] = all_power[x] + (lst_new[2],)
		
			#NORMALIZE CAPACITY
			try:
				norm_cap[x] = list(all_capacity[x])
				norm_cap[x] = [float(i) for i in norm_cap[x]]
				all_maxes = all_maxes + (max(norm_cap[x]),)
			except:
				tkMessageBox.showinfo(title='Run ', 
	                                    message='Run %s did not converge.' % x)
		
	all_maxes = list(all_maxes)
	cap_max = max(all_maxes)
	for x in dirs:
		norm_cap[x] = [float(i)/cap_max for i in norm_cap[x]]
	
	
	#USER INPUT FOR X VARIABLE
	if xvar==XVAR_OPT[0]:
		xvar=all_time
		xlabel='Time (min)'
	elif xvar==XVAR_OPT[1]:
		xvar=all_capacity
		xlabel='Capacity (A*h/m^2)'
	elif xvar==XVAR_OPT[2]:
		xvar=norm_cap
		xlabel='Normalized Capacity'
	elif xvar==XVAR_OPT[3]:
		xvar=all_potential
		xlabel='Cell Potential (V)'
	elif xvar==XVAR_OPT[4]:
		xvar=all_anode
		xlabel='Anode Utilization'
	elif xvar==XVAR_OPT[5]:
		xvar=all_cath
		xlabel='Cathode Utilization'

		
	#USER INPUT FOR Y VARIABLE
	if yvar==YVAR_OPT[0]:
		yvar=all_potential
		ylabel='Cell Potential (V)'		
	elif yvar==YVAR_OPT[1]:
		yvar=all_capacity
		ylabel='Capacity (A*h/m^2)'
	elif yvar==YVAR_OPT[2]:
		yvar=norm_cap
		ylabel='Normalized Capacity'
	elif yvar==YVAR_OPT[3]:
		yvar=all_anode
		ylabel='Anode Utilization'
	elif yvar==YVAR_OPT[4]:
		yvar=all_cath
		ylabel='Cathode Utilization'

	
	f1 = plt.figure()
	ax1 = f1.add_subplot(111)
	for x in dirs:
		dirdict_hold = dirdict[x]()
		if dirdict_hold == True:
			ax1.plot(xvar[x], yvar[x], label='%s' % x, linewidth=3.0)
	if len(dirs) <= 5:
		plt.legend()
	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	
	if ragone==True:
		Ragone(all_power, all_energy)
	if conc_profile==True or j_profile==True or overpot_profile==True:
		check_input=False
		for x in dirs:
			if profdir == x:
				check_input=True	
			else:
				pass
		if check_input==True:
			ExtractProfiles(profdir, conc_profile, j_profile, overpot_profile)
		else:
			tkMessageBox.showinfo(title='Error', message='Directory "%s" does not exist or contains no data.' % profdir)



	
	plt.show()


p=Parser(title='Visualization')
##-----------------------------------------------------------------------

#CREATE PARSER AND MENUS



welcome = Menu(title='Welcome', parser=p)
visdir = Menu(title='Directory Selection', parser=p)
vis = Menu(title='Electrochemical Response', parser=p)
prof = Menu(title='Battery Profiles', parser=p)




#CREATE PARAMETERS FOR WELCOME TAB
Parameter(name='', variable='label', menu=welcome)
Parameter(name='', variable='label', menu=welcome, default='Welcome to the Visualization Suite.\n' +\
		'_________________________________________\n\n\n' +\
		'You can use the "Menus" tab in the top\n' +\
		'left to navigate between windows.')
Parameter(name='', variable='label', menu=welcome)
Parameter(name='', variable='label', menu=welcome)

#CREATE PARAMETERS FOR DIRECTORY SELECTION TAB

dirs = GetDirectories() 
dirdict = {}

Parameter(name='', display_name='Directory Selection', variable='label', menu=visdir)
Parameter(name='', display_name='_________________________________________', variable='label', menu=visdir)

if len(dirs) <= 10:
	Parameter(name='', variable='label', menu=visdir)
	Parameter(name='', display_name='Select data repositories to extract from:', variable='label', menu=visdir)
	Parameter(name='', variable='label', menu=visdir)
	for x in dirs:
		key = '%s' % x
		dirdict[key] = Parameter(name='%s' % x, menu=visdir, variable=bool, default=True)
	Parameter(name='', variable='label', menu=visdir)

else:
	for x in dirs:
		key = '%s' % x
		dirdict[key] = Parameter(name='%s' % x, parser=p, variable=bool, default=True)
	
	Parameter(name='', display_name='Manual selection disabled: too many repositories (>10).', menu = visdir, variable='label')
	Parameter(name='', display_name='***All repositories will be visualized.***', menu = visdir, variable='label')
	Parameter(name='', variable='label', menu=visdir)
	#tkMessageBox.showinfo(parent=window, message='Too many directories for manual selection;' +\
		#' all output directories will be visualized.')

Parameter(name='', display_name='Use "Menus" tab to navigate to Visualization.', variable='label', menu=visdir)
Parameter(name='', variable='label', menu=visdir)


#CREATE PARAMETERS FOR VISUALIZATION TAB

#OPTIONS FOR Y VARIABLE DROP DOWN MENU
YVAR_OPT = ('Cell Potential (V)', 'Capacity (A*h/m^2)', 'Normalized Capacity', 'Anode Utilization', 'Cathode Utilization') 
XVAR_OPT = ('Time (min)', 'Capacity (A*h/m^2)', 'Normalized Capacity', 'Cell Potential', 'Anode Utilization', 'Cathode Utilization') 

	
Parameter(name='dirdict', variable=str, parser=p, default=(dirdict))



Parameter(name='yvar', display_name='y-axis variable:', menu=vis, variable=tuple,\
		default=(YVAR_OPT))

Parameter(name='xvar', display_name='x-axis variable:', menu=vis, variable=tuple,\
		default=(XVAR_OPT))
Parameter(name='', variable='label', menu=vis)
Parameter(name='ragone', display_name='Generate Ragone scatter plot?', variable=bool, menu=vis, default=False)
Parameter(name='', variable='label', menu=vis)

#CREATE PARAMETERS FOR BATTERY PROFILES

Parameter(name='', variable='label', menu=prof)
Parameter(name='conc_profile', display_name='Generate concentration profile video?', menu=prof, variable=bool, default=False)
Parameter(name='j_profile', display_name='Generate Butler-Volmer profile video?', menu=prof, variable=bool, default=False)
Parameter(name='overpot_profile', display_name='Generate overpotential profile video?', menu=prof, variable=bool, default=False)
Parameter(name='profdir', display_name='Enter repository to extract profiles from:', menu=prof, variable=str,\
			default='Output')
Parameter(name='run_function', display_name='Create plot(s)', variable='function', default=ExtractData,\
			menu=prof)
Parameter(name='', variable='label', menu=prof)

if p.is_gui_mode()==False:
	p.add_command(ExtractData)
else:
	pass
p()
