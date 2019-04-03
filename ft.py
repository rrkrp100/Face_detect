#!Python

#import os

#a=os.system("python /home/rahul/tf_rahul/classify.py test.jpg")
#print (a)
from subprocess import Popen, PIPE

process = Popen(["python", "/home/rahul/tf_rahul/classify.py","test.jpg"], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()
text = 'Face..!!'
if(output[0]=='r'):
	text="Rahul"
else:
	text="Not Rahul"

print(text)
