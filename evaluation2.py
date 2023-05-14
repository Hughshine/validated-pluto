from enum import Enum
import os
import subprocess
import scophelper 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--scheduling", action="store_true", help="Enable scheduling")
parser.add_argument("--tiling", action="store_true", help="Enable tiling")
parser.add_argument("--both", action="store_true", help="Enable both scheduling and tiling")

args = parser.parse_args()

scheduling = args.scheduling
tiling = args.tiling
both = args.both

'''
Evaluation: 
    - Run pluto to generate the scheduled (only schedule changed) / tiled / both scheduled and tiled code
        - Generate openscops (the polyhedral representation) before and after the 
          scheduling pass for each of the above
        - Record [pluto compilation time]   
    - Run validator on each pair of openscops
        - Record [validator's result]
        - Record [validator's execution time]
    - Along with original code, compile and run the code
        - Record [generated code's execution time]
    - Figures are drawn acording to these data
'''

'''
Expectation:
    - Validator's completeness is acceptable
        - Tiled / scheduled code is fully supported, unless the code is quasi-affine. This covers significant portion of possible transformation 
        - These validated code gains appreciable speed up
    - Validator's execution time is acceptable
        - Comparing to pluto's compilation time
'''

'''
Questions: 
    - how pet/clan differ?
'''

default_tests = [
    ('examples/matmul', 'matmul.c'),
    ('examples/adi', 'adi.c'),
]

absroot = os.path.abspath('.')


pluto_base = [
    absroot + '/polycc.sh',
    '--nointratileopt',     # ?
    '--nodiamond-tile',     
    '--noprevector',
    '--nofuse',             #  It seems fusion is important? Can we support it?
    '--nounrolljam',
    '--noparallel',
    # '--moredebug',
    # '--rar',              # use rar dependences
]

# pluto_none = pluto_base + ['--notile']
pluto_sched = pluto_base + ['--notile']
pluto_sched_and_tiles = pluto_base + ['--tile'] 


validator_base = [
    'sh',
    absroot + '/validator/validator.sh',
]

# validator + tiling

clang_command = [
    'clang',
    '-O3',
    '-march=native',
    '-mtune=native',
    '-ffast-math',   # fir matmul
    '-lm',
    '-DTIME',
]


class TestTy(Enum): 
    NONE = 'NONE' 
    SCHED_ONLY = 'SCHED_ONLY'
    TILE_ONLY = 'TILE_ONLY'
    SCHED_AND_TILE = 'SCHED_AND_TILE'

# print([ty.value for ty in TestTy])

def run_pluto_fragment(filebase, ty):
    pass

def run_pluto(filebase, ty):
    if ty is TestTy.SCHED_ONLY:
        command = pluto_sched \
            + [filebase + '.c'] \
            + ['-o', filebase + '.' + ty.value + '.c']
        result = subprocess.run(command, capture_output=True, text=True)
        print(result)
    if ty is TestTy.SCHED_AND_TILE: 
        command = pluto_sched_and_tiles \
            + [filebase + '.c'] \
            + ['-o', filebase + '.' + ty.value + '.c']
        result = subprocess.run(command, capture_output=True, text=True)
        print(result)
    
    # if ty is TestTy.NONE: 
    #     return
    # elif ty is TestTy.SCHED_ONLY: 
    #     # command = base_command + ['-s', file]
    #     pass
    # elif ty is TestTy.TILE_ONLY: 
    #     pass
    #     # command = base_command + ['-t', file]
    # elif ty is TestTy.SCHED_AND_TILE: 
    #     command = pluto_sched_and_tiles \
    #         + [filebase + '.c'] \
    #         + ['-o', filebase + '.' + ty.value + '.c' + '.fragment']
    #     result = subprocess.run(command, capture_output=True, text=True)
    #     print(result)
    # concat

    pass 

def run_validation(filebase, ty):
    command = validator_base
    pass 

def run_clang(filebase, ty):
    pass 

def run_generated(filebase, ty):
    pass 

def collect_statistics():
    pass

def run(dic, file):
    print(args)
    work_dic = os.getcwd()
    os.chdir(dic)
    filebase = os.path.splitext(file)[0]
    # command = base_command + [target_test_dic]
    if scheduling and not tiling:
        run_pluto(filebase, TestTy.SCHED_ONLY)
    elif tiling and not scheduling:
        run_pluto(filebase, TestTy.TILE_ONLY)
    elif both or (scheduling and tiling):
        run_pluto(filebase, TestTy.SCHED_AND_TILE)

    # run_validation(filebase, ty)    # supposing single scop per file
    # run_clang(filebase, ty)            
    # run_generated(filebase, ty)
        # command = clang_command + ['-DTIME', 'matmul.c', '-o', 'orig', '-lm']
        # result = subprocess.run(command, capture_output=True, text=True)
    # except err: 
    #     print(err)
    # Check the command execution status
        # if result.returncode == 0:
        #     print(result)
        # else:
        #     print("failed")
    os.chdir(work_dic)

# def clean(dic, file):
#     os.chdir(dic)
#     try: 
#         for ty in TestTy:
#             pass 
#     except err: 
#         print(err)

# def cleanall():
#     for (dic, file) in default_tests:
#         clean(dic, file)
    # pass

def runall(): 
    for (dic, file) in default_tests:
        run(dic, file)
    collect_statistics()

runall()
# cleanall()
# support single scop
# support single project with multiple scop in it (main.c)
