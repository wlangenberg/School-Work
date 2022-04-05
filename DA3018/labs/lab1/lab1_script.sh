echo "-- Question 1 -- "
# Counting number of lines in all .txt files in current directory
wc -l *.txt

echo "-- Question 2 --"
#grep -Ho  “fp.2.Luci_02H12.ctg.ctg7180000019650”
grep -Hor --include '*.txt' 'fp.2.Luci_02H12.ctg.ctg7180000019650' | uniq -c


echo "-- Question 3 --"


