# finnish-sentiment

Resources for Finnish sentiment classification

# Group first batch of Ylilauta texts

```
ls data/batch-01/*.txt | xargs python3 scripts/group.py \
    --seed 1234 --repeat 5 --max-size 100 50 > data/grouping-01.txt
Divided 1015 items into 50 groups (repeat 5), average size 100.0
```

```
i=0; cat data/grouping-01.txt | while read -r l; do i=$((i+1)); n=$(echo $i | perl -pe 's/^(\d)$/0$1/'); o="data/batch-01-grouped/group-$n"; mkdir -p $o; for f in $l; do cp ${f%.txt}.{txt,ann,json} $o; done; done
```
