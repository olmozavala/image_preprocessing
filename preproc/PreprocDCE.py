import pydicom
import SimpleITK as sitk
from os.path import join
import os
import numpy as np

def getDimensionsDCE(file):
    ''' Gets the dimension information from a single dcm file
    :param file:
    :return:
    '''
    dataset = pydicom.dcmread(file)
    rows = int(dataset.Rows)
    cols = int(dataset.Columns)
    total_times = dataset.NumberOfTemporalPositions
    total_slices = dataset.ImagesInAcquisition
    slices_per_image = int(total_slices/total_times)
    # origin = dataset.ImagePositionPatient
    # spacing = [dataset.PixelSpacing[0], dataset.PixelSpacing[1], dataset.SliceThickness]
    dt = dataset.RepetitionTime

    img = sitk.ReadImage(file)
    origin_itk = img.GetOrigin()
    spacing_itk = img.GetSpacing()
    direction_itk = img.GetDirection()
    return rows,cols,slices_per_image, total_times, origin_itk, spacing_itk, direction_itk, dt

def getDimensions(file):
    ''' Gets the dimension information from a single dcm file
    :param file:
    :return:
    '''
    dataset = pydicom.dcmread(file)
    rows = int(dataset.Rows)
    cols = int(dataset.Columns)
    c_time =dataset.AcquisitionNumber
    # print(F'{dataset.AcquisitionNumber}-{dataset.SeriesTime}-{dataset.RepetitionTime}')
    return rows, cols, c_time

def setParamsItkImage(itk_img, origin, direction, spacing):
    ''' Sets the parameters for an itk image
    :param itk_img:
    :param origin:
    :param direction:
    :param spacing:
    :return:
    '''
    itk_img.SetOrigin(origin)
    itk_img.SetDirection(direction)
    itk_img.SetSpacing(spacing)
    return itk_img

def preprocDCE(root_input_folder, output_folder, norm_dce):
    ''' Reads the DCE images from one or multiple folders and store the results as an nrrd file
    :param root_input_folder:
    :param output_folder:
    :return:
    '''

    folders_with_dce = [x for x in os.listdir(root_input_folder) if x.find('DCE') != -1]
    if len(folders_with_dce) == 1: # Case one, all the dcm files are inside one folder
        print('\t DCE -- Single folder')
        input_folder = join(root_input_folder,folders_with_dce[0])
        files = [x for x in os.listdir(input_folder) if x.find('.dcm') != -1]
        files.sort()

        rows,cols,slices_per_image,total_times, origin_itk, spacing_itk, direction_itk, dt = getDimensionsDCE(join(input_folder,files[0]))
        all_images = np.zeros((slices_per_image,cols,rows,total_times))
        print('\t Reading data....')
        for file in files:
            filename = join(input_folder,file)
            dataset = pydicom.dcmread(filename)
            c_time = int(np.floor((dataset.InstanceNumber - 1)/slices_per_image))  # We start index at 0 not at 1
            slice = dataset.InStackPositionNumber - 3  # We start index at 0 not at 1 TODO verify -3 works for all of them (it doesn't make sense)
            # print(F'OUR: {c_time} - {slice}     ORIGINAL: {dataset.InstanceNumber} - {dataset.InStackPositionNumber}')
            all_images[slice,:,:,c_time] = dataset.pixel_array

        print('\t Grouping images....')
        all_times = []
        for c_time in range(total_times):
            itk_img = sitk.GetImageFromArray(all_images[:,:,:,c_time])
            all_times.append(setParamsItkImage(itk_img,origin_itk, direction_itk, spacing_itk))

        print('\t Saving data....')
        img = sitk.JoinSeries(all_times)
        img.SetMetaData('dt', str(dt))
        sitk.WriteImage(img, join(output_folder,'img_dce.nrrd'))

    if len(folders_with_dce) > 1: # Case one, all the dcm files are inside one folder
        print('\t DCE -- Multiple folder')
        total_times = len(folders_with_dce)
        all_images = None
        for c_time_folder in folders_with_dce: # Iterate over each time
            input_folder = join(root_input_folder,c_time_folder)
            # Get all the dcm files for this time
            dcm_files = [x for x in os.listdir(input_folder) if x.find('.dcm') != -1]
            dcm_files.sort()
            # Get dimensions for current time
            rows, cols, c_time = getDimensions(join(root_input_folder,c_time_folder,dcm_files[0]))

            slices_per_image = len(dcm_files)

            # Get metadata for current timestep
            itk_img = sitk.ReadImage(join(root_input_folder,c_time_folder,dcm_files[0]))
            origin_itk = itk_img.GetOrigin()
            direction_itk = itk_img.GetDirection()
            spacing_itk = itk_img.GetSpacing()

            if all_images is None: # Instantiate all images
                all_images = np.zeros((slices_per_image,rows,cols,total_times))
                # print(F'Dimensions are {all_images.shape}')

            for c_dcm_file in dcm_files:
                filename = join(root_input_folder,c_time_folder,c_dcm_file)
                dataset = pydicom.dcmread(filename)
                slice = dataset.InstanceNumber - 1  # We start index at 0 not at 1
                # print(F'OUR: {slice}     ORIGINAL: {dataset.InstanceNumber} ')
                all_images[slice,:,:,c_time-1] = dataset.pixel_array

        print('\t Grouping images....')
        all_times = []
        for c_time in range(total_times):
            itk_img = sitk.GetImageFromArray(all_images[:,:,:,c_time])
            all_times.append(setParamsItkImage(itk_img,origin_itk, direction_itk, spacing_itk))

        print('\t Saving data....')
        img = sitk.JoinSeries(all_times)
        # img.SetMetaData('dt', str(dt))
        sitk.WriteImage(img, join(output_folder,'img_dce.nrrd'))
