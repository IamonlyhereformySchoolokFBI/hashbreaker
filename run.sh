# #!/bin/bash

if [[ $# -eq 5 ]] ; then

	if [[ $5 -lt $1 ]]; then
		printf 'Cannot pass granulation less than number of proc!\n'
		printf 'Set: granulation = number of proc.\n------------\n'
		mpiexec -n $1 -host localhost python3 src/main.py $2 $3 $4 $1 
	else
		mpiexec -n $1 -host localhost python3 src/main.py $2 $3 $4 $5 
		
	fi
else

	read -p 'How many processors: ' proc
	printf 'Passing:\n[ 1 ] Plain word\n[ 2 ] Hash\n'
	read -p 'choice: ' choice
	read -p 'Pass your string: ' string
	read -p 'Granulation: ' granulation

	if [[ $choice -eq 1 ]]; then
		trigger='-hash'
	else
		trigger='-word'
	fi

	dict_number=0

	read -p 'Use : numbers [Y/n]: ' choice
	if [[ $choice == 'Y' ]] || [[ $choice == 'y' ]]; then
		let dict_number=$dict_number+1
	fi

	read -p 'Use : lower_letters [Y/n]: ' choice
	if [[ $choice == 'Y' ]] || [[ $choice == 'y' ]]; then
		let dict_number=$dict_number+2
	fi

	read -p 'Use : upper_letters [Y/n]: ' choice
	if [[ $choice == 'Y' ]] || [[ $choice == 'y' ]]; then
		let dict_number=$dict_number+4
	fi

	read -p 'Use : special_sign [Y/n]: ' choice
	if [[ $choice == 'Y' ]] || [[ $choice == 'y' ]]; then
		let dict_number=$dict_number+8
	fi

	read -p 'Use : lower_polish_letters [Y/n]: ' choice
	if [[ $choice == 'Y' ]] || [[ $choice == 'y' ]]; then
		let dict_number=$dict_number+16
	fi

	read -p 'Use : upper_polish_letters [Y/n]: ' choice
	if [[ $choice == 'Y' ]] || [[ $choice == 'y' ]]; then
		let dict_number=$dict_number+32
	fi

	if [[ $granulation -lt $proc ]]; then
		printf 'Cannot pass granulation less than number of proc!\n'
		printf 'Set: granulation = number of proc.\n------------\n'
		mpiexec -n $proc -host localhost python3 src/main.py $trigger $string $dict_number $proc
	else
		mpiexec -n $proc -host localhost python3 src/main.py $trigger $string $dict_number $granulation
	fi
fi