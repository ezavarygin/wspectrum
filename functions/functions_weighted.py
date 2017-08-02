#!/usr/bin/env python

from astropy.io import fits
from glob import glob
import numpy as np




def make_dict(filepath):
    """
    The module is to create a dictionary.
    
    The dictionary structure is as follows: key=QSO name: value=[vel. off-set, binning, deckname].
    """
    with open(filepath,'r') as f:
        data = f.read().split('\n')
    qso_dict = dict()
    for line in data:
        qso_dict[line.split()[0]] = float(line.split()[1])
    return qso_dict


def find_anchor(file_list,shift_path):
    """
    The module is to find the anchor spectrum.
    
    The anchor spectrum is taken as one specified in the first line of 'voffset_result_bin.dat' file.
    """
    with open(shift_path,'r') as f:
        data = f.read().split('\n')[0]
    anchor_name = data.split()[0]
    for i,file in enumerate(file_list):
        if file.split('/')[-1] == anchor_name:
            i_an = i
            break
    else:
        print "========================================================================="
        print " Warning: the anchor spectrum '{}' was not specified!".format(anchor_name)
        print "========================================================================="
        quit()
    return file_list[i_an]


def group_print(file_list):
    """
    The module is to print names of spectra by groups.

    The spectra are grouped according to instrumental set-ups: binning and deckname.
    """
    print ""
    print "=============== wspectrum ==============="
    print ""
    print "'--group' was specified!"
    print ""
    print "Spectra grouped by instrumental set-ups:"
    print "........................................."
    spec_setup_dict = {}
    for path in file_list:
        name = path.split('/')[-1]
        # find a path to the corresponding raw fits-file
        find_path = glob('/Users/z5093467/ASTRO/reduction/HIRES/J101155+294141/HI.????????/sci/' + name)[0]
        fits_open = fits.open(find_path)
        deckname  = fits_open[0].header['deckname']
        if len(fits_open) == 4:
            binning = fits_open[0].header['binning'][-1]
        else:
            binning = fits_open[0].header['binning'][0]
        spec_setup_dict[name] = [str(binning),str(deckname)]
    fits_open.close()
    name_list = spec_setup_dict.keys()
    while len(name_list) > 0:
        spec_name = name_list[0]
        binning   = spec_setup_dict[spec_name][0]
        deckname  = spec_setup_dict[spec_name][1]
        print "Set-ups: binning = {}, slit = {}".format(binning,deckname)
        print ""
        for key, value in sorted(spec_setup_dict.iteritems()):
            if value[0] == binning and value[1] == deckname:
                print key #, value
                name_list.remove(key)
            else:
                pass
        print "........................................."

def voffset_bin(path_to_file):
    """
    The module is to extend 'voffset' output file with instrument set-ups. 

    The file voffset_setups.dat is created which contains 4 columns:
    (1) file name of a spectrum, 
    (2) velocity off-set,
    (3) binning in the dispersion direction,
    (4) decker name.
    """
    with open(path_to_file,'r') as f:
        data = f.read().split('\n')
    if path_to_file.split('/')[-1] == 'voffset_setups.dat':
        print "=============================================================================="
        print ""
        print "Warning: 'voffset_setups.dat' is reserved for the output file!"
        print ""
        print "Change either the input file name, or rename an output file name."
        print "In order to do the latter, modify a corresponding line in the"
        print "'funcions_weighted.voffset_bin' module!"
        print "=============================================================================="
        quit()
    else:
        pass
    new_file = open('voffset_setups.dat','w')
    for i,line in enumerate(data):
        name = line.split()[0]
        # find a path to the corresponding raw fits-file
        find_path = glob('/Users/z5093467/ASTRO/reduction/HIRES/J101155+294141/HI.????????/sci/' + name)[0]
        fits_open = fits.open(find_path)
        deckname = fits_open[0].header['deckname']
        if len(fits_open) == 4:
            binning = fits_open[0].header['binning'][-1]
        else:
            binning = fits_open[0].header['binning'][0]
        if i != len(data)-1:
            new_file.write(line + ' ' + str(binning) + ' ' + str(deckname) + '\n')
        else:
            new_file.write(line + ' ' + str(binning) + ' ' + str(deckname))
    fits_open.close()
    new_file.close()


def detail_wl_array(old_array,resol):
    """
    The module is to create a new, with smaller step, wavelength array.
    
    (resol-1) - number of subpixels between the old pixels.
    """
    new_list = []
    len_old = len(old_array)
    resol_rev = 1./resol
    for i in range(len_old):
        new_list.append(old_array[i])
        if i != len_old-1:
            for j in range(1,resol):
                new_list.append(old_array[i] + resol_rev*j*(old_array[i+1] - old_array[i]))
    return np.array(new_list)

