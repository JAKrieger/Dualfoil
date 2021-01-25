 # ############################################################################
 # FILE: visualize.py
 #
 #  Authors: Lucas Darby Robinson, R. Edwin García
 #       Copyright 2015
 #  Author: Jonas A. Krieger <econversion@empa.ch>
 #       Copyright 2021
 # 
 # ############################################################################
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider as pltSlider
from VKML.gui.tk import Parameter, Parser, Menu,DropDownMenu
# import pylab 
import tkinter.messagebox as tkMessageBox
import tkinter as tk
import os, sys
# import os.path
from time import sleep

    
def GetDirectories(path): 
    dirs=()
    for foldername in os.listdir(path):
        if os.path.isdir(os.path.join(path,foldername)):
            dirs+=(foldername,)
    return dirs

def IsNumeric(lst):
    if not len(lst): return False
    #FOR EACH VALUE FROM 0 TO LENGTH OF LINE
    for x in range(len(lst)):
        try:
            #TRUE IF NUMERICAL
            float(lst[x])
            return True #This seems a bit dubious, as it only requires one numerical value in the list.
        except ValueError:
            #FALSE IF NOT NUMERICAL
            return False         
            
class ProfileFigure :
    '''Helper class to produce responsive figures of depth profiles
       Otherwise the sliders seem to have a problem with their scopes.'''
    
    def __init__(self,profdir, profiles, conc_profile, saturation_profile, j_profile, overpot_profile,solpot_profile, icur_profile):
        
        num_subplots=conc_profile+saturation_profile+ j_profile+ overpot_profile+solpot_profile+ icur_profile
    
        #CREATE DICTIONARIES TO HOLD EACH PROFILE
        self.thickness = {}
        self.concentration = {}
        self.csol={}
        self.jmain = {}
        self.overpot = {}
        self.solpot = {}
        self.icur ={}
        
       # keep track of times
        self.profile_times={}
        
        #COUNT NUMBER OF PROFILES
        pcount = 1
        for line in profiles:
            lst = line
            lst = lst.strip()
            lst = lst.replace(" ","")
            #lst = lst.replace("-0.0","0.0")
            lst = lst.split(',')
            if IsNumeric(lst)==True:
                lst=[float(x) for x in lst]
                
                #EXTRACT PROFILES
                if lst[0]<1e-9:
                    key = 'profile_%s' % (str(pcount).zfill(4))
                    self.thickness[key] = ()
                    self.concentration[key] = ()
                    self.csol[key] = ()
                    self.jmain[key] = ()
                    self.overpot[key] = ()
                    self.solpot[key] = ()
                    self.icur[key] = ()
                    pcount=pcount+1
                    self.thickness[key] = self.thickness[key] + (lst[0],)
                    self.concentration[key] = self.concentration[key] + (lst[1],)
                    self.csol[key] = self.csol[key] + (lst[2]*100,)
                    self.overpot[key] = self.overpot[key] + (lst[3],)
                    self.solpot[key] = self.solpot[key] + (lst[4],)
                    self.icur[key] = self.icur[key] + (lst[5],)
                    self.jmain[key] = self.jmain[key] + (lst[6],)
                else:
                    #key = 'profile_%s' % str(pcount).zfill(4)
                    self.thickness[key] = self.thickness[key] + (lst[0],)
                    self.concentration[key] = self.concentration[key] + (lst[1],)
                    self.csol[key] = self.csol[key] + (lst[2]*100,)
                    self.overpot[key] = self.overpot[key] + (lst[3],)
                    self.solpot[key] = self.solpot[key] + (lst[4],)
                    self.icur[key] = self.icur[key] + (lst[5],)
                    self.jmain[key] = self.jmain[key] + (lst[6],)
            
            
            elif lst[0][0:2]=='t=':
                try:
                    key = 'profile_%s' % (str(pcount).zfill(4))
                    self.profile_times[key]=float(lst[0][2:-3])
                except Exception:
                    pass
                    
         
        
        
        #GENERATE .PNG PROFILE SNAPSHOTS
        z = range(1, pcount)

        #Simplify the original maximum/minimum determination
        def minmax_value(paramdict):
            p_max = float(max(paramdict['profile_0001']))
            p_min=p_max
            for x in z:
                for y in paramdict['profile_%s' % str(x).zfill(4)]:
                    if p_max < float(y): p_max = float(y)
                    if p_min > float(y): p_min = float(y)
            return p_min*0.95,p_max*1.05

        overpot_min, overpot_max =  minmax_value(self.overpot)
        conc_min, conc_max =  minmax_value(self.concentration)
        csol_min, csol_max =  minmax_value(self.csol)
        jmain_min, jmain_max =  minmax_value(self.jmain)
        solpot_min, solpot_max =  minmax_value(self.solpot)
        icur_min, icur_max =  minmax_value(self.icur)
        

        thick_len = len(self.thickness['profile_%s' % str(1).zfill(4)])
        thick_max_hold = self.thickness['profile_%s' % str(1).zfill(4)]
        thick_max = float(thick_max_hold[thick_len-1])
        
