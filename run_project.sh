START_TIME=$(date +%s)
echo "--- JOB START: $(date) ---"

hadoop fs -rm -r /user/student/library /user/student/final_index_output 2>/dev/null

hadoop fs -mkdir -p /user/student/library
hadoop fs -put /workspace/books/* /user/student/library/

hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
    -D mapreduce.job.reduces=1 \
    -D dfs.replication=3 \
    -files /workspace/mapper.py,/workspace/reducer.py,/workspace/combiner.py,/workspace/stopwords.txt \
    -cmdenv REMOVE_STOPWORDS=true \
    -mapper "python3 mapper.py" \
    -combiner "python3 combiner.py" \
    -reducer "python3 reducer.py" \
    -input /user/student/library \
    -output /user/student/final_index_output

END_TIME=$(date +%s)
echo "-------------------------------------------"
echo "TOTAL EXECUTION TIME: $((END_TIME - START_TIME)) seconds"
echo "-------------------------------------------"

echo "--- Top 20 Index Entries ---"
hadoop fs -cat /user/student/final_index_output/part-00000 | head -n 20
