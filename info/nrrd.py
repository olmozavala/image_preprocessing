import SimpleITK as sitk
import os
from os.path import join
from pandas import DataFrame


class NrrdDataSummary():
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

    def generate_data_summary(self, img_file_name, output_file_name):
        """It generates a small summary from the data_sum as a CSV file (shape and voxel size)
            :param img_file_name: Name of the nrrd file that we want to use to retrieve the info
            :param output_file_name: Name of the output file
            :return:
        """
        cases = [x for x in os.listdir(self._input_folder) if os.path.isdir(join(self._input_folder, x))]
        cases.sort()
        
        data_sum = DataFrame(index=cases, columns=['size','origin','spacing','direction'])

        for c_case in cases:
            print(F"---------- {c_case}----------")
            try:
                cur_img = sitk.ReadImage(join(self._input_folder, c_case, img_file_name))
                data_sum.loc[c_case]['size'] = cur_img.GetSize()
                data_sum.loc[c_case]['origin'] = cur_img.GetOrigin()
                data_sum.loc[c_case]['spacing'] = cur_img.GetSpacing()
                data_sum.loc[c_case]['direction'] = cur_img.GetDirection()
            except Exception as e:
                print(F'Failed for folder {c_case}: {e}')
                continue

        data_sum.to_csv(join(self._output_folder, output_file_name))
