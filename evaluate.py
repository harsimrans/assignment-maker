#!/usr/bin/env python2
#
# evaluate.py - evaluates the users programs
#
# Copyright (c) 2015 Harsimran Singh <me@harsimransingh.in>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import subprocess
import filecmp

MASTER_SOLUTION = './assignment/output_files/'
MASTER_INPUT = './assignment/input_files/'
#TOOLS = './tools'
USER_SOLUTIONS = './user_solution/'
#USER_OUTPUT = './user_solution/output_files'

# modify this section to include more functionality like
# display warning  and other flags
COMPILE_C = 'gcc'
COMPILE_CPP = 'g++'
COMPILE_JAVA = 'javac'
RUN_JAVA = 'java'


def main():
    print "--------------------------------------------"
    print "*              Evaluating                  *"
    print "--------------------------------------------\n"
    evaluate(USER_SOLUTIONS)
    return 0


def evaluate(soln_direc):
    ''' Runs the evaluation of the user solutions
    '''
    sol_direc_abs = os.path.abspath(soln_direc);
    solutions = os.listdir(soln_direc)
    evaluations = []
    for solution in solutions:
        if compile_files(sol_direc_abs, solution):
            print solution + ": PASSED\n"
            evaluations.append("True")
        else:
            print solution + ": FAILED\n"
            evaluations.append("False")

    clear_compiled_files(sol_direc_abs)
    return

def compile_files(path, filename):
    ''' Compiles and runs user solution and tells
        if the output matches the master solution

        returns
            True: If the files match
            False: If the output files don't match
    '''
    name, extension = filename.split(".")
    print "Compiling: ", filename

    if extension == 'c':
        input_file = os.path.join(path, filename)
        output_file = os.path.join(path, name)

        command = COMPILE_C + ' ' + input_file + " -o " + output_file
        os.system(command)

        command = output_file + " < " + os.path.join(os.path.abspath(MASTER_INPUT),  name + ".input") + " > " + os.path.join(os.path.abspath(USER_SOLUTIONS), name + ".output")
        os.system(command)

        # compare the output
        return filecmp.cmp(os.path.join(os.path.abspath(MASTER_SOLUTION) , name + ".output"),  os.path.join(os.path.abspath(USER_SOLUTIONS) , name + ".output"), shallow=False)


    elif extension == 'cpp':
        input_file = os.path.join(path, filename)
        output_file = os.path.join(path, name)

        command = COMPILE_CPP + ' ' + input_file + " -o " + output_file
        os.system(command)

        command = output_file + " < " + os.path.join(os.path.abspath(MASTER_INPUT),  name + ".input") + " > " + os.path.join(os.path.abspath(USER_SOLUTIONS), name + ".output")
        os.system(command)

        # compare the output
        return filecmp.cmp(os.path.join(os.path.abspath(MASTER_SOLUTION) , name + ".output"),  os.path.join(os.path.abspath(USER_SOLUTIONS) , name + ".output"), shallow=False)


    elif extension == 'java':
        input_file = os.path.join(path, filename)
        output_file = os.path.join(path, name)

        command = COMPILE_JAVA + ' ' + input_file
        os.system(command)

        command = RUN_JAVA + " -cp " + path + " " + name + " < " + os.path.join(os.path.abspath(MASTER_INPUT) , name + ".input") + " > " + os.path.join(os.path.abspath(USER_SOLUTIONS) , name + ".output")
        os.system(command)

        # compare the output
        return filecmp.cmp(os.path.join(os.path.abspath(MASTER_SOLUTION) , name + ".output"),  os.path.join(os.path.abspath(USER_SOLUTIONS) , name + ".output"), shallow=False)

    else:
        print "Unsupported file format"
        return False

def clear_compiled_files(path):
    ''' Clears all the output and class files
        generated duruing the evaluation process
    '''
    print "Clearing compiled files generated during evaluating...\n"
    files = os.listdir(path)
    for file in files:
        ext = file.split(".")
        if len(ext) == 1:
            os.system("rm " + path + "/" +  file)
        elif ext[-1] == 'class' or ext[-1] == 'output':
            os.system("rm " + path + "/" +  file)

if __name__=='__main__':
    main()

