import pydicom
from pydicom import Dataset, DataElement, Sequence
from pydicom.multival import MultiValue
from skimage.draw import polygon
import inout.io_common as io_com
import numpy as np
import SimpleITK as sitk
from os.path import join
from os import listdir
import re
from preproc.contour_smoothing import getContourMinPosFrom2DMask
import datetime
from inout.io_common import get_earliest_mri_from_folder


def read_structures(dataset):
    '''
    Reads dicom structures for contours from a Dicom dataset
    :param dataset:  Dicom dataset from pydicom
    :return: contours dataset
    '''
    rt_dicom_structures = []
    for i in range(len(dataset.ROIContourSequence)):
        contour = {}
        contour['color'] = dataset.ROIContourSequence[i].ROIDisplayColor
        contour['number'] = dataset.ROIContourSequence[i].ReferencedROINumber
        contour['name'] = dataset.StructureSetROISequence[i].ROIName
        contour['date'] = dataset.StudyDate
        assert contour['number'] == dataset.StructureSetROISequence[i].ROINumber
        contour['contours'] = [s.ContourData for s in dataset.ROIContourSequence[i].ContourSequence]
        rt_dicom_structures.append(contour)
    return rt_dicom_structures


def get_mask_itk(rt_dicom_structures, reference_image_itk, ctr_names, whole_word=False):
    '''
    Obtains a mask from an rtstructure dicom structure.
    :param rt_dicom_structures:  rt_dicom_structures information
    :param reference_image_itk: Image to use as reference to compute the masks
    :param ctr_names: Name of the rt contours to search for
    :return:
    '''
    image_dims = reference_image_itk.GetSize()

    z_index = -1 # Initialized in -1 so that we only search the first z_index

    all_masks = []
    mask_names = []
    # Iterate over the rt structures in the dicom files
    for con in rt_dicom_structures:
        ctr_mask = np.zeros((image_dims[2], image_dims[1], image_dims[0]), dtype=np.uint8)
        cur_name = con['name']
        # We decide if we need to find exctly the word, or just a contains in
        if whole_word:
            is_found = np.any([cur_name.lower().strip() == roi.lower().strip() for roi in ctr_names])
        else:
            # Using regular expresions
            # Be careful, we are not using lower() here because it is a regular expression
            # Useful for debugging: is_found = re.search(ctr_names[0], cur_name)
            is_found = np.any([re.search(roi, cur_name) for roi in ctr_names])

        if is_found:
            # Iterate over each 'slice' of the contour
            for z_con in con['contours']:
                # Sets the positions as x,y,z
                nodes = np.array(z_con).reshape((-1, 3))
                c_idx = []
                r_idx = []
                # Iterate over each point in that contour
                for node_idx in range(len(nodes)):
                    # Get the position from the original image
                    pos = reference_image_itk.TransformPhysicalPointToIndex(nodes[node_idx])
                    z_index = pos[2] # Save z postion

                    c_idx.append(pos[0])
                    r_idx.append(pos[1])

                # # Create a polygon 'mask' from the contour
                rr, cc = polygon(r_idx, c_idx) # Interpolate contour
                ctr_mask[z_index, rr, cc] = 1
            all_masks.append(ctr_mask)
            mask_names.append(cur_name)

    if len(all_masks) > 0:
        if len(all_masks) > 1:
            return all_masks, mask_names
        else:
            return all_masks, mask_names
    else:
        raise Exception("ERROR: didn't found contour ", ctr_names[0])


def getCtrAsItk(input_folder, ctr_folder_names, ctr_names, base_img, whole_word=False):
    '''
    Gets a contour as an itk image.
    :param input_folder: Where the DICOMS are (root folder)
    :param ctr_folder_names: Folders to search for contours (in order of priority)
    :param ctr_names: Name of the contours
    :param base_img: Base image to 'resample' to
    :param whole_word: Bool array that states if we need to find the whole word of the name
    :return:
    '''

    # Gets the proper rt_folder to look for contours
    cont_file = getLatestContourFolder(ctr_folder_names, input_folder)
    lstFilesContour = io_com.get_dicom_files_in_folder(join(input_folder, cont_file))

    # ===================== Contours ==================
    ds = pydicom.read_file(lstFilesContour[0]) # Reads dataset
    # Reads all the contours in the folder (they are in a dictionary and the 'contours' key has the values as a list
    rt_structures = read_structures(ds)

    all_masks, mask_names = get_mask_itk(rt_structures, base_img, ctr_names, whole_word)

    itk_imgs = [sitk.GetImageFromArray(mask) for mask in all_masks]
    for itk_img in itk_imgs:
        itk_img.CopyInformation(base_img)

    return itk_imgs, mask_names


