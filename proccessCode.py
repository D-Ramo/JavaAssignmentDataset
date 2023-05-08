import os
import pandas as pd
import re
from datetime import datetime
import subprocess
import time
import random


directory = '.\Data'


#pattern for file name so extract info
filename_pattern = r"Assignment #(\d+)_(\d+)_attempt_(\d{4}-\d{2}-\d{2})-(\d{2}-\d{2}-\d{2})_Problem_(\d+)\.java"

#read file and store content into array
file_list = []
for filename in os.listdir(directory):
    with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as f:
        file_contents = f.read()
        file_list.append(file_contents)

'''def check_filename_match(directory, filename_pattern):
    file_names = os.listdir(directory)
    random.seed(time.time())
    file_names = file_names[random.randint(1 ,len(file_names) - 1)]
    if re.match(filename_pattern, filename):
        print(f"Filename '{filename}' matches the pattern.")
        return True
    else:
        print(f"Filename '{filename}' does not match the pattern.")
        return False'''

#extract info from file name such as id assigment number attempt time and date and problem number
def title_extraction(directory,filename_pattern):

    ids = []
    assignment_numbers = []
    attempt_dates = []
    attempt_times = []
    problem_numbers = []

    for filename in os.listdir(directory):
        match = re.match(filename_pattern, filename)
        if match:
            ids.append(match.group(2))  # matach id in the name of the file

            assignment_numbers.append(match.group(1))  # get assigenment number
            # get date and time from regex too
            attempt_dates.append(datetime.strptime(
                match.group(3), '%Y-%m-%d').date())

            attempt_times.append(datetime.strptime(
                match.group(4), '%H-%M-%S').time())

            problem_numbers.append(match.group(5))
        else:
            # remove the file if it's not matched
            os.remove(os.path.join(directory, filename))
    return ids, assignment_numbers, attempt_dates, attempt_times, problem_numbers

    # Count the number of lines in the file
def coun_lines(directory, file_list):
    line_count_list = []

    for file_contents in zip(os.listdir(directory), file_list):
        line_count = file_contents.count('\n') + 1
        line_count_list.append(line_count)
    return line_count_list


#rename files to write on the files as valid class names
def rename_files(directory):
    for filename in os.listdir(directory):
        rename_pattern = r"Assignment #(\d+)_(\d+)_attempt_(\d{4}-\d{2}-\d{2})-(\d{2}-\d{2}-\d{2})_Problem_(\d+)\.java"
        match = re.match(rename_pattern, filename)
        new_file_name = f"Assigenment{match.group(1)}_Problem{match.group(5)}_{match.group(2)}" + '.java'
        os.rename(os.path.join(directory, filename),
                  os.path.join(directory, new_file_name))



# rename to the name of each file so it runs without errors 
def rename_classes(directory):
    for filename in os.listdir(directory):

        with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as f:
            file_contents = f.read()
        # Replace the target string
        new_name = filename.replace('.java', '')
        file_contents = re.sub(r"(public\s+)?class\s+\w+",
                               'public class ' + new_name, file_contents)

        # Write the file out again
        with open(os.path.join(directory, filename), 'w', encoding='utf-8', errors='ignore') as f:
            f.write(file_contents)




# check if java file is compiled or not and execution time
def check_code(directory):
    compile_status_list = []
    execution_time_list = []

    for filename in os.listdir(directory):
        if filename.endswith(".java"):  
            try:
                java_file_path = os.path.join(directory, filename)
                class_file_path = java_file_path[:-5] + ".class"
                
                start_time = time.time()
                compile_status = subprocess.call(["javac", java_file_path])
                end_time = time.time()
                
                if compile_status == 0:
                    compile_status_str = "Compiled successfully"
                else:
                    compile_status_str = "Compilation error"
                
                execution_time = end_time - start_time
                compile_status_list.append(compile_status_str)
                execution_time_list.append(execution_time)                
                
                if os.path.exists(class_file_path):
                    os.remove(class_file_path)
            except subprocess.CalledProcessError:
                execution_time_list.append(("Error", None))
    return compile_status_list, execution_time_list

def count(directory):
    variable_count_list = []
    loop_count_list = []
    function_count_list = []
    if_statement_count_list=[]
    elif_statement_count_list =[]
    else_statement_count_list = []

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r',encoding='utf-8', errors='ignore') as f:
            file_content = f.read()
        #check how many variables in each file
        variable_declarations = re.findall(r"\b\w+\s+\w+(\s*=\s*\w+)?\s*;", file_content)

        #check how many loops are in each file
        loop_structures = re.findall(r"(for|while|do-while)\s*\([^)]*\)", file_content)

        #check how many funtions
        function_declarations = re.findall(r"(\w+)\s+\w+\([^)]*\)\s*{", file_content)

        #count number of if statements
        if_statements = re.findall(r"\bif\b", file_content)

        else_statements = re.findall(r"\belse\b", file_content)

        elif_statements = re.findall(r"\belse\s+if\b", file_content)

        variable_count = len(variable_declarations)
        variable_count_list.append(variable_count)

        loop_count= len(loop_structures)
        loop_count_list.append(loop_count)

        function_count = len(function_declarations)
        function_count_list.append(function_count)

        if_statement_Count = len(if_statements)
        if_statement_count_list.append(if_statement_Count)

        else_statement_Count= len(else_statements)
        else_statement_count_list.append(else_statement_Count)

        elif_count=len(elif_statements)
        elif_statement_count_list.append(elif_count)
    return function_count_list, variable_count_list, loop_count_list, if_statement_count_list, elif_statement_count_list, else_statement_count_list

ids, assignment_numbers, attempt_dates, attempt_times, problem_numbers = title_extraction(directory, filename_pattern)
lines = coun_lines(directory,file_list)
rename_files(directory)
rename_classes(directory)
compile_status, execution_time = check_code(directory)
functions, variables, loops, ifs ,elifs,elses = count(directory)

print("Length of 'ids':", len(ids))
print("Length of 'assignment_numbers':", len(assignment_numbers))
print("Length of 'attempt_dates':", len(attempt_dates))
print("Length of 'attempt_times':", len(attempt_times))
print("Length of 'problem_numbers':", len(problem_numbers))
print("Length of 'lines':", len(lines))
print("Length of 'compile_status':", len(compile_status))
print("Length of 'execution_time':", len(execution_time))
print("Length of 'functions':", len(functions))
print("Length of 'variables':", len(variables))
print("Length of 'loops':", len(loops))
print("Length of 'ifs':", len(ifs))
print("Length of 'elifs':", len(elifs))
print("Length of 'elses':", len(elses))


data_dict = {
    "ids": ids,
    "assignment_number": assignment_numbers,
    "problem_number": problem_numbers,
    "attempt date": attempt_dates,
    "attempt time": attempt_times,
    "line count": lines,
    "compile status":compile_status,
    "execution time":execution_time,
    "function count": functions,
    "varirable count": variables,
    "loop count": loops,
    "if statements": ifs,
    "else if statements": elifs,
    "else_statements": elses
}
df = pd.DataFrame(data_dict)
df.to_excel("output.xlsx", index=False)


print(df)
