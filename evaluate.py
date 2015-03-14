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
    return


def evaluate(soln_direc):
    sol_direc_abs = os.path.abspath(soln_direc);
    #print sol_direc_abs
    solutions = os.listdir(soln_direc)
    #print "Solutions: ", solutions
    evaluations = []
    for solution in solutions:
        #sol_location = os.path.join(sol_direc_abs, solution)
        #print sol_location
        #os.system("./tools/universal.py " + sol_location)
        if compile_files(sol_direc_abs, solution):
            print solution + ": PASSED\n"
            evaluations.append("True")
        else:
            print solution + ": FAILED\n"
            evaluations.append("False")

    clear_compiled_files(sol_direc_abs)
    #print "Results: ", evaluations
    return

def compile_files(path, filename):
    #print "Print: ", os.getcwd()
    name, extension = filename.split(".")
    print "Compiling: ", filename
    #print name, extension

    if extension == 'c':
        input_file = os.path.join(path, filename)
        output_file = os.path.join(path, name)
        command = COMPILE_C + ' ' + input_file + " -o " + output_file
        #print command
        os.system(command)

        command = output_file + " < " + MASTER_INPUT  + name + ".input" + " > " + USER_SOLUTIONS + name + ".output"
        #print command
        os.system(command)

        # compare the output
        #command = "cmp --silent " + MASTER_SOLUTION + name + ".output" + " " + USER_SOLUTIONS + name + ".output"
        #print "comapring 2", MASTER_SOLUTION + name + ".output",  USER_SOLUTIONS + name + ".output"
        return filecmp.cmp(MASTER_SOLUTION + name + ".output",  USER_SOLUTIONS + name + ".output", shallow=False)


        #output = subprocess.check_output(command, shell=True)
        #print "output: ", output
    elif extension == 'cpp':
        input_file = os.path.join(path, filename)
        output_file = os.path.join(path, name)
        command = COMPILE_CPP + ' ' + input_file + " -o " + output_file
        #print command
        os.system(command)

        command = output_file + " < " + MASTER_INPUT  + name + ".input" + " > " + USER_SOLUTIONS + name + ".output"
        #print command
        os.system(command)

        # compare the output
        #command = "cmp --silent " + MASTER_SOLUTION + name + ".output" + " " + USER_SOLUTIONS + name + ".output"
        #print "comapring 2", MASTER_SOLUTION + name + ".output",  USER_SOLUTIONS + name + ".output"
        return filecmp.cmp(MASTER_SOLUTION + name + ".output",  USER_SOLUTIONS + name + ".output", shallow=False)

    elif extension == 'java':
        input_file = os.path.join(path, filename)
        output_file = os.path.join(path, name)
        command = COMPILE_JAVA + ' ' + input_file
        #print command
        os.system(command)
        command = RUN_JAVA + " -cp " + path + " " + name + " < " + MASTER_INPUT  + name + ".input" + " > " + USER_SOLUTIONS + name + ".output"
        #print command

        os.system(command)
        # compare the output
        #command = "cmp --silent " + MASTER_SOLUTION + name + ".output" + " " + USER_SOLUTIONS + name + ".output"
        #print "comapring 2", MASTER_SOLUTION + name + ".output",  USER_SOLUTIONS + name + ".output"
        return filecmp.cmp(MASTER_SOLUTION + name + ".output",  USER_SOLUTIONS + name + ".output", shallow=False)
    else:
        print "Unsupported file format"

def clear_compiled_files(path):
    print "Clearing compiled files generated during evaluating...\n"
    files = os.listdir(path)
    for file in files:
        ext = file.split(".")
        #print "ext: ", ext
        if len(ext) == 1:
            os.system("rm " + path + "/" +  file)
        elif ext[-1] == 'class' or ext[-1] == 'output':
        #elif ext[-1] == 'class':
            os.system("rm " + path + "/" +  file)

if __name__=='__main__':
    main()

