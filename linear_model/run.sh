source "../env.sh"
source "../utils.sh"

replace_word_with_wid() {
    for path in $LABELED_DATA_PH $TRAIN_DATA_PH $TEST_DATA_PH; do
        titles_ph=${path}_titles
        seg_ph=${titles_ph}_seg
        #dic_ph=${titles_ph}_seg_dic
        wid_ph=${seg_ph}_wid
        cmd="$PYPY replace_word_with_wid.py $TOTAL_DIC_PATH $seg_ph $wid_ph"
        echo $cmd
        $cmd
    done

    # train
    $PYPY gen_2gram_titles.py ${LABELED_DATA_PH}_titles_seg $LABEL_DATA_TITLES_2GRAM
    $PYPY replace_word_with_wid.py $TOTAL_DIC_PATH2 $LABEL_DATA_TITLES_2GRAM ${LABELED_DATA_PH}_titles_2gram_seg_wid

    # test
    $PYPY gen_2gram_titles.py ${TEST_DATA_PH}_titles_seg $TEST_DATA_TITLES_2GRAM
    $PYPY replace_word_with_wid.py $TOTAL_DIC_PATH2 $TEST_DATA_TITLES_2GRAM ${TEST_DATA_PH}_titles_2gram_seg_wid
}

generate_linear_file() {
    # train test
    $PYPY trans_linear_model_format.py word $LABELED_DATA_LABEL_PH ${LABELED_DATA_PH}_titles_seg_wid ${LABELED_DATA_PH}_linear
    $PYPY trans_linear_model_format.py word $LABELED_DATA_LABEL_PH  ${LABELED_DATA_PH}_titles_2gram_seg_wid ${LABELED_DATA_PH}_2gram_linear
    # test file
    $PYPY trans_linear_model_format.py test ${TEST_DATA_PH}_titles_seg_wid ${TEST_DATA_PH}_titles_linear
    #$PYPY trans_linear_model_format.py test ${TEST_DATA_TITLES_2GRAM}_wid ${TEST_DATA_PH}_titles_2gram_linear
    $PYPY trans_linear_model_format.py test ${TEST_DATA_PH}_titles_2gram_seg_wid ${TEST_DATA_PH}_titles_2gram_linear
}



#replace_word_with_wid
#generate_linear_file

line_model() {
    $liblinear_train -s 3 -c 4 -e 0.001 -v 5 ${LABELED_DATA_PH}_linear   ${LABELED_DATA_PH}_linear.model  
    $liblinear_train -s 3 -c 4 -e 0.001 ${LABELED_DATA_PH}_linear   ${LABELED_DATA_PH}_linear.model  

    $liblinear_train -s 3 -c 4 -e 0.001 -v 5  ${LABELED_DATA_PH}_2gram_linear ${LABELED_DATA_PH}_2gram_linear.model
    $liblinear_train -s 3 -c 4 -e 0.001  ${LABELED_DATA_PH}_2gram_linear ${LABELED_DATA_PH}_2gram_linear.model
}

line_predict() {
#$PYPY trans_linear_model_format.py test ${TEST_DATA_PH}_titles_seg_wid ${TEST_DATA_PH}_titles_linear
$liblinear_predict  ${TEST_DATA_PH}_titles_linear ${LABELED_DATA_PH}_linear.model ${TEST_DATA_PH}_titles_linear_predict 
$liblinear_predict  ${TEST_DATA_PH}_titles_2gram_linear ${LABELED_DATA_PH}_linear.model ${TEST_DATA_PH}_titles_linear_2gram_predict 
}

trans_predict_res_format() {
    seg_predict_ph=${TEST_DATA_PH}_titles_linear_predict 
    seg_predict_res_ph=${seg_predict_ph}_upload
    cd ..
    # seg, 1 gram
    $PYPY gen_predict_res_format.py $seg_predict_ph $TEST_DATA_PH $seg_predict_res_ph
    zip -r ${seg_predict_res_ph}.zip $seg_predict_res_ph 
    # seg, 2 gram
    $PYPY gen_predict_res_format.py  $TEST_DATA_PH $seg_predict_res_ph

    cd linear_model 
}

#trans_predict_res_format
