#!/usr/bin/env python

from astropy.io import fits
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

