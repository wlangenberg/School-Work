
# for f in *.txt; do 
#     echo "$f:"; 
#     grep -w "fp.2.Luci_02H12.ctg.ctg7180000019650" $f | wc -l; 
# done;


# {if ($1<$2) print $2" "$1; else print $1" "$2}


for f in *.txt; do 
    echo "Duplicate pairs in file '$f':";
    echo " "
    cat $f | 
    awk '{if ($1<$2) print $2" "$1; else print $1" "$2}' | 
    sort | 
    uniq -d
done;

awk '{if ($1<$2) print $2" "$1; else print $1" "$2}'

# awk ' {split( $0, a, " " ); asort( a ); for( i = 1; i <= length(a); i++ ) printf( "%s ", a[i] ); printf( "\n" ); }' *.txt


cat *.txt | awk '{if ($1<$2) print $2" "$1; else print $1" "$2}' | sort | uniq -d | wc -l