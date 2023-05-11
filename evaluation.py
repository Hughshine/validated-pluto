from enum import Enum
import os
import subprocess
import time

'''
Prerequisite:
    - python3
    - compcert (ccomp), (version 3.12)
'''

'''
Evaluation: 
    - Run PolOpt to generate verified optimized C code
        - Record [PolOpt compilation time]
            - Report whether PolOpt success
                - If yes: 
                    - Extractor / Scheduler / Validator / Codegen time is recorded separately
                - If not:
                    - Report reason (the failing phrase & detailed error message)

    - Compile the original code and the optimized code with CompCert
        - Record [CompCert compilation time for original code] and 
                 [CompCert compilation time for verified code] 
    
    - Run the compiled code
        - Compare the result
        - Record [Execution time for original code] and
                 [Execution time for optimized code]

    * May compare with clang optimized (with and without full pluto support) to see the discrepency
'''

'''
Test suits: 
    - Pluto's test suit first
    - PolyBench 4.3 later maybe
    - Rewrite the unsupported code, update the size of the problem (because effiency may still significantly lag behind unverified production compiler) 
'''

'''
Expectation:
    - PolOpt is applicable, gain speed-up for most cases, with scheduling/tiling only 
        - Which also suggests the validator has acceptable completeness
    - PolOpt, especially the validator's execution time is acceptable
        - Comparing to pluto's compilation time
'''

default_tests = [
    ('examples/matmul', 'matmul.c'),
    ('examples/matmul-init', 'matmul-init.c')
]

absroot = os.path.abspath('.')

# PolOpt
polopt_base = [
    'python3',
    absroot + '/coq-openscop/bin/' + 'polopt.py',
]

# Compcert
ccomp = [
    'ccomp',  # user should install compcert himself, seen CompCert doc 
]
def print_header(message): 
    print("\033[97m{}\033[0m".format(message))

def print_error(message):
    print("\033[91m{}\033[0m".format(message))

def print_info(message):
    print("\033[94m{}\033[0m".format(message))

def print_delimiter_line():
    delimiter = '-' * 40
    gray_color_code = '\033[90m'  # ANSI escape sequence for gray color
    reset_color_code = '\033[0m'  # ANSI escape sequence to reset color

    print(f"{gray_color_code}{delimiter}{reset_color_code}")

start_time = time.time()
end_time = time.time()

def tic():
    global start_time
    start_time = time.time()

def toc():
    global end_time
    end_time = time.time()
    return end_time - start_time


import yaml

class PerformanceData:
    def __init__(self, success, total_time, extractor_time, scheduler_time, validator_time, codegen_time):
        self.success = success
        self.total_time = total_time
        self.extractor_time = extractor_time
        self.scheduler_time = scheduler_time
        self.validator_time = validator_time
        self.codegen_time = codegen_time
    def __str__(self):
        return f"Success: {self.success}, Total time: {self.total_time}s, Extractor time: {self.extractor_time}s, Scheduler time: {self.scheduler_time}s, Validator time: {self.validator_time}s, Codegen time: {self.codegen_time}s"

def parse_performance_data(data_string):
    # Convert YAML string to Python dictionary
    data_dict = yaml.safe_load(data_string)

    # Extract values from the dictionary
    success = data_dict.get('Success', False)
    total_time = data_dict.get('Total time(s)', 0.0)
    extractor_time = data_dict.get('Extractor time(s)', 0.0)
    scheduler_time = data_dict.get('Scheduler time(s)', 0.0)
    validator_time = data_dict.get('Validator time(s)', 0.0)
    codegen_time = data_dict.get('Codegen time(s)', 0.0)

    performance_data = PerformanceData(success, total_time, extractor_time, scheduler_time, validator_time, codegen_time)
    return performance_data

def run(dic, file):
    print_delimiter_line()
    print_header(f"Testing on {dic}/{file}")
    orig_dic = os.getcwd()
    os.chdir(dic)
    filebase = os.path.splitext(file)[0]
    opt_file = filebase + '.polopt.c'
    # 1. PolOpt the original code
    result = subprocess.run(
        polopt_base + [file, '-o', opt_file],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print_error(f"Exception[PolOpt][{dic}/{file}]:\n{result.stderr}")
        return 
    report = parse_performance_data(result.stdout)
    # print(str(report))
    if report.success == False:
        print_error(f"Failed[PolOpt][{dic}/{file}]:\n{result.stderr}")
        return
    # 2. Compile the original code with CompCert
    tic()
    result_ccomp_orig = subprocess.run(
        ccomp + [file, '-o', filebase + '.orig.out'],
        capture_output=True, text=True
    )
    time_ccomp_orig = toc()
    print_info(f"Compilation time[{dic}/{file}][Original]: {time_ccomp_orig:.2f} seconds")
    tic()
    result_ccomp_opt = subprocess.run(
        ccomp + [opt_file, '-o', filebase + '.polopt.out'],
        capture_output=True, text=True
    )
    time_ccomp_opt = toc()
    print_info(f"Compilation time[{dic}/{opt_file}][Opt]: {time_ccomp_opt:.2f} seconds")
    if result_ccomp_orig.returncode != 0:
        print_error(f"Exception[CompCert][{dic}/{file}][Original]:\n{result_ccomp_orig.stderr}")
        return
    if result_ccomp_opt.returncode != 0:
        print_error(f"Exception[CompCert][{dic}/{file}][Opt]:\n{result_ccomp_opt.stderr}")
        return
    # assert (result_ccomp_opt.returncode == 0 and result_ccomp_orig.returncode == 0)
    tic()
    result_exec_orig = subprocess.run(
        './' + filebase + '.orig.out',
        capture_output=True, text=True
    )
    time_exec_orig = toc()
    print_info(f"Execution time[{dic}/{file}][Original]: {time_exec_orig:.2f} seconds")
    tic()
    result_exec_opt = subprocess.run(
        './' + filebase + '.polopt.out',
        capture_output=True, text=True
    )
    time_exec_opt = toc()
    print_info(f"Execution time[{dic}/{opt_file}][Opt]: {time_exec_opt:.2f} seconds")
    assert (result_exec_orig.returncode == 0 and result_exec_opt.returncode == 0)

    os.chdir(orig_dic)

def runall():
    for (dic, file) in default_tests:
        run(dic, file)

def cleanall():
    pass

runall()

