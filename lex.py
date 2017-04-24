import re
from sys import argv
#Removing comments
symbolTable=[]
stack=[];
lstack=[];
top=-1;
temp=1;
label=0;
data=[];
types={};
star =False;
	
def isfloa(element):
	try:
    		float(element)
	except ValueError:
    		return False
	return True;
	
def removecomments():
	with open ("input.c", "r") as myfile:
		string=myfile.read()

	string = re.sub(re.compile("[^\"]/\*.*?\*/",re.DOTALL ) ,"" ,string) 
	# remove all occurance streamed comments (/*COMMENT */) from string
	string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
	#string = re.sub(re.compile("\n{2,}|[\t]+\n|[\t]+") ,"" ,string) # remove multiple spaces
	
	string=string.split("\n")

	with open("output","w+") as f:
		for i in string:
			i+="\n"
			f.write(i.lstrip())
	

removecomments()
valueStack = []
def BuildTable():
	with open ("output", "r") as myfile:
		string=myfile.read()
	
	string=string.replace(';'," ; ").replace("("," ( ").replace(")"," ) ").replace(","," , ").replace("+"," + ").replace("--"," -- ").replace("++"," ++ ").replace("&"," & ").replace("|"," || ").replace("}"," } ").replace("{"," { ").replace("["," [ ").replace("-"," - ").replace("="," = ")
	
	
	if(re.findall("\s*\+\s*\+\s*\+\s*",string)):
		x= re.findall("\s*\+\s*\+\s*\+\s*",string)
		
		for i in x:
			string=string.replace(i," ++ + ");
	if(re.findall("\s*-\s*-\s*-\s*",string)):
		x= re.findall("\s*-\s*-\s*-\s*",string)
	
		
		for i in x:
			string=string.replace(i," -- - ");
	
	if(re.findall("\s*<\s*=\s*",string)):
		x= re.findall("\s*<\s*=\s*",string)
		for i in x:
			string=string.replace(i," <= ");
	if(re.findall("\s*>\s*=\s*",string)):
		x= re.findall("\s*>\s*=\s*",string)
		for i in x:
			string=string.replace(i," >= ");
	
	if(re.findall("\s*&\s*&\s*",string)):
		x= re.findall("\s*&\s*&\s*",string)
		for i in x:
			string=string.replace(i," && ");
	
	program =  string.strip().split('\n')
	#Token Names
	
	header = set(['#include'])
	
	
	
	datatype = {'int','float', 'char','long'}
	
	symbols = set(['_','/','*','`','~','!','@','#','$','%','^','&','(',')','|','"',':',';','{'
,'}','[',']','<','>','?','/',','])
	
	operator = { '=' , '+', '-', '/' , '*', '++' , '--','<=','<' ,">=","&&" ,'||','|','&'}
	
	keyword=set(["while"])
	startQuote = "\""
	singleQuote = "\'"
	lineno =[]
	for i in range(len(program)):
		lis=list(program[i])
		loop=0;
		lol=False
		while(loop != len(lis)):
			##print(lis[loop],lis[loop]=="\"",lol)
			if(lis[loop]=="\""):
				if(lol==False  ):
					lol=True
					
				elif(lol==True):
					lol=False
					
					
			if(lol==True):
				if(lis[loop]==" "):
					lis[loop]="_"
			
		
					
			loop +=1
		program[i] = "".join(lis);		
		
		sp = program[i].split(' ')
		sp = list(map(lambda x: (x,i) ,sp))
		
		lineno += sp;
		
	
	x=len(lineno)
	
	cnt=0;
	global symbolTable;
	symbolTable=[]
	idNo=1;
	while(cnt != x):
		
		tok=lineno[cnt][0];
		
		
		if(tok in header):
			cont=tok;
			if(cnt+1 < x and re.search('<.*>',lineno[cnt+1][0]).group(0) ):
				cnt +=1;
				cont += lineno[cnt][0];
			elif(cnt+1 < x and '<' in lineno[cnt+1][0] ):
				cnt +=1;
				cont += lineno[cnt][0];
				if(cnt+1 < x and re.search('.*\.h',lineno[cnt+1][0]).group(0) ):
					cnt +=1;
					cont += lineno[cnt][0];
				if(cnt+1 < x and '>' in lineno[cnt+1][0] ):
					cnt +=1;
					cont += lineno[cnt][0];
			symbolTable.append(("HEADER",cont,lineno[cnt][1]));
			
		elif(tok in datatype):
			symbolTable.append(("DATA_TYPE",tok,lineno[cnt][1]))
		elif(tok in symbols):
			symbolTable.append(("SYMBOL",tok,lineno[cnt][1]));
		elif(tok in operator):
			symbolTable.append(("OPERATOR",tok,lineno[cnt][1]));
		elif("\"" in tok):
			symbolTable.append(("STRING",tok.replace("_"," "),lineno[cnt][1]))
		elif(tok in keyword):
			symbolTable.append(("KEYWORD",tok.replace("_"," "),lineno[cnt][1]))
		elif(singleQuote in tok):
			symbolTable.append( [("CHAR"),tok,idn,lineno[cnt][1] ])
			
		else:
			if(tok != ""):
				idn = idNo
				Found=False
				for i in symbolTable:
					if(i[0] == "ID"):
						if(tok == i[1]):
							Found=True
							idn=i[2]
			
				if(tok.isdigit()):
					symbolTable.append( [("NUM"),tok,("int"),idn,lineno[cnt][1] ])
				elif(isfloa(tok)):
					symbolTable.append( [("NUM"),tok,("float"),idn,lineno[cnt][1] ])	
				else:	
					symbolTable.append( [("ID"),tok,idn,lineno[cnt][1] ])
				if(Found==True):
					Found =False
				else:
					idNo += 1
		
			
			
		
		cnt +=1;
	
BuildTable();

tableCnt=0;
max_s = len(symbolTable)

for x in range(len(symbolTable)):
	print(symbolTable[x])						

	
	
		

	

	

	
	
	

#Hi!
