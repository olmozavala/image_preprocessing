#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/AI_UM_RadOn/imagevisualizer"

func_fix_folder_names(){
    LOCAL=$1
    # ------- Variables and print (replace al weird stuff into _------
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/, /_/g' {} \+`
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/ /_/g' {} \+`
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/\^/_/g' {} \+`
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/,\^/_/g' {} \+`
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/\^\^/_/g' {} \+`
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/\(/_/g' {} \+`
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/\)/_/g' {} \+`
    # Not sure about this, because is deleting them. In theory the old ones
#    `find $LOCAL/MIM_ORIGINAL -name '*, *' -type d -exec rm -R {} \;`
#    `find $LOCAL/MIM_ORIGINAL -name '* *'  -type d -exec rm -R {} \;`
#    `find $LOCAL/MIM_ORIGINAL -name '*,\^*'-type d -exec rm -R {} \;`
}

RUN_FOLDER='Radiomics'
FOLDER='RADIOMICS_and_MRI_Normalization'
SRC_PATH='/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/PreprocessData/'
CONFIG_PATH="${SRC_PATH}/RUN_OZ/${RUN_FOLDER}/"
MAIN_CONFIG="${SRC_PATH}/config"

REMOTE=/CIFS/Biomarkers_Group/DATA_MRI/
LOCAL=/media/osz1/DATA/DATA/
LOCAL_MIRROR=/media/osz1/DATA_Old/ALL/

echo '############################ Copying configuration file ############################ '
cp Config_Radiomics.py $MAIN_CONFIG/MainConfig.py
#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------

#echo '############################ Synchronizing MIM_ORIGINAL ############################ '
#rsync -r --info=progress2 $REMOTE/$FOLDER/MIM_ORIGINAL $LOCAL/$FOLDER

#echo '############################ Fixing names from MIM ORIGINAL ############################ '
#func_fix_folder_names $LOCAL/$FOLDER

#echo '############################ Making internal link ############################ '
#ln -s $LOCAL/$FOLDER/ $LOCAL_MIRROR

#echo '############################ Reordering Folders ############################ '
#python $SRC_PATH/ReorderMIMFolders.py

#echo '############################ Sync Reordered folders ############################ '
#sudo rsync -r --info=progress2  $LOCAL/$FOLDER/MIM_ORGANIZED_NO_DATE $REMOTE/$FOLDER/

echo '############################ Preprocessing ############################ '
python $SRC_PATH/Preprocessing.py

#echo '############################ Sync Preproc folders ############################ '
#sudo rsync -r --info=progress2  $LOCAL/$FOLDER/Preproc $REMOTE/$FOLDER/

#echo '############################ Sync Preproc folders ############################ '
#sudo rsync -r --info=progress2  $LOCAL/$FOLDER/RADIOMICS_OZ $REMOTE/$FOLDER/
