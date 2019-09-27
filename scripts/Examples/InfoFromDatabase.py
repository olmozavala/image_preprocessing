from info.dicom import DicomDataSummary
from info.nrrd import NrrdDataSummary


def main():

    #### Example in how to generate a summary of dicom database#######
    fname = 'GE'
    sum_obj = DicomDataSummary(input_folder=F'/media/osz1/DATA/DATA/{fname}/MIM_ORGANIZED_NO_DATE',
                               output_folder='.')

    sum_obj.generate_data_summary(folder_name_regex='T2_TRANSVERSAL', file_name=F'{fname}_Axial.csv')
    sum_obj.generate_data_summary(folder_name_regex='T2_CORONAL', file_name=F'{fname}_Coronal.csv')
    sum_obj.generate_data_summary(folder_name_regex='T2_SAGITTAL', file_name=F'{fname}_Sagital.csv')


    #### Example in how to generate a summary of PREPROC database#######
    sum_obj = NrrdDataSummary(input_folder=F'/media/osz1/DATA/DATA/{fname}/Preproc',
                              output_folder='.')

    sum_obj.generate_data_summary(img_file_name='img_tra.nrrd', output_file_name='Summary_Nrrd.csv')


if __name__ == '__main__':
    main()
