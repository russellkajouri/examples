#!/bin/python3
try:
    import os
    import numpy as np

    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except:
    raise RuntimeError('not found modules ...')

def ideal_gas(num_dens, temp):
    import scipy.constants as sc
    P = num_dens * sc.k * temp * 1e30  ## J/m^3 == Pa
    P /= sc.atm
    return P
    
def return_data(
    N : int = None,
    temp : float = None,
    path : str = None):

    if any([N, temp, path]) == None:
        raise Exception('ERORR, not defined parameters ...')

    data = []
    elements = [ element for element in os.listdir(path) if 'len_' in element ]
    

    for element in sorted(elements, key=lambda x : float(x[4:])):
        print('\tat ', element)
        local_data = np.loadtxt(f'{element}/statistics.dat')

        ## measuring the average pressure
        ## we don't consider the first 250 data point
        ave_press = np.mean(local_data[250:, 3]) 
        std_press = np.std(local_data[250:, 3])
        length    = float(element[4:])
        
        data.append([length, ave_press, std_press])
        
    else:
        print()
        data = np.array(data)
    
    return data

def Plot_the_data(
    N : int = None,
    data : np.array = None,
    path : str = None ):

    
    ## plotting the data
    
    fig, ax = plt.subplots(1,1, figsize=(4,4))
    num_dens =  N / data.T[0]**3
    
    ax.errorbar(num_dens, data.T[1], yerr = data.T[2], \
        marker='o', mfc='red', mec='black', ls='-', lw=2, c='black')
    
    ax.plot(num_dens, ideal_gas(num_dens, temp), 'k--')
    
    
    ax.tick_params(which='both', direction='in')
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    
    ax.grid(alpha=0.7, which='both')    
    ax.set_xlabel(r'$\rm \rho_n [\AA^{-3}]$')
    ax.set_ylabel(r'$\rm P [atm]$')
    
    plt.tight_layout()
    if path != None: plt.savefig('P-rho.png', dpi=300)
    plt.show()


if '__main__' == __name__:
        
        
    N       = 500
    temp    = 300
    data    = return_data(N, temp, './')
    np.savetxt('press_vs_length.dat', data, header='length[AA] press[atm] err', fmt='%.5f')
       

    ## plotting
    Plot_the_data(N, data, 'P-rho.png') 
        
    
    