def getLatestContourFolder(ctr_folder_names, path_ctrs):
    '''
    Reads all the contours folders inside the path and selects the earliest based in
    the order of ctr_folder_names
    :param ctr_folder_names: Names of contours to take into account (in order of priority)
    :param path_ctrs: Path where the contours are stored
    :return:
    '''

    idx_file = 0
    cont_files = []
    # Searches for the proper folder name
    while (len(cont_files) == 0) and (idx_file < len(ctr_folder_names)):
        cont_files = [f for f in listdir(path_ctrs) if f.lower().find(ctr_folder_names[idx_file].lower()) != -1 ]
        idx_file += 1

    if len(cont_files) == 0:
        raise Exception("ERROR: didn't found rt dataset ", ctr_folder_names, " inside ", path_ctrs)
    elif len(cont_files) > 0: # In this case we need to check the date
        times = []
        for cfile in cont_files:
            dicomFiles =[f for f in listdir(join(path_ctrs,cfile)) if f.find('.dcm') != -1 ]
            # Here we are assuming that only one dicom file is present in any RT folder
            ds = pydicom.read_file(join(path_ctrs,cfile,dicomFiles[0])) # Reads dataset
            f_date = np.datetime64( ds.InstanceCreationDate[0:4]+'-'+ \
                           ds.InstanceCreationDate[4:6]+'-'+ \
                           ds.InstanceCreationDate[6:8]+'T'+ \
                           ds.InstanceCreationTime[0:2]+':'+ \
                           ds.InstanceCreationTime[2:4]+':'+ \
                           ds.InstanceCreationTime[4:6] )
            times.append(f_date)

        closest_date = max(times)
        idx_file = np.where(closest_date == times)
        final_file = cont_files[idx_file[0][0]]
    else:# Only one file in this case
        final_file = cont_files[0]

    return final_file


