#!/bin/bash

declare -A table
num_rows=3
num_columns=3

# print table at the start
for ((i=1;i<=num_rows;i++)) do
	printf "|"
	for ((j=1;j<=num_columns;j++)) do
		table[$i,$j]="-"
		printf " ${table[$i,$j]} "
	done
	echo "|"
done

# loop condition
k=1
# starting player
player="O"

# main loop
while [ "$k" -eq 1 ]
do
	
	echo ""
	echo "Kolejna tura"

	# action
	echo "Graczu ${player} podaj kolumne"
	read given_column
	echo "Graczu ${player} podaj wiersz"
    read given_row

	# reaction 
	# check if cell is free
	if [ "${table[$given_row,$given_column]}" == "-" ]
	then
		# mark cell and change player
		table[$given_row,$given_column]=${player}
		if [ ${player} == "O" ]
		then	
			player="X"
		else
			player="O"
		fi
	else
		echo "Pole nie jest wolne bądź nie istnieje"
	fi

	# information
	k=0
	for ((i=1;i<=num_rows;i++)) 
	do
        printf "|"
        for ((j=1;j<=num_columns;j++)) do
            printf " ${table[$i,$j]} "
			if [ "${table[$i,$j]}" == "-" ]
			then
				k=1
			fi
        done
        echo "|"
    done

	for x in {1..3}
	do
        if [ "${table[1,$x]}" == "${table[2,$x]}" ] && [ "${table[2,$x]}" == "${table[3,$x]}" ] && [ "${table[2,$x]}" != "-" ]
		then
			echo "wygrał gracz ${table[2,$x]}"
			k=0
		elif [ "${table[$x,1]}" == "${table[$x,2]}" ] && [ "${table[$x,2]}" == "${table[$x,3]}" ] && [ "${table[$x,2]}" != "-" ]
		then
			echo "wygrał gracz ${table[$x,2]}"
            k=0
		fi
	done

	if [ "${table[1,1]}" == "${table[2,2]}" ] && [ "${table[2,2]}" == "${table[3,3]}" ] && [ "${table[2,2]}" != "-" ]
    then
	    echo "wygrał gracz ${table[2,2]}"
        k=0
    elif [ "${table[3,1]}" == "${table[2,2]}" ] && [ "${table[2,2]}" == "${table[1,3]}" ] && [ "${table[2,2]}" != "-" ]
    then        
    	echo "wygrał gracz ${table[2,2]}"
        k=0
    fi

done
