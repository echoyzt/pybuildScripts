#_*_ coding:utf-8 _*_
import os,sys

if __name__ == "__main__":
	view=""
	label=""
	view=sys.argv[1]
	label=sys.argv[2]
	PATH=os.getcwd()
	if '/' in label:pass
	else:
		if os.path.exists(PATH+'/'+view+'/BuildHistory.log'):
			f=open(PATH+'/'+view+'/BuildHistory.log','r')
			while True:
				line = f.readline()
				line = line.rstrip('\n')
				if not line:
					print 'the label '+label+' will create in ST after build success...'
					f.close()
					sys.exit()
				#print line
				if label in line:
					print 'error: Label '+label +' you have build success before. can not be reused...'
					f.close()
					sys.exit(1)
			
		else:
			print 'there is no file BuildHistory.log in '+PATH+'/'+view
			print 'will create BuildHistory.log after build success...'
		
	