# David Lin, May 2016
# Python 2.7
# Python script that walks through an entire directory (and subdirectories)
# and counts lines of code of respective languages. Ignores white space and
# commented code. Not efficient as did not previously plan on excluding block
# comments.
#
# usage: python ploc.py -{options} {target directory}
#
# options currently are -v, which prints the directory path as it is read
# 						-c, which prints the count of each directory
#						-d, debug which prints out all counted lines

import os
import sys

# Dictionary of extensions : tuple(Language name, single line comment,
# 								   LHS of block comment, RHS of block comment)
# where if none exist denoted by ''
extensions = {
	'.py'   : ('Python'       , '#'   ,  ''        ,  ''     ),
	'.c'    : ('C'            , '//'  ,  '/*'      ,  '*/'   ),
	'.cpp'  : ('C++'          , '//'  ,  '/*'      ,  '*/'   ),
	'.cs'   : ('C#'           , '///' ,  '/*'      ,  '*/'   ),
	'.java' : ('Java'         , '//'  ,  '/*'      ,  '*/'   ),
	'.jar'  : ('Java'         , '//'  ,  '/*'      ,  '*/'   ),
	'.class': ('Java'         , '//'  ,  '/*'      ,  '*/'   ),
	'.js'   : ('JavaScript'   , '//'  ,  '/*'      ,  '*/'   ),
	'.m'    : ('Objective-C'  , '//'  ,  '/*'      ,  '*/'   ),
	'.r'    : ('R'            , '#'   ,  ''        ,  ''     ),
	'.swift': ('Swift'        , '//'  ,  '/*'      ,  '*/'   ),
	'.rb'   : ('Ruby'         , '#'   ,  '=begin'  ,  '=end' ),
	'.rbw'  : ('Ruby'         , '#'   ,  '=begin'  ,  '=end' ),
	'.sh'   : ('Bash'         , '#'   ,  '/*'      ,  '*/'   ),
	'.html' : ('HTML'         , ''    ,  '<!--'    ,  '-->'  ),
	'.css'  : ('CSS'          , ''    ,  '/*'      ,  '*/'   )
}

# debug flag. Interesting thing about global python
debug = 0

def setDebug():
	global debug
	debug = 1

def returndebug():
	return debug

# checks line if it is commented or not
def countedLine(line,comment):
	token = ''
	if line.isspace():
		return 0
	for char in line:
		token = token + char
		if len(token) > len(comment):
			return 1
		if token == comment:
			return 0

# counts legit lines if the language has single line, as well as block comments
def count3(path,comment,lcomment,rcomment):
	lines = open(path, 'r')
	count = 0
	flag = True
	for line in lines:
		if lcomment in line and rcomment in line:
			if line.rstrip()[len(line.rstrip()) - 1] != rcomment[len(rcomment) - 1]:
				count = count + 1
				if returndebug():
					print line
			else:
				continue
		elif lcomment in line:
			flag = False
			if line[len(line) - len(line.lstrip())] != lcomment[0]:
				if returndebug():
					print line
				count = count + 1
		elif rcomment in line and flag == False:
			flag = True
			if line.index(rcomment) + len(rcomment) < len(line) - 2:
				if returndebug():
					print line
				count = count + 1
		elif flag and countedLine(line,comment):
			if returndebug():
				print line
			count = count + 1
	return count

# counts legit lines if the language has only single line comments
def count1(path, comment):
	lines = open(path, 'r')
	count = 0
	flag = True
	for line in lines:
		if countedLine(line,comment):
			if returndebug():
				print line
			count = count + 1
	return count

# counts legit lines if the language has only block comments (HTML, CSS)
def count2(path,lcomment,rcomment):
	lines = open(path, 'r')
	count = 0
	flag = True
	for line in lines:
		if lcomment in line and rcomment in line:
			if line.rstrip()[len(line.rstrip()) - 1] != rcomment[len(rcomment) - 1]:
				if returndebug():
					print line
				count = count + 1
			else:
				continue
		elif lcomment in line:
			flag = False
			if line[len(line) - len(line.lstrip())] != lcomment[0]:
				if returndebug():
					print line
				count = count + 1
		elif rcomment in line and flag == False:
			flag = True
			if line.index(rcomment) + len(rcomment) < len(line) - 2:
				if returndebug():
					print line
				count = count + 1
		elif flag and not line.isspace():
			if returndebug():
				print line
			count = count + 1
	return count

# iterates through files and uses respective count
def traverse(filename,cwd,flags):
	myDict = {}
	countFlag = False
	verboseFlag = False
	count = 0
	if 'c' in flags:
		countFlag = True
	if 'v' in flags:
		verboseFlag = True
	for subdir, dirs, files in os.walk(os.path.join(cwd, filename)):
		for file in files:
			path = os.path.join(subdir, file)
			ext = os.path.splitext(path)[1]
			if ext in extensions:
				if verboseFlag:
					print path
				if extensions[ext][0] not in myDict:
					myDict[extensions[ext][0]] = 0
				if extensions[ext][1] == '':
					count = count2(path,extensions[ext][2],extensions[ext][3])
					if countFlag:
						print extensions[ext][0] + ": " + str(count)
					myDict[extensions[ext][0]] += count
				elif extensions[ext][2] == '':
					count = count1(path,extensions[ext][1])
					if countFlag:
						print extensions[ext][0] + ": " + str(count)
					myDict[extensions[ext][0]] += count
				else:
					count = count3(path,extensions[ext][1],extensions[ext][2],extensions[ext][3])
					if countFlag:
						print extensions[ext][0] + ": " + str(count)
					myDict[extensions[ext][0]] += count
	return myDict

# prints contents of dictionary 
def printDict(dictionary,cwd):
	print "\nTotal lines of code in " + cwd
	print "\n---------------------------\n"
	for language, count in sorted(dictionary.iteritems()):
		print '{0:12}  :  {1:10}'.format(language,str(count))
	print "\n---------------------------\n"

# main, get flags and extract command line args.
def main():
	cwd = os.getcwd()
	args = sys.argv
	flag = ''
	if args[1][0] == '-':
		if 'v' in args[1]:
			flag = flag + 'v'
		if 'c' in args[1]:
			flag = flag + 'c'
		if 'd' in args[1]:
			setDebug()
		filename = args[2]
	else:
		filename = args[1]

	returnDict = traverse(filename,cwd,flag)
	printDict(returnDict,cwd + '/' + filename)

if __name__ == "__main__":
	main()