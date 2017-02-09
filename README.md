# README

## Description

The program is to co-add 1D-spectra taking into account velocity off-sets between them. It was designed to follow up the result of the [voffset](https://github.com/ezavarygin/voffset) software but can, of course, be used independently.

## Installation
The software was written to work with `python 2.7`. 
To get started, include the path to the `wspectrum` executable file into your system PATH.
That is it, you can run it from any directory on your machine.

**Python modules used:**

- astropy
- numpy
- sys
- barak
- matplotlib

## Usage

`wspectrum <list of spectra> [--anchor] [--output] [--shift]`

where:
```
<list of spectra> - List of UVES_popler output files to co-add,

```
Options:
```
--anchor - followed with a path to the anchor spectrum. It is not rebinned and its wavelength array is used as reference.

--output - followed with a name of the weighted spectrum.

--shift  - followed with a path to the file with velocity off-sets.
--plot   - overplot all the spectra including the co-added one.
```
