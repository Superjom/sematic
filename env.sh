PROJECT_PATH=/home/chunwei/sematic
DATA_PATH=$PROJECT_PATH/data
# origin data paths
ORIGIN_LABELED_DATA_PH=$DATA_PATH/origin/train4user_with_label.txt
ORIGIN_TRAIN_DATA_PH=$DATA_PATH/origin/train4user.txt
ORIGIN_TEST_DATA_PH=$DATA_PATH/origin/test4user.txt
# data paths
LABELED_DATA_PH=$DATA_PATH/train4user_with_label.txt
TRAIN_DATA_PH=$DATA_PATH/train4user.txt
TEST_DATA_PH=$DATA_PATH/test4user.txt
# label path
LABELED_DATA_LABEL_PH=${LABELED_DATA_PH}_labels
# dic path
LABEL_DATA_DIC=${LABELED_DATA_PH}_titles_seg_dic 
# 2 gram
LABEL_DATA_DIC2=${LABELED_DATA_PH}_titles_seg_2_dic 
LABEL_DATA_TITLES_2GRAM=${LABELED_DATA_PH}_titles_2gram
TRAIN_DATA_DIC=${TRAIN_DATA_PH}_titles_seg_dic 
TRAIN_DATA_DIC2=${TRAIN_DATA_PH}_titles_seg_2_dic 
TEST_DATA_DIC=${TEST_DATA_PH}_titles_seg_dic 
TEST_DATA_DIC2=${TEST_DATA_PH}_titles_seg_2_dic 
TOTAL_DIC_PATH=$DATA_PATH/total_dic.txt
TOTAL_DIC_PATH2=$DATA_PATH/total_dic_2.txt

PYPY=$PROJECT_PATH/tools/pypy-2.1/bin/pypy


# tools 
liblinear_train=${PROJECT_PATH}/tools/liblinear-1.93/train
liblinear_predict=${PROJECT_PATH}/tools/liblinear-1.93/predict
