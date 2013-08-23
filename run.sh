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
# dic path
LABEL_DATA_DIC=${LABELED_DATA_PH}_titles_seg_dic 
# 2 gram
LABEL_DATA_DIC2=${LABELED_DATA_PH}_titles_seg_2_dic 
TRAIN_DATA_DIC=${TRAIN_DATA_PH}_titles_seg_dic 
TRAIN_DATA_DIC2=${TRAIN_DATA_PH}_titles_seg_2_dic 
TEST_DATA_DIC=${TEST_DATA_PH}_titles_seg_dic 
TEST_DATA_DIC2=${TEST_DATA_PH}_titles_seg_2_dic 
TOTAL_DIC_PATH=$DATA_PATH/total_dic.txt
TOTAL_DIC_PATH2=$DATA_PATH/total_dic_2.txt

# include utils.sh
source "./utils.sh"

# ========== actions ===================
init_data() {
    # convert encoding
    echo "convert encoding ..."
    echo $ORIGIN_LABELED_DATA_PH
    convert_encoding $ORIGIN_LABELED_DATA_PH $LABELED_DATA_PH gbk utf8
    convert_encoding $ORIGIN_TRAIN_DATA_PH $TRAIN_DATA_PH gbk utf8
    convert_encoding $ORIGIN_TEST_DATA_PH $TEST_DATA_PH gbk utf8
    # generate text file for wordseg
    awk -F"\t" '{print $2 "\t" $4}' $LABELED_DATA_PH > ${LABELED_DATA_PH}_titles
    awk -F"\t" '{print $1 "\t" $3}' $TRAIN_DATA_PH > ${TRAIN_DATA_PH}_titles
    awk -F"\t" '{print $1 "\t" $3}' $TEST_DATA_PH > ${TEST_DATA_PH}_titles

}
# split word for titles and gen a dic
split_word() {
    # split word
    for path in $LABELED_DATA_PH $TRAIN_DATA_PH $TEST_DATA_PH; do
        new_path=${path}_titles
        wordseg $new_path utf8 0
        wordseg $new_path utf8 1
    done
}

gen_dic() {
    for path in $LABELED_DATA_PH $TRAIN_DATA_PH $TEST_DATA_PH; do
        new_path=${path}_titles
        # gen dic
        seg_path=${new_path}_seg
        tag_seg_path=${new_path}_seg_tag
        seg_dic_path=${seg_path}_dic
        seg_dic_2_path=${new_path}_seg_2_dic
        tag_seg_dic_path=${tag_seg_path}_dic
        #tag_seg_dic_2_path=${tag_seg_path}_dic
        ./tools/pypy gen_dic.py 1 $seg_path $seg_dic_path
        ./tools/pypy gen_dic.py 2 $seg_path $seg_dic_2_path
        ./tools/pypy gen_dic.py 1 $tag_seg_path $tag_seg_dic_path
    done
    # gen total dic
    cat $LABEL_DATA_DIC $TRAIN_DATA_DIC $TEST_DATA_DIC > $TOTAL_DIC_PATH
    ./tools/pypy gen_dic.py $TOTAL_DIC_PATH $TOTAL_DIC_PATH

    cat $LABEL_DATA_DIC2 $TRAIN_DATA_DIC2 $TEST_DATA_DIC2 > $TOTAL_DIC_PATH2
    ./tools/pypy gen_dic.py 2 $TOTAL_DIC_PATH2 $TOTAL_DIC_PATH2
}

# replace title's words with their word indexs

#init_data
#split_word
gen_dic