def rtDicomFromPreviousFolder(input_folder, ctr_folder_names, ctr_names, base_img,
                        masks_np, output_file_name, prefix_name=''):
    '''

    :param input_folder: Input folder where the ORIGINAL DICOMS are stored
    :param ctr_folder_names:  Name of folders where to search for contours
    :param ctr_names:  Original contour names (this should have the same order as the contours in masks_np)
    :param base_img:  Itk base image to use for obtaining the positions
    :param masks_np:  This is the numpy 4D binary array with the masks for each contour (ctr, slice, w, h)
    :param prefix_name:  Additional prefix string to use in the new names of the contours
    :return:
    '''

    print('Getting pydicom DataSequence from previous data...')

    # Gets the proper rt_folder to look for contours
    cont_file = getLatestContourFolder(ctr_folder_names, input_folder)
    lstFilesContour = io_com.get_dicom_files_in_folder(join(input_folder, cont_file))

    # ===================== Contours ==================
    ds = pydicom.read_file(lstFilesContour[0]) # Reads original dataset

    final_ROIContourSequence_values = [] # This should be an array of datasets and will be replaced from the original FileDataset

    # Iterate over the ROIContourSequences (ak the contours) Type: Sequence
    for new_idx_ctr, c_ctr_name in enumerate(ctr_names):
        old_idx_ctr = [i for i, x in enumerate(ds.StructureSetROISequence) if x.ROIName == c_ctr_name]

        if len(old_idx_ctr) == 0: # If the ROI was not found
            print(F'ERROR the contour {c_ctr_name} was not found on previous RTStructure')
        else:
            # If the ROI is found, the we use it as a template and just modify the positions of the contours
            old_idx_ctr = old_idx_ctr[0] # Get just the index
            ds.StructureSetROISequence[new_idx_ctr].ROIName == c_ctr_name # Use the new name for this index
            ds.StructureSetROISequence[new_idx_ctr].ROINumber == new_idx_ctr + 1# Use the new name for this index
            ds.Manufacturer = 'Deep Learning Biomarkers Group'
            ds.SeriesDate = str(datetime.date.today().strftime('%Y%m%d'))
            ds.SeriesDescription = 'NN Prediction'
            ds.StructureSetName = 'NN Prediction'

            print(F'\t Found {c_ctr_name} with idx {old_idx_ctr}!!!')

            # Copy the ROIContourSequence of the OLD contour (VERY IMPORTANT STEP, we initalize with everything that was there before)
            old_ROIContour_ds = ds.ROIContourSequence[old_idx_ctr]
            ds.StructureSetROISequence[old_idx_ctr].ROIName = F'{prefix_name}{c_ctr_name}'

            cur_mask = masks_np[new_idx_ctr,:,:,:] # Get the proper mask data

            slices_w_data = np.unique(np.where(cur_mask > 0)[0])
            cur_ContourSequence_values = []

            # Use the first contour sequence as template (IMPORTANT)
            old_ContourSequence_ds = old_ROIContour_ds.ContourSequence[0]
            # Iterate slices with some contour inside. Transform the mask to contour and add it to the sequence
            for idx_slice,slice in enumerate(slices_w_data):
            # for idx_slice,slice in enumerate([82]):

                # Get a contour from the 2D mask using OpenCV
                ctr_pts = getContourMinPosFrom2DMask(cur_mask[slice,:,:])
                # --- Use to visualize the contoured points for each slice and contour -----------
                # import matplotlib.pyplot as plt
                # plt.imshow(cur_mask[slice,:,:])
                # plt.title(slice)
                # for c_ctr in ctr_pts:
                #     plt.scatter(c_ctr[:,0,0],c_ctr[:,0,1],s=1)
                # plt.show()

                tot_ctrs = len(ctr_pts)
                # Iterate over EACH contour and create a dataset for each of them
                for idx_ctr in range(tot_ctrs):
                    cur_contourdata_ds = Dataset() # This is the Contour data for this ContourSequence
                    # Copy the desired values from the OLD ContourSequence
                    cur_contourdata_ds.ContourGeometricType = old_ContourSequence_ds.ContourGeometricType

                    contourdata_values = []

                    tot_pts = ctr_pts[idx_ctr].shape[0]
                    this_slice_indx_pos  = []

                    # Add the 'desired' format of (x,y,z) for each contour point
                    cur_ctr_pts = ctr_pts[idx_ctr]
                    for cur_pt in cur_ctr_pts:
                        this_slice_indx_pos.append([int(cur_pt[0][0]),int(cur_pt[0][1]), int(slice)])
                    # We add again the first point of each contour at the end (trying to 'close' the contour)
                    this_slice_indx_pos.append([int(cur_ctr_pts[0][0][0]),int(cur_ctr_pts[0][0][1]), int(slice)])

                    # Transform each point into a physical position
                    for c_pos in this_slice_indx_pos:
                        phys_pos = base_img.TransformIndexToPhysicalPoint(c_pos)
                        contourdata_values.append(phys_pos[0])
                        contourdata_values.append(phys_pos[1])
                        contourdata_values.append(phys_pos[2])

                    # Copy the list of physical positions in the variable ContourData of the dataset
                    cur_contourdata_ds.ContourData = MultiValue(pydicom.valuerep.DSfloat, contourdata_values)
                    cur_contourdata_ds.NumberOfContourPoints = tot_pts

                    # Append this Dataset into the list of slices with date
                    cur_ContourSequence_values.append(cur_contourdata_ds)

            old_ROIContour_ds.ContourSequence = Sequence(cur_ContourSequence_values)  # Replace the desired sequence with the new values
            final_ROIContourSequence_values.append(old_ROIContour_ds)  # Append it to the ROIContourSquence values

    # Replace the original Sequence of ROIContours with the new ones. These were initialized with the previous values
    # and only the Contour Data was replaced
    new_ROIContourSequence = Sequence(final_ROIContourSequence_values)
    ds.ROIContourSequence = new_ROIContourSequence # Replace old ROIContourSequence with new one

    pydicom.dcmwrite(output_file_name, ds)
