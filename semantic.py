import re
from sys import argv
strmap={}
symbolTable=[]
stack=[];
lstack=[];
top=-1;
temp=1;
label=0;
data=[];
types={};
star =False;
count=ord("a"); 
	
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


def getTok():
	global tableCnt,top,stack,temp,label;
	
	if(tableCnt >= max_s ):
		tableCnt += 1;
		return None;
	
	ret = symbolTable[tableCnt];	
	tableCnt += 1
	return ret;
		
def O():
	global tableCnt,top,stack,temp,label,star;
	x=getTok();#print( x );
	if(x != None and x[0]=="HEADER"):
		#print( x );
		O();
		return
	elif(x[0]=="DATA_TYPE"):
		data.append(x)
		x=getTok();
		if(x[1] != '*'):
			tableCnt -= 1
		else:
			star = True;
		x=getTok();#print( x );
		if(x[0]=="ID"):
			M()
		else:
			s="Expected ID but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
			raise Exception(s)
	else:
		s="Expected HEADER or FUNCTION or DECLARATION but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
		raise Exception(s)
		tableCnt -= 1
		
		return
def M():
	global tableCnt,top,stack,temp,label,star;
	x=getTok();#print( x );
	if(x != None and x[0]=="SYMBOL" and x[1] == "(" ):
		#Dec
		x=getTok();#print( x );
		if(x != None and x[0]=="SYMBOL" and x[1] == ")" ):
			x=getTok();#print( x );
			if(x != None and x[0]=="SYMBOL" and x[1] == "{" ):
				F();
				x=getTok();#print( x );
				if(x != None and x[0]=="SYMBOL" and x[1] == "}" ):
					return
				else:
					s="Expected } but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
					raise Exception(s)
			else:
				s="Expected { but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
				raise Exception(s)
		else:
			s="Expected ) but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
			raise Exception(s)
	else:
		X()
		if(x != None and x[0]=="SYMBOL" and x[1] == ";" ):
			star=False;
			O();
			return
		else:
			s="Expected ; but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
			raise Exception(s)
def F():
	S()
	#P()
	#put $
	return ;
	
def S():
	x=getTok();#print( x );
	global tableCnt,top,stack,temp,label,data,star;
	if(x != None and x[0]=="KEYWORD" and x[1]=="while"):
		x=getTok();#print( x );
		if(x != None and x[0] == "SYMBOL" and x[1] == '(' ):
			Label0();
			B();
			Label1();
			x=getTok();#print( x , "  Here");
		
			if(x != None and x[0] == "SYMBOL" and x[1] == ')' ):
				x=getTok();#print( x  );
				
				if(x != None and x[0] == "SYMBOL" and x[1] == '{' ):
				
					S()
					#x=getTok();#print( x );
					
					if( True ):
						
						x=getTok();#print( x );
						
						if(x != None and x[0] == "SYMBOL" and x[1] == '}' ):
							Label2();
							print("Node "+chr(count)+" ="," while "," | ptr	 to -",stack[top-1].replace("t","N"));
							P();
						else:
							s="Expected } but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
							raise Exception(s) 
				
					else:
						s="Expected ; but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
						raise Exception(s) 
				else:
					s="Expected { but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
					raise Exception(s) 
			else:
				s="Expected ) but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
				raise Exception(s) 
		
		else:
			s="Expected ( but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
			raise Exception(s) 				
		
			
	elif(x[0]=="ID"):
		stack.append(x[1]);
		top+=1;
		x=getTok();#print( x );
		if(x != None and x[0] == "OPERATOR" and x[1] == '=' ):
			stack.append(x[1]);
			top+=1;
			K();
			gen_assign();
			x=getTok();#print( x ,"Here" );
			#print("After K")
			if(x != None and x[0] == "SYMBOL" and x[1] == ';' ):
				P();
				return
			else:
				s="Expected ; but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
				raise Exception(s) 
					
		else:
			s="Expected = but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
			raise Exception(s) 
	
	elif(x != None and  x[0]=="DATA_TYPE"):
		data.append(x);
		x=getTok();
		if(x[1] != '*'):
			tableCnt -= 1
		else:
			star = True;
		
		L()
		x=getTok();#print(x);
		if(x[1] == ";" ):
		
			star = False
			P()
			return
		else:
			s="Expected ; but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
			raise Exception(s)
		
		return 
	else:
		s="Expected ID or KEYWORD but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
		raise Exception(s) 
			
	
def L():
	global tableCnt,top,stack,temp,label;
	x=getTok();#print( x, " L in" ,tableCnt );
	if(x != None and x[0] == "ID" ):
		#print(star);
		addType(x);
		X()
		return
	else:
		s="Expected ID but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
		tableCnt -= 1
		raise Exception(s)

def X():

	global tableCnt,top,stack,temp,label;
	x=getTok();#print( x, " x in" ,tableCnt);
	if(x != None and x[0] == "SYMBOL" and x[1] == ','):
		L()
		return
	else:
		tableCnt -= 1
		return
	data.pop();
		
def K():
	#print("in K")
	T()
	Kdash()

def T():
	#print("in T")
	E()
	Tdash()

def Tdash():
	global tableCnt,top,stack,temp,label;
	
	x=getTok();#print( x ,"In TdaSH");
	
	if(x != None and x[0] == "SYMBOL"  and x[1] == '*'):
		stack.append(x[1]);
		top+=1;
		E()
		codegen();
		Tdash()
		return
	else:
		#print(x , " Tdash Null");
		tableCnt -= 1
		return

