David Lin, May 2016
Python 2.7
Python script that walks through an entire directory (and subdirectories)
and counts lines of code of respective languages. Ignores white space and
commented code. Not efficient as did not previously plan on excluding block
comments.

usage: python ploc.py -{options} {target directory}

options currently are -v, which prints the directory path as it is read
					  -c, which prints the count of each directory
					  -d, debug which prints out all counted lines