# load environment
source "./env.sh"
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
    # generate titles
    awk -F"\t" '{print $1}' $LABELED_DATA_PH > $LABELED_DATA_LABEL_PH
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
        ./tools/pypy gen_dic.py 1 $tag_seg_path $tag_seg_dic_path
        ./tools/pypy gen_dic.py 2 $seg_path $seg_dic_2_path
    done
    # gen total dic
    #cat $LABEL_DATA_DIC $TRAIN_DATA_DIC $TEST_DATA_DIC > $TOTAL_DIC_PATH
    cat $LABEL_DATA_DIC $TEST_DATA_DIC > $TOTAL_DIC_PATH
    ./tools/pypy gen_dic.py 1 $TOTAL_DIC_PATH $TOTAL_DIC_PATH
    # gen total 2gram dic
    #cat $LABEL_DATA_DIC2 $TRAIN_DATA_DIC2 $TEST_DATA_DIC2 > $TOTAL_DIC_PATH2
    cat $LABEL_DATA_DIC2 $TEST_DATA_DIC2 > $TOTAL_DIC_PATH2
    ./tools/pypy gen_dic.py 1 $TOTAL_DIC_PATH2 $TOTAL_DIC_PATH2
}

# extract tokens from titles
token2titles_seg() {
    # extract tags to titles
    for path in $LABELED_DATA_PH $TEST_DATA_PH; do
        $PYPY titles_seg_token2titles.py ${path}_titles_seg_tag ${path}_titles_seg_tokens
    done
    # generate total tag dic 
    # here only for labeled and test data
    cat ${LABELED_DATA_PH}_titles_seg_tokens ${TEST_DATA_PH}_titles_seg_tokens > $TOTAL_TOKEN_DIC
    $PYPY gen_dic.py 1 $TOTAL_TOKEN_DIC $TOTAL_TOKEN_DIC
    cat ${LABELED_DATA_PH}_titles_seg_tokens ${TEST_DATA_PH}_titles_seg_tokens > $TOTAL_TOKEN_2_DIC
    $PYPY gen_dic.py 2 $TOTAL_TOKEN_2_DIC $TOTAL_TOKEN_2_DIC
}

edit_distance() {
    for path in $LABELED_DATA_PH $TEST_DATA_PH; do
        # word-wise
        wid_path=${path}_titles_seg_wid
        source_path=${path}_titles
        word_dis_path=${path}.word.distance
        char_dis_path=${path}.char.distance

        cmd="$PYPY edit_distance.py word $wid_path $word_dis_path"
        echo $cmd; $cmd

        cmd="$PYPY edit_distance.py char $source_path $char_dis_path"
        echo $cmd; $cmd
    done
}

# replace title's words with their word indexs

#init_data
#split_word
gen_dic
#token2titles_seg
#edit_distance
