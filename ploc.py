import os
import sys

extensions = {
	'.py'   : ('Python'       , '#'   ,  '/*'  ,  '*/' ),
	'.c'    : ('C'            , '//'  ,  '/*'  ,  '*/' ),
	'.cpp'  : ('C++'          , '//'  ,  '/*'  ,  '*/' ),
	'.cs'   : ('C#'           , '///' ,  '/*'  ,  '*/' ),
	'.java' : ('Java'         , '//'  ,  '/*'  ,  '*/' ),
	'.jar'  : ('Java'         , '//'  ,  '/*'  ,  '*/' ),
	'.class': ('Java'         , '//'  ,  '/*'  ,  '*/' ),
	'.js'   : ('JavaScript'   , '//'  ,  '/*'  ,  '*/' ),
	'.m'    : ('Objective-C'  , '//'  ,  '/*'  ,  '*/' ),
	'.r'    : ('R'            , '#'   ,  '/*'  ,  '*/' ),
	'.swift': ('Swift'        , '//'  ,  '/*'  ,  '*/' ),
	'.rb'   : ('Ruby'         , '#'   ,  '/*'  ,  '*/' ),
	'.rbw'  : ('Ruby'         , '#'   ,  '/*'  ,  '*/' ),
	'.sh'   : ('Bash'         , '#'   ,  '/*'  ,  '*/' )
}

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

def count(path,comment,lcomment,rcomment):
	lines = open(path, 'r')
	count = 0
	flag = True
	for line in lines:
		if lcomment in line:
			print str(1)
			flag = False
			if line[len(line) - len(line.lstrip()):] != lcomment[0]:
				count = count + 1
		elif rcomment in line and flag == False:
			flag = True
			if line.index(rcomment) + len(rcomment) < len(line) - 2:
				count = count + 1
		elif flag and countedLine(line,comment) and flag:
			print str(3)
			count = count + 1
	return count

def traverse(args,cwd,flags):
	myDict = {}
	indx = 1
	if flags != "":
		indx = 2
	for subdir, dirs, files in os.walk(os.path.join(cwd, args[indx])):
		for file in files:
			path = os.path.join(subdir, file)
			ext = os.path.splitext(path)[1]
			if ext in extensions:
				if 'v' in flags:
					print path
				if extensions[ext][0] not in myDict:
					myDict[extensions[ext][0]] = 0
				myDict[extensions[ext][0]] += count(path,extensions[ext][1],extensions[ext][2],extensions[ext][3])
	return myDict

def printDict(dictionary,cwd):
	print "\nTotal lines of code in " + cwd
	print "\n---------------------------\n"
	for language, count in sorted(dictionary.iteritems()):
		print '{0:12}  :  {1:10}'.format(language,str(count))
	print "\n---------------------------\n"

def main():
	cwd = os.getcwd()
	args = sys.argv
	flag = ''
	if args[1][0] == '-':
		if 'v' in args[1]:
			flag = flag + 'v'
	returnDict = traverse(args,cwd,flag)
	printDict(returnDict,cwd)

if __name__ == "__main__":
	main()