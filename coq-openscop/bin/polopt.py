import argparse
import shutil

'''
Mocking PolOpt...
'''

def copy_file(source_file, destination_file):
    shutil.copy(source_file, destination_file)

def main():
    parser = argparse.ArgumentParser(description='Copy contents of one file into another')
    parser.add_argument('source', metavar='source_file', help='path to the source file')
    parser.add_argument('-o', '--output', metavar='destination_file', help='path to the destination file')

    args = parser.parse_args()
    source_file = args.source
    destination_file = args.output

    copy_file(source_file, destination_file)

    print('Success: True')
    print('Total time(s): 2.00')
    print('Extractor time(s): 0.10')
    print('Scheduler time(s): 0.10')
    print('Validator time(s): 0.20')
    print('Codegen time(s): 0.10')


if __name__ == '__main__':
    main()
    


