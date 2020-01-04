# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:19:36 2019

@author: mtroyer
"""

import os
from filecmp import dircmp
 

#dir1 = r'.\Test\Test1.gdb'
#dir2 = r'.\Test\Test3.gdb'

dir1 = r'.\Test\Dir1'
dir2 = r'.\Test\Dir2'

dcmp = dircmp(dir1, dir2)

def report_differences(dir1, dir2):
    
    def dcmp_report(name, dcmp, level=0):
        indent = '\t' * level
        print('\n{}'.format(indent) + ' {} '.format(name).center(40, '-'))

        if name.endswith('.gdb'):
            print('{}* Found a geodatabase..'.format(indent))
            if dcmp.diff_files:
                print('{}* Geodatabases are different..'.format(indent))
            else:
                print('{}* Geodatabases are the same..'.format(indent))
            return
        
        # print('{}{} folders in common..'.format(indent, len(dcmp.common_files)))

        if not dcmp.common_files:
            print('{} * No common files..'.format(indent))
        else:
            print('{} * {} files in common..'.format(indent, len(dcmp.common_files)))
            if dcmp.right_only:
                print('\t{}{} file(s) in right dir only..'.format(indent, len(dcmp.right_only)))
            if dcmp.left_only:
                print('\t{}{} file(s) in left dir only..'.format(indent, len(dcmp.left_only)))
            
            if not dcmp.diff_files:
                print('{} * All common files are the same..'.format(indent))
            elif not dcmp.same_files:
                print('{} * All common files are different..'.format(indent))
            else:
                print('{}[-] Same files:'.format(indent))
                for same_file in dcmp.same_files:
                    print('{} * {}'.format(indent, same_file))
                print()
                print('{}[-] Different files:'.format(indent))
                for diff_file in dcmp.diff_files:
                    print('{} * {}'.format(indent, diff_file))
                if dcmp.funny_files: 
                    print('{}[-] Weird stuff:'.format(indent))
                    for funny_file in dcmp.funny_files:
                        print('{} * {}'.format(indent, funny_file))

            if dcmp.common_dirs:
                print('\n{} + [Common directories]'.format(indent))
                for common_dir in dcmp.common_dirs:
                    print('{} *  {}'.format(indent, common_dir))
                    
            # Recurse
            if dcmp.subdirs:
                next_level = level + 1
                for name, subdir in dcmp.subdirs.items():
                    dcmp_report(name, subdir, next_level)


    name = os.path.basename(dir1) + " | " + os.path.basename(dir2)
    dcmp_report(name, dircmp(dir1, dir2))

    
report_differences(dir1, dir2)
