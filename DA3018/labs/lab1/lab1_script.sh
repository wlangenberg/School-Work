echo "-- Question 1 -------------------------------------------------------------------------------------------------- "
echo "How many lines do the two files contain? Count for each file separately using a single command and globbing."
echo "---------------------------------------------------------------------------------------------------------------- "
echo ""

wc -l *.txt

echo ""
echo ""
echo "-- Question 2 --------------------------------------------------------------------------------------------------"
echo "In how many pairs do we find the identifier “fp.2.Luci_02H12.ctg.ctg7180000019650”? Count in the two files separately (i.e., report two numbers)."
echo "---------------------------------------------------------------------------------------------------------------- "
echo ""

grep -o 'fp.2.Luci_02H12.ctg.ctg7180000019650' *.txt | sort | uniq -c

#Also works: for f in *.txt; do echo "$f:"; grep -w "fp.2.Luci_02H12.ctg.ctg7180000019650" $f | wc -l; done;

echo ""
echo ""
echo "-- Question 3 --------------------------------------------------------------------------------------------------"
echo "How many distinct identifiers do we have? That is, if you have seen the identifiers a, b, a, c, a, then there are three distinct identifiers: a, b, and c. Count the two files together as one dataset. Hint: The tr command can be useful here."
echo "---------------------------------------------------------------------------------------------------------------- "
echo ""

cat *.txt | tr -s [:space:] '\n' | sort | uniq -c | wc -l

echo ""
echo ""
echo "-- Question 4 --------------------------------------------------------------------------------------------------"
echo "There are actually two pairs that are appear twice in the two files. Which pairs and in which file?"
echo "---------------------------------------------------------------------------------------------------------------- "

for f in *.txt; do 
    echo "";
    echo "Duplicate pairs in file '$f':";
    cat $f | 
    awk '{if ($1<$2) print $2" "$1; else print $1" "$2}' | 
    sort | 
    uniq -d
done;


echo ""
echo ""
echo "-- Question 5 --------------------------------------------------------------------------------------------------"
echo "Write a 'one-liner', using shell commands, to compute the number of shared edges (i.e., columns) found in pairs1.txt and pairs2.txt. That is, write a shell command, using pipes, that computes the intersection of the edge sets represented in the two files. You must handle the fact that the line 'a b' represents the same edge as 'b a'. You may disregard duplicate edges within the same file"
echo "---------------------------------------------------------------------------------------------------------------- "
echo ""


echo "I am not certain if I have understood the question entierly. Here is atleast the number of unique pairs when combining both text files and sorting each line so that a = b is equivalent to b = a."
echo ""
cat *.txt | awk '{if ($1<$2) print $2" "$1; else print $1" "$2}' | sort | uniq -d | wc -l

echo ""
echo "---------------------------------------------------------------------------------------------------------------- "

