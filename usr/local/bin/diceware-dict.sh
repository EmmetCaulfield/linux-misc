#!/bin/bash

# This shell script generates alternative diceware wordlists which you
# can then use in the usual way. See: www.diceware.com

# Plain-text dictionary to use:
dict=/usr/share/dict/words

# Form a candidate word list:
candidate_words () {
    LC_COLLATE=en_US grep -E '^[a-z]{2,6}[a-rt-z]$' "$dict"
}

# Convert a number to base6 plus one so digits match the spots on dice
base6plus1 () {
    declare -i  i n r d
    declare -a  a
    i=$1	# Number to be converted
    n=$2	# Number of digits total
    
    # Initialize array of digits to all ones:
    for ((d=0; d<n; d++)); do
	a[$d]=1
    done

    for ((d=n-1; d>=0; d--)); do
	r=$(( i % 6 ))
	i=$(( i / 6 ))
	a[$d]=$(( r + 1 ))
    done
    oifs="$IFS"
    IFS=
    echo "${a[*]}"
    IFS="$oifs"
}


n_candidate_words=$(candidate_words | wc -l)
n_dice=$(echo "l($n_candidate_words)/l(6)" | bc -ql | cut -d. -f1)
n_words=$(echo "6^$n_dice" | bc -ql)
n_digits=$(( $(echo "$n_words" | wc -c) - 1 ))

declare -i i=0
while read word; do
    echo "$(base6plus1 $i $n_dice): $word"
    i=$((i+1))
done < <(candidate_words | shuf -n$n_words)