#        owd = os.getcwd()
            
        self.fig=plt.figure(num='Profiles '+profdir)
        plt.clf()
        self.fig, self.axs = plt.subplots(num_subplots,sharex=True,num='Profiles '+profdir,squeeze=False)
        plt.subplots_adjust(bottom=0.2)
        
        self.updates=[]#Functions to update plot with the slider
        
        
        key='profile_%s' % str(1).zfill(4)   
        if key in self.profile_times.keys():
            self.axs[0][0].set_title('t = {:3} min'.format(self.profile_times[key]))
        else:
            self.axs[0][0].set_title('t = undefined')
        
        
        subplot=0#increment
        
        
        if solpot_profile==True:
            ax=self.axs[subplot][0]
            subplot+=1
            self.l1a, = ax.plot(self.thickness[key], self.solpot[key], linewidth=3.0) 
            ax.set_ylabel('Potential (V)')
            ax.set_ylim([float(solpot_min), float(solpot_max)])

            def update(key):
                self.l1a.set_data(self.thickness[key],self.solpot[key])
            self.updates.append(update)
        
        if overpot_profile==True:
            ax=self.axs[subplot][0]
            subplot+=1
            self.l1, = ax.plot(self.thickness[key], self.overpot[key], linewidth=3.0) 
            ax.set_ylabel('Overpotential (V)')
            ax.set_ylim([float(overpot_min), float(overpot_max)])

            def update(key):
                self.l1.set_data(self.thickness[key],self.overpot[key])
            self.updates.append(update)
            
        if conc_profile==True: 
            ax=self.axs[subplot][0]
            subplot+=1
            self.l2, = ax.plot(self.thickness[key], self.concentration[key], linewidth=3.0)            
            ax.set_ylabel('Concentration (mol/m3)')
            ax.set_ylim([float(conc_min), float(conc_max)])

            def update(key):
                self.l2.set_data(self.thickness[key],self.concentration[key])
            self.updates.append(update)   

         
        if saturation_profile==True: 
            ax=self.axs[subplot][0]
            subplot+=1
            self.l2b, = ax.plot(self.thickness[key], self.csol[key], linewidth=3.0)            
            ax.set_ylabel('Saturation (%)')
            ax.set_ylim([float(csol_min), float(csol_max)])

            def update(key):
                self.l2b.set_data(self.thickness[key],self.csol[key])
            self.updates.append(update)  
            
        if j_profile==True:
            ax=self.axs[subplot][0]
            subplot+=1
            self.l3, = ax.plot(self.thickness[key], self.jmain[key], linewidth=3.0)   
            ax.set_ylabel('Current density (A/m^2)')
            ax.set_ylim([float(jmain_min), float(jmain_max)])

            def update(key):
                self.l3.set_data(self.thickness[key],self.jmain[key])
            self.updates.append(update)   
            
        if icur_profile==True:
            ax=self.axs[subplot][0]
            subplot+=1
            self.l4, = ax.plot(self.thickness[key], self.icur[key], linewidth=3.0)   
            ax.set_ylabel('Ionic current density (A/m^2)')
            ax.set_ylim([float(icur_min), float(icur_max)])

            def update(key):
                self.l4.set_data(self.thickness[key],self.icur[key])
            self.updates.append(update) 
            
        ax.set_xlim([0.0, thick_max])
        ax.set_xlabel('Thickness (microns)') 
        #Construct Slider
        def update(val):
            try: #Otherwise the slider seems to silently crash, if e.g. a key is missing
                key='profile_%s' % str(int(val)).zfill(4)
                for f in self.updates: f(key)
                self.fig.canvas.draw_idle()
                if key in self.profile_times.keys():
                    ax=self.axs[0][0]
                    ax.set_title('t = {:3} min'.format(self.profile_times[key]))
            except:pass
        self.axslider = plt.axes([0.10, 0.05, 0.8, 0.03])
        valinit=z[int(len(z)/2)]
        self.slider = pltSlider(self.axslider, 'Time', z[0], z[-1], valinit=valinit, valstep=1)
        update(valinit)
        self.slider.on_changed(update)
        
        self.axs[0][0].legend((profdir,))
        
    
    
