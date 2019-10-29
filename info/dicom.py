from __future__ import division, print_function
import os
from os.path import join
from pandas import DataFrame
import re
import dicom
from inout.io_common import get_dicom_files_in_folder


class DicomDataSummary():
    """
    This function allows the generation of information stored on nrrd files. 
    """

    def __init__(self, **kwargs):
        self.input_folder = 'input'
        self.output_folder = 'output'

        # All the arguments that are passed to the constructor of the class MUST have its name on it.
        for arg_name, arg_value in kwargs.items():
            self.__dict__["_" + arg_name] = arg_value

    def __getattr__(self, attr):
        '''Generic getter for all the properties of the class'''
        return self.__dict__["_" + attr]

    def __setattr__(self, attr, value):
        '''Generic setter for all the properties of the class'''
        self.__dict__["_" + attr] = value

    def generate_data_summary(self, folder_name_regex, file_name='data_summary'):
        """It generates a small summary from the data_sum as a CSV file (shape and voxel size)
            :param folder_name_regex:
            :return: 
        """
        cases = [x for x in os.listdir(self._input_folder) if os.path.isdir(join(self._input_folder, x))]
        cases.sort()
        
        colums_dic = {'Date':'AcquisitionDate',
                    'EchoTime':'EchoTime',
                    'EchoTrainLength':'EchoTrainLength',
                    'Manufacturer':'Manufacturer',
                    'Model':'ManufacturerModelName',
                    'Modality':'Modality',
                    'RepetitionTime': 'RepetitionTime',
                    'Orientation': 'ImageOrientationPatient'}

        extra_columns = ['Size', 'Spacing', 'PixelSize']
        all_columns = extra_columns + list(colums_dic.keys())
        data_sum = DataFrame(index=cases, columns=all_columns)
                             
        # In this case we look for folders inside each case
        for c_case in cases:
            print(F"---------- {c_case}----------")
            try:
                matched_folders = [x for x in os.listdir(join(self._input_folder, c_case)) if not (re.search(folder_name_regex, x) is None)]
                
                if len(matched_folders) > 1:
                    print(F'Warning: more than one folder matched: {matched_folders}')
                if len(matched_folders) == 0:
                    print(F'Warning: folder not matched for {c_case}')
                    continue
                else:
                    final_folder_name = join(self._input_folder, c_case, matched_folders[0])
                    all_dicom_files = get_dicom_files_in_folder(final_folder_name)
                    ds = dicom.read_file(all_dicom_files[0])  # Reads dataset
                    for c_name, c_key in colums_dic.items():
                        data_sum.loc[c_case][c_name] = eval(F'ds.{c_key}')
                    data_sum.loc[c_case]['Size'] = F'{ds.Rows} x {ds.Columns} x {len(all_dicom_files)}'
                    spacing = ds.PixelSpacing
                    data_sum.loc[c_case]['Spacing'] = F'{spacing[0]} x {spacing[1]} x {ds.SliceThickness}'
                    data_sum.loc[c_case]['PixelSize'] = F'{spacing[0]*spacing[1]*ds.SliceThickness:.2f}'
            except Exception as e:
                print(F'Failed for folder {c_case}: {e}')
                continue

        data_sum.to_csv(join(self._output_folder, file_name))
