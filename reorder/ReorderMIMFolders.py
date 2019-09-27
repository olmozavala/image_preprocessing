import os
import shutil
from inout.io_common import create_folder

import numpy as np
from os.path import join
import pandas as pd

from platform import system
import csv
import re


class ReorderMIMFolders:
    '''
    This class reorders MIM folders by MRI series. It separates each MRI and patient into a new
    folder. It also generates a csv file with the correspondence of the original and new names
    '''
    _lut_file_name = 'File_name_correspondence.csv'  # File name of a CSV containing the relationship of file names
    _prefix_name = 'Case'  # What is the name of the final folders to be used
    _orig_folder_names = [['MR'], ['RTst']]  # RegEx of the folders that we will _search for each patient
    _new_folder_names = ['T2_TRANSVERSAL', 'CONTOURS']  # Final names of the folders, once they are reorganized
    _replace_chars = 14  # Number of characters to be removed from the original folders
    _keep_original_names = False  # Indicate we don't want to replace any character and want to keep original names
    _search_previous_names = True  # Indicate we want to continue on a previous run and it tries to read a prev CSV file

    _src_folder = 'source_folder'  # Source folder
    _dst_folder = 'dst_folder'  # Where to store the reordered folders
    _start_idx = 0  # Which index to start on the new folders

    def __init__(self, **kwargs):
        # All the arguments that are passed to the constructor of the class MUST have its name on it.
        for arg_name, arg_value in kwargs.items():
            self.__dict__["_"+arg_name] = arg_value

    def __getattr__(self, attr):
        '''Generic getter for all the properties of the class'''
        return self.__dict__["_"+attr]

    def __setattr__(self, attr, value):
        '''Generic setter for all the properties of the class'''
        self.__dict__["_"+attr] = value

    def saveLUT(self, LUT: dict):
        ''' Writes the LUT dictionary into a csv file.
        :param LUT: These is the dictionary to save
        '''
        with open(join(self._dst_folder, self._lut_file_name), 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for key in LUT.keys():
                writer.writerow([LUT[key]['Folder'], '   {}'.format(key)])

    def make_windows_path(self, dst, curr_patient):
        """ Reduces the length of the curr_patient string by the number of characters required to make
            dst path comply with MAX_PATH in Windows (260 characters).

            Arguments:
                dst = The full destination path.
                curr_patient = the curr_patient string to be reduced.
        """
        dst_str_count = len(dst)
        net_diff = dst_str_count - 180  # AB: This is arbitrary, but I found that lengths of 180 or so work nicely for not having issues
        curr_patient = curr_patient[:-net_diff]
        return curr_patient

    def read_prev_lut_file(self):
        ''' Reads a previous CSV file and sets the correct index'''
        try:
            prev_csv_file = join(self._dst_folder, self._lut_file_name)
            print(F'---- Using previous names from {prev_csv_file}')
            # Reading previous csv file
            prev_cases = pd.read_csv(prev_csv_file, header=None, names=['Cases', 'Names'], index_col=False)
            # Get last index from previous file
            last_case = prev_cases.iloc[-1][0]
            prev_last_idx = int(last_case.split('-')[1])
            last_idx = max(self._start_idx, prev_last_idx + 1)
            LUT = {}
            for ii, c_id in enumerate(prev_cases['Names'].str.strip()):
                c_case = prev_cases.iloc[ii]['Cases']
                c_case_id = int(c_case.split('-')[1])
                LUT[c_id] = {'Folder': c_case, 'id': c_case_id}

            return LUT, prev_csv_file, last_idx, True

        except Exception as e:
            print("!!!!!! Failed To read previous file {} !!!!!!".format(e))
            return {}, '', self._start_idx, False

    def organize_folders(self):
        '''
        This is the main function that organizes the folders.
        :return:
        '''
        LUT = {}
        original_date_folders = os.listdir(self._src_folder)
        original_date_folders.sort()
        last_idx = self._start_idx
        prev_file_found = False

        create_folder(self._dst_folder)

        if self._search_previous_names:
            LUT, prev_csv_file, last_idx, prev_file_found = self.read_prev_lut_file()

        # Iterate over all the source folders (dates of MIM)
        for c_date_folder in original_date_folders:
            print('******************************* {} *************************************'.format(c_date_folder))
            all_patients_in_date = os.listdir(join(self._src_folder, c_date_folder))
            only_date = c_date_folder.replace('__Studies', '')

            # Iterate folders we are _searching (a list for each image type)
            for idx_kf, keep_folder in enumerate(self._orig_folder_names):
                isNotDCE = self._new_folder_names[idx_kf] != 'DCE'

                # Iterate the hierarchy of this folder (when we are looking for multiple folders)
                for c_keep_folder in keep_folder:
                    # Search the folders that match by hierarchy
                    matched_folders = [x for x in all_patients_in_date if not (re.search(c_keep_folder, x) is None)]

                    # Iterate over matched folders
                    for c_folder in matched_folders:
                        pid = '{}_{}'.format(c_folder[0:self._replace_chars], only_date)  # Get patient id
                        if pid in LUT:  # Verify we havent 'used' this patient
                            cidx = LUT[pid]['id']
                            if self._keep_original_names:
                                curr_dst_folder = c_folder[0:self._replace_chars]
                            else:
                                curr_dst_folder = join('%s-%04d' % (self._prefix_name, cidx))

                            # Patch for DCE
                            if isNotDCE:
                                # Assure this folder is NOT already there
                                if os.path.exists(join(self._dst_folder, curr_dst_folder)):
                                    check_folders = os.listdir(join(self._dst_folder, curr_dst_folder))
                                    if np.any([x.find(self._new_folder_names[idx_kf]) != -1 for x in check_folders]):
                                        continue  # In this case we matched a LOWER level folder (in the hierarchy)

                        else:  # pid is not in LUT
                            if self._keep_original_names:
                                curr_dst_folder = c_folder[0:self._replace_chars]
                            else:
                                curr_dst_folder = join('%s-%04d' % (self._prefix_name, last_idx))
                            LUT[pid] = {'Folder': join('%s-%04d' % (self._prefix_name, last_idx)), 'id': last_idx}
                            last_idx += 1

                        curr_patient = c_folder[self._replace_chars:]
                        # Take into account only the folders in 'self._orig_folder_names'
                        src = join(self._src_folder, c_date_folder, c_folder)
                        dst = join(self._dst_folder, curr_dst_folder, '{}_{}'.format(self._new_folder_names[idx_kf], curr_patient))

                        if (len(dst) > 150) and (system() == 'Windows'):
                            curr_patient = self.make_windows_path(dst, curr_patient)
                            dst = join(self._dst_folder, curr_dst_folder, '{}_{}'.format(self._new_folder_names[idx_kf], curr_patient))

                        print(F" -------------- \n {src} \n {dst}")
                        if os.path.exists(dst):
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)

        # Remove the previous LUT file and save the new one
        if prev_file_found: #
            os.remove(prev_csv_file)
        _lut_file_name = join(self._dst_folder, '{}_from_{}_to_{}.csv'.format(self._lut_file_name, self._start_idx, last_idx - 1))
        self.saveLUT(LUT)
