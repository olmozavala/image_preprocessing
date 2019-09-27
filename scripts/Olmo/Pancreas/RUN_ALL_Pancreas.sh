#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/AI_UM_RadOn/imagevisualizer"

FOLDER='Pancreas'
SRC_PATH='/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/PreprocessData/'
CONFIG_PATH="${SRC_PATH}/RUN_OZ/Pancreas/"
MAIN_CONFIG="${SRC_PATH}/config"

echo '############################ Copying configuration file ############################ '
cp Config_Pancreas.py $MAIN_CONFIG/MainConfig.py
#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------

#echo '############################ Synchronizing MIM_ORIGINAL ############################ '
#rsync -r --info=progress2 /CIFS/Biomarkers_Group/DATA_MRI/$FOLDER/MIM_ORIGINAL /media/osz1/DATA_Old/ALL/$FOLDER/
#echo '############################ Making internal link ############################ '
#ln -s /media/osz1/DATA_Old/ALL/$FOLDER/ /media/osz1/DATA/DATA

#echo '############################ Reordering Folders ############################ '
#python $SRC_PATH/ReorderMIMFolders.py

#echo '############################ Sync Reordered folders ############################ '
#sudo rsync -r --info=progress2  /media/osz1/DATA_Old/ALL/$FOLDER/ORGANIZED /CIFS/Biomarkers_Group/DATA_MRI/$FOLDER/

#echo '############################ Preprocessing ############################ '
python $SRC_PATH/Preprocessing.py

#echo '############################ Sync Preproc folders ############################ '
#sudo rsync -r --info=progress2  /media/osz1/DATA_Old/ALL/$FOLDER/Preproc /CIFS/Biomarkers_Group/DATA_MRI/$FOLDER/
