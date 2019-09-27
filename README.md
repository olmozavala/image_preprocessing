Preprocessing MIM data
================
This software is used to preprocess MRI images that have been downloaded with the MIM software. 
The two main objectives of this program are:
* **Reorder folder (ReorderFolders.py)**. This program will read every MRI series for different patients in
different dates and will move them to an sequential numbering folders which are easier to analyze. It also
anonymize a section of the folder names, to remove patient information. 
* **Preprocess data (Preprocessing.py)**. This program changes the original format of the images (DICOM) into 
a more commonly used format in the Medical Imaging world (NRRD). Additionally, with this program we separate
the desired contours into separate binary masks. With this program you can also perform important enhancements
on the images and contours like: normalization, bias correction, resampling, cropping, etc. 

Install
================
conda 
-------
```
conda instal python=3.5
conda install -c conda-forge pydicom 
conda install -c simpleitk simpleitk 
```
Conda  from requirements.txt file (linux)
-------
`
while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirementsT.txt
`

pip
-------

`
pip3 install --user numpy pydicom pandas 
`

RUN
=================

In order to run the code, copy the file `Example_MainConfig.py` into `MainConfig.py` and update the desired parameters
with information from your computer and your dataset. 

Our common pipeline is that the cases downloaded from MIM are first stored in a folder `MIM_ORIGINAL` then, 
the output of the first program `ReorderFolders.py` is stored in `MIM_ORGANIZED_NO_DATE` and the
output of the second program `Preprocessing.py` is stored in `Preproc` folder. 
