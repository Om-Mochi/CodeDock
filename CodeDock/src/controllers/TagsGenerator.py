import os
import subprocess
import re

def tagsPython(file_path):
	# Run the ctags command
	command=["ctags","-f","-","--fields=+n","--kinds-python=+v",file_path] 
	result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
	tags=[]
	lines=[]
	for line in result.stdout.splitlines():
		if line.startswith("!"):
			continue

		parts = line.split("\t")
		
		if len(parts)>=5:
				
			if len(parts)==4:
				name,pattern,types,line_no,member=parts[0],parts[2],parts[3],parts[4],parts[5]
			else:name,pattern,types,line_no,member=parts[0],parts[2],parts[3],parts[4],None
			#tags.append({"name": tag_name, "pattern": pattern, "line":,"def": components_name})
			

			pattern=pattern.replace("/^","",1)
			pattern=pattern.replace('$/;"',"")
			line_no=line_no.replace("line:","")

			total_strtab=0
			if pattern.startswith('    ')==True:
				total_strtab=pattern.count('    ')
			
			#replace std tabs to html tabs
			pattern=pattern.replace(total_strtab*'    ',total_strtab*'')
			#pattern=f"{line_no} {pattern}"
			#lines.append(line_no)

			if types=='c':
				pattern=f"<span style='color: green;'>class</span> {name}"
			if types=='m':
				pattern=f"<span style='color: yellow;'>def</span> {name}"
			if types=='f':
				pattern=f"<span style='color: pink;'>def</span> {name}"
			
			
			tags.append([int(line_no),types,int(total_strtab),name,pattern,member])

		




	return sorted(tags,key=lambda x: x[0])

#problem in importing PathHandle.py in only this file/....
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_FILE=os.path.join(BASE_DIR, "temp_files")
PY_TEMP_FILE=os.path.join(TEMP_FILE, "tempFilePy.py")

def codeUse(sWord,):
	with open("/home/omx/dt.txt",'r+')as file:
		define_data=file.read()
		split_data=define_data.splitlines()
		for line_num,defines in enumerate(split_data,start=1):
			if defines.startswith(f'{sWord}')==True:pass

def formatPyCode(file_path):
	formated_f=file_path.split('/')
	len_f=len(formated_f)-1
	formated_f_path=file_path.replace(formated_f[len_f],f"{formated_f[len_f].replace('.py','')}_formatted.py")
	
	subprocess.run(['cp',rf'{file_path}',rf'{formated_f_path}'])
	subprocess.run(['python3','-m','black',rf'{formated_f_path}','--line-length','88'])

	return formated_f_path

def showDefines(code):
	current_tab=0
	str_tab=None
	code_list=[]
	code_lines=[]
	code_list=[]
	"""
	if file_path!=None:	
		f_path=formatPyCode(file_path)
	else:f_path=PY_TEMP_FILE"""
	split_data=code.splitlines()
	
	for line_num,split_codes in enumerate(split_data,start=1):
		
		current_tab=0
		if split_codes.startswith('    ')==True:
			current_tab=split_codes.count('    ')
				
		str_tab=current_tab*'    '

		if split_codes.startswith(f'{str_tab}class ')==True:
			code_lines.append(line_num)
			index_of_def=split_codes.find('class')
			index_of_tab=split_codes.find(':')

			split_codes=split_codes.replace(str_tab,current_tab*'&nbsp;&nbsp;&nbsp;&nbsp;')
			split_codes=split_codes.replace(' ',',',1)
			#split_codes=split_codes.replace(split_codes[5],',')
			split_codes=split_codes.replace('(',',')
			split_codes=split_codes.replace(')',',')
			split_codes=split_codes=split_codes.split(',')
			split_codes.insert(0,line_num)
			#split_codes.insert(1,current_tab)
			code_list.append(split_codes)
			

		elif split_codes.startswith(f'{str_tab}def ')==True:
			
			code_lines.append(line_num)
			index_of_def=split_codes.find('def')
			index_of_tab=split_codes.find(':')
			
			split_codes=split_codes.replace(str_tab,current_tab*'&nbsp;&nbsp;&nbsp;&nbsp;')
			#split_codes=split_codes.replace(str_tab,',')
			split_codes=split_codes.replace(' ',',',1)
			split_codes=split_codes.replace('(',',')
			split_codes=split_codes.replace(')',',')
			split_codes=split_codes.split(',')
			
			split_codes.insert(0,line_num)		
			code_list.append(split_codes)
			
	return code_list,len(split_data)

def showDefinesCPP(code):
	current_tab=0
	str_tab=None
	code_list=[]
	code_lines=[]
	code_list=[]
	"""
	if file_path!=None:	
		f_path=formatPyCode(file_path)
	else:f_path=PY_TEMP_FILE"""
	split_data=code.splitlines()
	for line_num,split_codes in enumerate(split_data,start=1):
		
		current_tab=0
		if split_codes.startswith('    ')==True:
			current_tab=split_codes.count('    ')
				
		str_tab=current_tab*'    '

		if split_codes.startswith(f'{str_tab}class ')==True:
			code_lines.append(line_num)
			index_of_def=split_codes.find('class')
			index_of_tab=split_codes.find(':')

			split_codes=split_codes.replace(str_tab,current_tab*'&nbsp;&nbsp;&nbsp;&nbsp;')
			split_codes=split_codes.replace(' ',',',1)
			#split_codes=split_codes.replace(split_codes[5],',')
			split_codes=split_codes.replace('(',',')
			split_codes=split_codes.replace(')',',')
			split_codes=split_codes=split_codes.split(',')
			split_codes.insert(0,line_num)
			#split_codes.insert(1,current_tab)
			code_list.append(split_codes)
			

		elif split_codes.startswith(f'{str_tab}def ')==True:
			
			code_lines.append(line_num)
			index_of_def=split_codes.find('def')
			index_of_tab=split_codes.find(':')
			
			split_codes=split_codes.replace(str_tab,current_tab*'&nbsp;&nbsp;&nbsp;&nbsp;')
			#split_codes=split_codes.replace(str_tab,',')
			split_codes=split_codes.replace(' ',',',1)
			split_codes=split_codes.replace('(',',')
			split_codes=split_codes.replace(')',',')
			split_codes=split_codes.split(',')
			
			split_codes.insert(0,line_num)		
			code_list.append(split_codes)
			
	return code_list,len(split_data)
    
			#print(split_codes[ind:ind1])
"""elif split_codes.startswith('    def')==True:
			code_lines.append(line_num)
			index_of_def=split_codes.find('def')
			index_of_tab=split_codes.find(':')
			split_codes=split_codes.replace(split_codes[8],',')
			split_codes=split_codes.replace('(',',')
			split_codes=split_codes.replace(')',',')
			split_codes=split_codes.split(',')
			split_codes.insert(0,line_num)				
			code_list.append(split_codes)
		"""
		
	


def isCodeComponents(code):
	current_tab=0
	if code.startswith('    ')==True:
		current_tab=code.count('    ')
			
	str_tab=current_tab*'    '

	if code.startswith(f'{str_tab}class')==True:
		return True

	elif code.startswith(f'{str_tab}def')==True:
		return True
	
	return False

if __name__ in '__main__':
	#0,2,3-type,4-line,5-name
	tag=tagsPython('/media/omx/24A2A33AA2A30F7C/Linux/projects/CodeBookN/CodeDock/Features.py')
	for tags in tag:
		print(tags)