def main():

        
    def choose_cwd():
        old_wd= os.getcwd()
        options={}
        options['title']='Choose data directory'
        options['initialdir']=directory['cwd']
        dirname = tk.filedialog.askdirectory(**options)
        if dirname=='':return #choosing was aborted
        try:  
            os.chdir('%s' % dirname)
        except Exception: 
            tkMessageBox.showinfo(title='Input Error', message="Error, couldn't change working directory to {} .".format({dirname}))
            return #failed
        if len(GetDirectories(path=os.getcwd()))<1:
            os.chdir(old_wd)
            tkMessageBox.showinfo(title='Input Error', message="Attention: {} doesn't contain any subdirectories with data. Please choose a parent directory".format({dirname}))
            return
        directory['cwd']=os.getcwd()
        update=reconstruct_visdir(dirdict,update_gui=True)
        dirdict.clear()
        dirdict.update(update)
        os.chdir(old_wd)
    
    def Ragone(all_energy, all_power):
        old_wd=os.getcwd()
        os.chdir(directory['cwd'])
        
        #GENERATE PLOT AND RETURN IT TO EXTRACTDATA
        f2 = plt.figure(num='Ragone plot')
        plt.clf()#clear figure
        ax2 = f2.add_subplot(111)
            
        for x in all_energy.keys():
            dirdict_hold = dirdict[x]()
            #DETERMINE WHICH BOOLS WERE SELECTED
            if dirdict_hold == True:
                if IsNumeric(all_energy[x]) and IsNumeric(all_power[x]):
                    ax2.scatter([abs(float(k)) for k in all_power[x]],
                                [abs(float(k)) for k in all_energy[x]],
                                label=x)
        plt.ylabel('Energy Density (W-h/kg)')
        plt.xlabel('Power Density (W/kg)')
        if len(all_energy.keys())<10:
            plt.legend(loc='best')
        os.chdir(old_wd)
        return plt
    
    def ExtractProfilesMultipleDirs( conc_profile, saturation_profile, j_profile, overpot_profile,solpot_profile, icur_profile):
        '''extract profiles from multiple direcotries and plot them, Helper function'''
        
        num_subplots=conc_profile+saturation_profile+ j_profile+ overpot_profile+solpot_profile+ icur_profile
        if not num_subplots>0:return #nothing to plot
        
        old_wd=os.getcwd()
        os.chdir(directory['cwd'])
        dirs = GetDirectories(path=directory['cwd']) 
        
        keep_figs=[]
        for profdir in dirs:
            if not dirdict[profdir]()== True: continue
            try:
                with open('%s/profiles.out' % profdir, 'r+') as f:
                    profiles = f.readlines()
            except Exception:
                tkMessageBox.showinfo(title='Error', message='File profiles.out in directory "%s" cannot be opened.' % profdir)
                continue
            #Encapsulating the plotting into another class to ensure that 
            #new local variables are defined and thereby the sliders of all 
            #figures will stay responsive.
            fig=ProfileFigure(profdir, profiles,conc_profile, saturation_profile, j_profile, overpot_profile,solpot_profile, icur_profile)
            keep_figs.append(fig)
        os.chdir(old_wd)
        plt.show()
    
    
    def ExtractData(xvar, yvar, ragone,showcycle):
        old_wd=os.getcwd()
        os.chdir(directory['cwd'])
        #GET DIRECTORIES
        dirs = GetDirectories(path=directory['cwd'])
        
        #Remove dirs that are not containing data:
        datadirs=list(dirs)
        for x in dirs:
            if not dirdict[x]()== True:
                datadirs.remove(x)
                continue
            try:
                with open('%s/profiles.out' % x, 'r+') as f:
                    pass
            except Exception:
                datadirs.remove(x)
                tkMessageBox.showinfo(title='Error', message='File profiles.out in directory "%s" cannot be opened.' % x)
                continue
        dirs=tuple(datadirs)
        
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
        all_ocv = {}
        for x in dirs:
            all_ocv[x] = ()
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
        all_en = {}
        for x in dirs:
            all_en[x] = ()
        norm_cap = {}
        for x in dirs:
            norm_cap[x] = ()
        all_temp = {}
        for x in dirs:
            all_temp[x] = ()
        all_heatgen = {}
        for x in dirs:
            all_heatgen[x] = ()
        all_maxes = ()
            
        
        #LOOP THROUGH DIRECTORIES
        for x in dirs:
            dirdict_hold = dirdict[x]()
            #DETERMINE WHICH BOOLS WERE SELECTED
            if dirdict_hold == True:
                #OPEN FILE INSIDE SLECTED DIRECTORY
                with open('%s/dualfoil5.out' % x, 'r+') as f:
                    data = f.readlines()
               
                time_prev=0
                capacity=(0,)
                energy=(0,)
                prev_current_pos=None
                #LOOP THROUGH ALL DATA LINES
                for line in data:
                    #REMOVE ALL WHITESPACE/0'S AND SPLIT
                    lst = line
                    lst = lst.strip()
                    lst = lst.split(',')
                    #DETERMINE IF ALL STRINGS IN LIST ARE NUMERICAL
                    if IsNumeric(lst)==True:
                        #For some unclear reason the last entry of a series of Galvanostatic segments has the wrong sign. Therefore, it is skipped.
                        if (showcycle==Cycle_OPT[0] or
                          (showcycle==Cycle_OPT[1] and float(lst[5])<0 and (prev_current_pos==None or not prev_current_pos)) or
                          (showcycle==Cycle_OPT[2] and float(lst[5])>0) and (prev_current_pos==None or prev_current_pos)):
                            #BUILD DATA
                            all_time[x] = all_time[x] + (float(lst[0]),)
                            all_anode[x] = all_anode[x] + (float(lst[1]),) 
                            all_cath[x] = all_cath[x] + (float(lst[2]),) 
                            all_potential[x] = all_potential[x] + (float(lst[3]),)
                            all_ocv[x] = all_ocv[x] + (float(lst[4]),)
                            all_current[x] = all_current[x] + (float(lst[5]),)
                            all_temp[x] = all_temp[x] + (float(lst[6]),)
                            all_heatgen[x] = all_heatgen[x] + (float(lst[7]),)
                            #Calculate capacity as Integral current dt
                            capacity+=(capacity[-1]+float(lst[5])*(float(lst[0])-time_prev)/60,)
                            #Calculate energy as Integral current*voltage dt
                            energy+=(energy[-1]+float(lst[3])*float(lst[5])*(float(lst[0])-time_prev)/60,)
                        
                            # all_capacity[x] = all_capacity[x] + (cap_prev,)
                            # all_en[x]=all_en[x]+(en_prev,)
                        time_prev=float(lst[0])
                        prev_current_pos=float(lst[5])>0 #Store the current direction
                    
                    else:
                        #CHECK FIRST ELEMENT FOR 'ENERGY' AND 'POWER'
                        hold = lst[0]
                        hold = hold.split(" ")
                        if len(hold)>1 and hold[1]=='energy':
                            value=[i for i in filter(None, hold)] [-2]
                            all_energy[x]+=(value,)
                            #Offset the zero of the capacity:
                            if len(capacity)>1 and (
                                    all_current[x][-1]>0 or showcycle!=Cycle_OPT[0]):
                                min_cap=min(capacity)
                                if min_cap<0: #Offset:
                                    capacity=tuple([c-min_cap for c in capacity])
                                all_capacity[x]+=capacity[1:]
                                capacity=(0,)
                                #Do the same for the energy
                                min_en=min(energy)
                                if min_en<0: #Offset:
                                    energy=tuple([e-min_en for e in energy])
                                all_en[x]+=energy[1:]
                                energy=(0,)
                        elif len(hold)>1 and hold[1]=='power':
                            value=[i for i in filter(None, hold)] [-2]
                            all_power[x] +=(value,)  
                            
                #Offset the zero of the capacity if last segment had current<0:
                if len(capacity)>1:
                    min_cap=min(capacity)
                    if min_cap<0: #Offset:
                        capacity=tuple([c-min_cap for c in capacity])
                    all_capacity[x]+=capacity[1:]
                    min_en=min(energy)
                    if min_en<0: #Offset:
                        energy=tuple([e-min_en for e in energy])
                    all_en[x]+=energy[1:]
                #NORMALIZE CAPACITY
                try:
                    norm_cap[x] = list(all_capacity[x])
                    norm_cap[x] = [float(i) for i in norm_cap[x]]
                    all_maxes = all_maxes + (max(norm_cap[x]),)
                except Exception as e:
                    tkMessageBox.showinfo(title='Run ', 
                                            message='Run %s did not converge.' % x)
            
        all_maxes = list(all_maxes)
        cap_max = max(all_maxes)
        for x in dirs:
            if cap_max!=0:
                norm_cap[x] = [float(i)/cap_max for i in norm_cap[x]]
        
        show_energy_in_legend=(yvar==YVAR_OPT[0] and xvar==XVAR_OPT[1])\
                        or ( yvar==YVAR_OPT[1] and xvar==XVAR_OPT[3])
        
        #USER INPUT FOR X VARIABLE
        if xvar==XVAR_OPT[0]:
            xvar=all_time
            xlabel='Time (min)'
        elif xvar==XVAR_OPT[1]:
            xvar=all_capacity
            xlabel='Capacity (A*h/m^2)'
        elif xvar==XVAR_OPT[2]:
            xvar=norm_cap
            xlabel='Normalized capacity'
        elif xvar==XVAR_OPT[3]:
            xvar=all_potential
            xlabel='Cell potential (V)'
        elif xvar==XVAR_OPT[4]:
            xvar=all_anode
            xlabel='Anode utilization'
        elif xvar==XVAR_OPT[5]:
            xvar=all_cath
            xlabel='Cathode utilization'
        elif xvar==XVAR_OPT[6]:
            xvar=all_ocv
            xlabel='Open circuit voltage (V)'
        elif xvar==XVAR_OPT[7]:
            xvar=all_temp
            xlabel='Temperature (°C)'
        elif xvar==XVAR_OPT[8]:
            xvar=all_heatgen
            xlabel='Heat generation (W/m^2)'
        elif xvar==XVAR_OPT[9]:
            xvar=all_current
            xlabel='Current (A/m^2)'
        elif xvar==XVAR_OPT[10]:
            xvar=all_en
            xlabel='Energy (Wh/m^2)'
    
            
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
        elif yvar==YVAR_OPT[5]:
            yvar=all_ocv
            ylabel='Open circuit voltage (V)'
        elif yvar==YVAR_OPT[6]:
            yvar=all_temp
            ylabel='Temperature (°C)'
        elif yvar==YVAR_OPT[7]:
            yvar=all_heatgen
            ylabel='Heat generation (W/m^2)'
        elif yvar==YVAR_OPT[8]:
            yvar=all_current
            ylabel='Current (A/m^2)'
        elif yvar==YVAR_OPT[9]:
            yvar=all_en
            ylabel='Energy (Wh/m^2)'
   
    
        f1 = plt.figure(num='Electrochemical Response')
        plt.clf()#clear figure
        ax1 = f1.add_subplot(111)
        for x in dirs:
            dirdict_hold = dirdict[x]()
            if dirdict_hold == True:
                #In Capacity vs potential plot, add  energy to label
                if len(all_energy[x]) and show_energy_in_legend:
                    label='{}: {} Wh/kg'.format(x,all_energy[x][0])
                    ax1.plot(xvar[x], yvar[x], 'o',label=label, ms=3.5)
                else:
                    label='%s' % x
                    ax1.plot(xvar[x], yvar[x], label=label, linewidth=3.0)
        if len(dirs) <= 5:
            plt.legend()
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        
        if ragone==True:
            Ragone(all_energy,all_power)
    
    
        os.chdir(old_wd)
        plt.show()

    p=Parser(title='Visualization')
    ##-----------------------------------------------------------------------
    
    #Keeping track of the current directory, which should be independent from the dualfoil.py working directory.
    # Using a dicitionary, because it has a different scope than a string.    
    directory={'cwd':os.getcwd()}

    
    #CREATE PARSER AND MENUS
    def close():
        p.gui.close()
    mFile=DropDownMenu(title='File', parser=p)
    mFile.add(func=close,label='Quit')
    
    
    # welcome = Menu(title='Welcome', parser=p)
    visdir = Menu(title='Directory Selection', parser=p,scrollable=True)
    vis = Menu(title='Electrochemical Response', parser=p)
    prof = Menu(title='Battery Profiles', parser=p)
    
    dirdict={}  
    def reconstruct_visdir(dirdict,update_gui=True):
        '''reconstruct the directory selection menu'''
        
        if update_gui:visdir.clear()

        Parameter(name='', display_name='Directory Selection', variable='function', default=choose_cwd, menu=visdir,button_text='Select parent directory')
        Parameter(name='', display_name='_________________________________________', variable='label', menu=visdir)
        Parameter(name='', variable='label', menu=visdir)
        Parameter(name='', display_name='Select data repositories to extract from:', variable='label', menu=visdir)
        Parameter(name='', variable='label', menu=visdir)
       
        dirs = GetDirectories(path=directory['cwd']) 
        dirdict_new={}
        for x in dirs:
            key = '%s' % x
            dirdict_new[key] = Parameter(name='%s' % x, menu=visdir, variable=bool, default=True)
   
        Parameter(name='', variable='label', menu=visdir)
        Parameter(name='', display_name='Use the tabs to navigate to visualization.', variable='label', menu=visdir)
        if update_gui:visdir.show()
        return dirdict_new
    # Parameter(name='', variable='label', menu=visdir)
    
    dirdict=reconstruct_visdir(dirdict,update_gui=False)
    
    #CREATE PARAMETERS FOR VISUALIZATION TAB
    
    #OPTIONS FOR Y VARIABLE DROP DOWN MENU
    YVAR_OPT = ('Cell potential (V)', 'Capacity (A*h/m^2)', 'Normalized capacity', 'Anode utilization', 'Cathode utilization', 'Open circuit voltage (V)','Temperature (°C)','Heat generation (W/m^2)','Current (A/m^2)','Energy (Wh/m^2)') 
    XVAR_OPT = ('Time (min)', 'Capacity (A*h/m^2)', 'Normalized capacity', 'Cell potential', 'Anode utilization', 'Cathode utilization', 'Open circuit voltage (V)','Temperature (°C)','Heat generation (W/m^2)','Current (A/m^2)','Energy (Wh/m^2)') 
    
        

    #Parameters to select which data to show

    Cycle_OPT = ('All data','Only charging','Only discharging')
    
    Parameter(name='yvar', display_name='y-axis variable:', menu=vis, variable=tuple,\
            default=(YVAR_OPT))
    
    Parameter(name='xvar', display_name='x-axis variable:', menu=vis, variable=tuple,\
            default=(XVAR_OPT))
    Parameter(name='', variable='label', menu=vis)
    Parameter(name='ragone', display_name='Generate Ragone plot?', variable=bool, menu=vis, default=False)
    Parameter(name='', variable='label', menu=vis)
    Parameter(name='showcycle', display_name='Show:', menu=vis, variable=tuple,\
            default=(Cycle_OPT))
    Parameter(name='', variable='label', menu=vis)
    Parameter(name='run_function', display_name='Plot', variable='function', default=ExtractData,\
                menu=vis)
    
    #CREATE PARAMETERS FOR BATTERY PROFILES

    Parameter(name='', variable='label', menu=prof)
    Parameter(name='conc_profile', display_name='Salt concentration in the electrolyte', menu=prof, variable=bool, default=True)
    Parameter(name='saturation_profile', display_name='Concentration of inserted lithium in electrode', menu=prof, variable=bool, default=False)
    Parameter(name='solpot_profile', display_name='Potential in the electrode phase', menu=prof, variable=bool, default=False)
    Parameter(name='overpot_profile', display_name='Potential in the electrolyte phase', menu=prof, variable=bool, default=False)
    Parameter(name='j_profile', display_name='Current density in the electrode', menu=prof, variable=bool, default=False)
    
    Parameter(name='icur_profile', display_name='Current density in the electrolyte', menu=prof, variable=bool, default=False)

# current density side reactions 1, 2, 3
    Parameter(name='run_function', display_name='Plot profiles', variable='function', default=ExtractProfilesMultipleDirs,\
                menu=prof)
    Parameter(name='', variable='label', menu=prof)
    
    sys.argv.append('--gui')
    if p.is_gui_mode()==False:
        p.add_command(ExtractData)
    else:
        pass
    p()
if __name__=='__main__':
    main()
