### Package to parse the GSM code from Alejandro Aviles Cervantes

import numpy as np
import matplotlib.pyplot as plt


### Part for CAMB

import sys, platform, os,subprocess
import camb
from camb import model, initialpower
print('Using CAMB %s installed at %s'%(camb.__version__,os.path.dirname(camb.__file__)))



## Functions definitions. In this version we will define functions and not a class. Maybe will change if provide easier use.
#path_gsm = '/Users/sebinouf/Dropbox/My_python/gsm/'
# Since we do not add an argument that allow to execute gsm from other place:
path_gsm='./' 


    

##### Redshift of study 

def generate_ps(proc, H0=67.5, ombh2=0.022, omch2=0.122, omnuh2=0.066, omk=0, As=2.142e-9, ns=0.9667, z=[0.97], khmin=0.0001, khmax=25., nbk=1000):
#    pars = camb.CAMBparams() ### Probably have to be external and define just one time in order to speed-up
     
    pars=camb.read_ini(os.path.join('params_Planck15Table4LastColumn_copy.ini'))
    results = camb.get_background(pars)
     
#    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, omnuh2=omnuh2, tau=0.06)
#    pars.InitPower.set_params(As=As, ns=ns, r=0)
#    pars.set_matter_power(redshifts=z)
#    results = camb.get_results(pars)
    kh, z, pk = results.get_matter_power_spectrum(minkh=khmin, maxkh=khmax, npoints = nbk)
    np.savetxt(path_gsm+'Input/ps_%d.txt'%proc, np.array( (kh, pk[0])).T)

    
    
    return({'kh':kh, 'z':z, 'pk':pk})
    
    
    
def run_gsm(proc,  pk_name='', Om=0.28, h=0.68, zout=0.97,b1=0., b2=0., sigma2eft=-2, smin=1., smax=200., Ns=140, remove=True ):
    
    
    args_exe = [path_gsm+'gsm', 'Om=%f'%Om, 'h=%f'%h, 'b1=%f'%b1, 'b2=%f'%b2, 'sigma2eft=%f'%sigma2eft, 'zout=%f'%zout, 'Ns=%f'%Ns, 'smin=%f'%smin,
                  'smax=%f'%smax, 'suffixModel=_%d'%proc ]
    if pk_name != '': args_exe.append('fnamePS=%s'%pk_name)
    res_proc = subprocess.call(args_exe)
    ### Part to read the data and then remove the file 
    name_read = path_gsm+'rsd_multipoles_%d'%proc+'.dat'
    data = np.loadtxt(name_read, skiprows=3).T
    
    
    line_results = np.loadtxt(name_read, skiprows=0, max_rows=1,comments=['$'], usecols=(4), dtype=np.str, delimiter=',')
    my_string_date = str(line_results).replace(' f=', '')
    fv =float(my_string_date)
    
    


    line_results = np.loadtxt(name_read, skiprows=0, max_rows=1,comments=['$'], usecols=(10), dtype=np.str, delimiter=',')
    my_string_date = str(line_results).replace(' s2FoG=', '')
    sigma =float(my_string_date)
      
    
    
    
    
    if remove==False:
        ## Remove the rsd results
        args_rm = ['rm', 'rsd_multipoles_%d'%proc+'.dat']
        subprocess.call(args_rm)
        ## Remove all the intermediate results in Output
        args_rm = ['rm', 'Output/clpt_%d'%proc+'.dat', 'Output/kfunctions_%d'%proc+'.dat','Output/PSL_%d'%proc+'.dat', 
                   'tmp/tables_%d'%proc+'.dat', 'Output/qfunctions_%d'%proc+'.dat', 'tmp/params_%d'%proc+'.dat'  ]
        subprocess.call(args_rm)
        ## Remove the linear power spectrum in Input
        args_rm = ['rm','Input/ps_%d'%proc+'.txt' ]
        subprocess.call(args_rm)
    
    
    
    return({'s':data[0], 'mono':data[1], 'quad':data[2], 'hexa':data[3],  'fv':fv ,  'sigma':sigma} )


def Plot_res(res, lw=4):
    plt.figure(figsize=(12,10))
    plt.plot(res['s'], res['s']**2*res['mono'], label=r'$\xi_{0}(s)\times s^2$', color='purple', lw=lw)
    plt.plot(res['s'], res['s']**2*res['quad'], label=r'$\xi_{2}(s)\times s^2$', color='salmon', lw=lw)
    plt.plot(res['s'], res['s']**2*res['hexa'], label=r'$\xi_{4}(s)\times s^2$', color='lightgreen', lw=lw)
    plt.xlabel(r'$s$', fontsize=20)
    plt.ylabel(r'$\xi_{i}(s)\times s^2$', fontsize=20)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.legend(fontsize=22)
    plt.show()


