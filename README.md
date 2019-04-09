# Hashbreaker with MPI
**Hashbreaker**  - brutforce method for looking matching hash to password.

## Algorithm
Algorithm use brutforce method, iterates by numbers. Every number is change to a word with a special dictionary.\
In this program you can use any hash method from `hashlib` module. By default, its `md5`.

There are implemented following dicts: 
* [ 1 ] numbers 
* [ 2 ] lower_letters
* [ 4 ] upper_letters
* [ 8 ] special_sign
* [ 16 ] lower_polish_letters
* [ 32 ] upper_polish_letters

To use combination of dicts, by line argument, just add value in the square bracket.
To use full all possibilities, `number_of_dict` must equal 64.

## Run program:
To run program just use script: `run.sh`.\
or `run.sh <number of processors> <flag> <password/hash> <number_of_dict> <granulation>` .

Possible flags:
 *  `-hash` - if user already have hash to break,
 *  `-word` - if user just want to test program or strength of his password.\
 Program in first place generate properly hash.

## MPI

MPI is implemented as Process farm. By created partition (about length of partition, decide parameter: granulation), to the processors are sending jobs. If on any machine/processor algorithm will find matching hash, Process farm discontinues sending next jobs, and finish his work.


In code, you can change length of looking password, by default is 8. Variable: `password_length`.

## Result

Result will be saved as `*.txt` file with time and info about numb of processors.

##
`Python3.6.5`\
`mpi4py` 
