import sys
sys.path.append('AI')
from AI.test import prediction

# File used to test the AI manually.

text = "Computer programming is the process of designing and building an executable computer program to accomplish a specific computing result or to perform a specific task. Programming involves tasks such as: analysis, generating algorithms, profiling algorithms' accuracy and resource consumption, and the implementation of algorithms in a chosen programming language (commonly referred to as coding)."

# make sure the file is empty
f = open('AI/test/inp.txt', 'r+')
f.truncate(0)
f.close()

inputfile = open("AI/test/inp.txt","a") # write the text to the file
inputfile.write(text)
inputfile.close() 

 # prediction('fast' / 'slow', length)

# Read output file
outputfile = open("AI/test/out.txt", "r")
output = outputfile.read()
outputfile.close
print(output)

