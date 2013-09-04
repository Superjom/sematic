# 一系列的相似度
# 完全一致              : 相似度
# 疑问词 助动词变换     : token tfidf 相似度
# 语序变化              : 1元 tfidf
# query是title子句      : 字句检测相似度

# 字句检测
source "../env.sh"

subseq_check() {
    for path in $LABEL_DATA_TITLES_2GRAM \
        ${LABELED_DATA_PH}_titles_seg\
        $TEST_DATA_TITLES_2GRAM\
        ${TEST_DATA_PH}_titles_seg; do
        cmd="$PYPY sim.py subseq $path ${path}.subseq.sim"
        echo $cmd; $cmd;
    done

    for path in $LABELED_DATA_PH $TEST_DATA_PH; do
        path=${path}_titles
        cmd="$PYPY sim.py subseq_char $path ${path}.subseq.sim"
        echo $cmd; $cmd;
    done
}

tfidf_sim() {
    type=$1
    if [ $type = "init" ]; then
        #$PYPY tfidf.py 
        cmd="cat ${LABELED_DATA_PH}_titles_seg \
            ${TRAIN_DATA_PH}_titles_seg \
            ${TEST_DATA_PH}_titles_seg > $DATA_PATH/total_titles_seg"
        echo $cmd; $cmd;
    fi

    if [ $type = "train" ]; then
        cmd="$PYPY tfidf.py word_tf_idf $DATA_PATH/total_titles_seg $DATA_PATH/total_titles_seg.tfidf.sim"
        echo $cmd; $cmd;
    fi

    if [ $type = "trans_format" ]; then
        # trans format
        cmd="$PYPY tfidf.py trans_format $DATA_PATH/total_titles_seg.tfidf.sim $LABELED_DATA_PH $TRAIN_DATA_PH $TEST_DATA_PH"
        echo $cmd; $cmd
    fi
}
#subseq_check
#tfidf_sim

trans_linear_format() {
    path=${LABELED_DATA_PH}_titles.subseq.sim
    cmd="$PYPY trans_linear_model.py vector train $path ${path}.linear $LABELED_DATA_LABEL_PH "
    echo $cmd; $cmd;

    path=${TEST_DATA_PH}_titles.subseq.sim
    cmd="$PYPY trans_linear_model.py vector test $path ${path}.linear $LABELED_DATA_LABEL_PH "
    echo $cmd; $cmd;
    #$PYPY trans_linear_model_format.py test $test_wid_path $test_linear_file
}

train() {
    path=${LABELED_DATA_PH}_titles.subseq.sim
    train_linear_file=${path}.linear
    model_path=${train_linear_file}.model

    path=${TEST_DATA_PH}_titles.subseq.sim
    test_linear_file=${path}.linear
    predict_ph=${test_linear_file}_predict
    upload_ph=${predict_ph}_upload
    # train
    cmd="$liblinear_train -s 2 -c 4 -e 0.001 -v 5 $train_linear_file"
    echo $cmd; $cmd

    cmd="$liblinear_train -s 2 -c 4 -e 0.001 $train_linear_file $model_path"
    echo $cmd; $cmd
    $liblinear_predict $test_linear_file $model_path $predict_ph


    cd ..
    cmd="$PYPY gen_predict_res_format.py $predict_ph $TEST_DATA_PH $upload_ph"
    echo $cmd; $cmd
    cd sim 

    cmd="$PYPY sim.py filter_sim_label $upload_ph ${TEST_DATA_PH}_titles.subseq.sim"
    echo $cmd; $cmd
    rm ${upload_ph}.zip 
    zip -r ${upload_ph}.zip $upload_ph
}

#subseq_check
#trans_linear_format
#train

#tfidf_sim train
tfidf_sim trans_format
