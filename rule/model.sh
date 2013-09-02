source "../env.sh"
source "../utils.sh"

clean_dataset() {
    for path in $LABELED_DATA_PH $TEST_DATA_PH; do
        fph=${path}_titles_seg_tag
        tph=${path}_cleaned_titles
        cmd="$PYPY filte.py $fph $tph"
        echo $cmd; $cmd
    done
}

clean_dataset