def Kdash():
	
	global tableCnt,top,stack,temp,label;
	x=getTok();#print( x,"Kdash" );
	if(x != None and x[0] == "OPERATOR" and x[1] == '+'):
		stack.append(x[1]);
		top+=1;
		
		T()
		codegen();
		Kdash()
		return
	else:
		#print(x , "Null");
		tableCnt -= 1
		return

def P():
	global tableCnt,top,stack,temp,label;
	x=getTok();#print( x );
	if(x!=None and (x[0] == "ID" or x[1]=="while" or x[0] == "DATA_TYPE") ):
		tableCnt -= 1
		##print("In P")
		S()
		return
	else:
	
		tableCnt -= 1
		return
def B():
	global tableCnt,top,stack,temp,label;
	E();
	R();
	E();
	Q();
	return

def Q():
	global tableCnt,top,stack,temp,label;
	x=getTok();#print( x );
	if(x != None and (x[1] == "&&" or x[1] == "||" ) ):
		B();
		codegen();
		Q();
		return
	else:
		tableCnt -= 1;
		codegen();
		return

def E():
	
	global tableCnt,top,stack,temp,label;
	x=getTok();#print( x );
	if(x != None and ((x[0] == "ID" or x[0] == "NUM" or x[0] == "CHAR"  or x[0] == "STRING" ))):
		printLeaf(x);
		stack.append(x[1]);
		top+=1;
		return
	else:
		s="Expected ID OR NUM but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
		raise Exception(s) 

def R():
	global tableCnt,top,stack,temp,label;
	x=getTok();#print( x );
	if(x != None and ( (x[1] == "<=" or x[1] == ">="   or x[1] == ">" or x[1] == "<" or x[1] == "==" or x[1] == "!="  )  )):
	
		stack.append(x[1]);
		top+=1;
		return
	else:
		s="Expected RELOP but Found " + x[1] + "  On Line Number "+ str(x[2]+1)
		raise Exception(s) 



def codegen():
	global tableCnt,top,stack,temp,label,strmap;
	
	
	
	
	if(stack[top-2].isdigit()):
		types[stack[top-2]] ="int"; 
		
	if(stack[top].isdigit()):
		types[stack[top]] ="int";
		
	if(isfloa(stack[top-2])):
		types[stack[top-2]] ="float"; 
		
	if(isfloa(stack[top])):
		types[stack[top]] ="float";
	 
	if(stack[top-2] not in types):
		s="No Declaration Found for " + stack[top-2] ;
		raise Exception(s)
	if(stack[top] not in types):
		s="No Declaration Found for " + stack[top];
		raise Exception(s)
	if((types[stack[top-2]] == "string" or types[stack[top]] == "string" ) ):
		s="Invalid operation on Type char * ";
		raise Exception(s)
	
	if(types[stack[top-2]] == 'float' or types[stack[top]] == 'float'):
		types["t"+str(temp)] = 'float'
	else:
		types["t"+str(temp)] = 'int'
	
	#print(stack,top)
	x=stack[top-2],stack[top-1],stack[top];
	if(x not in strmap):
		strmap[x] = "t"+str(temp);
		#print("t"+str(temp),'=',stack[top-2],stack[top-1],stack[top]);
		print( "Node N"+str(temp) +" = ", stack[top-1], "| ptr to -",stack[top-2].replace("t","N")  ,"| ptr to - "+stack[top].replace("t","N") )
		top-=2;
		stack.pop()
		stack.pop()
		stack[top]="t"+str(temp);
		temp+=1;
	else:
		l = int(strmap[x].replace("t",""));
		#print("t"+str(temp), "=", strmap[x])
		top-=2;
		stack.pop()
		stack.pop()
		stack[top]="t"+str(l);
	
	
def gen_assign():
	global tableCnt,top,stack,temp,label;
	
	

	print( "Node N"+str(temp) +" = ", stack[top-1], "| ptr to -",stack[top-2].replace("t","N")  ,"| ptr to - "+stack[top].replace("t","N") )
	#print(stack[top-2]," = ",stack[top])
	stack.pop()
	stack.pop()
	top-=2;
	


def Label0():
	global tableCnt,top,stack,temp,label;
	#print("L"+str(label),":");
	lstack.append(label);
	label+=1;
	

def Label1():
	global tableCnt,top,stack,temp,label;
	
	
	#print( "t"+str(temp) ,"=" , "not",stack[top]);
	#print("if t"+str(temp),"goto" ,"L"+str(label));
	lstack.append(label);
	label+=1;
	temp+=1;
	
def Label2():
	global tableCnt,top,stack,temp,label;
	x1= lstack.pop();
	x0 = lstack.pop();
	#print("goto L"+str(x0))
	#print("L"+str(x1)," :")
    	
    
def printLeaf(x):
	print("Leaf(",x[1],",",x[2],')')
	   
def addType(x):
	l=data[-1];
	x.append(l[1]);
	
	#print(star , x[1]);	
	if(x[1] in types):
		s= " Conflicting types for " + str(x[1]) + " previously declared "+ str(types[x[1]]) ;
		raise Exception(s)
	
	if(data[-1][1] == 'char' and star == True):
		tp = "string";
		types[x[1]]=tp
	else:
		types[x[1]]=data[-1][1];
	
	
	#print(data)
	#print(types)
	#data.pop();  
		
#print("############### Parsing ###########")			
O();	
		
#print("Compiled Sucessfully")		

	

	
	

