# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 09:42:20 2020

@author: mtroyer
"""

import os
import shutil


def error_handler(func, path, exc_info):  
    print("Error deleting folder..")  
    print(exc_info)
    
    
def find_empty_folders(directory, delete_empty_dirs=False, delete_empty_branches=False):
    """
    Walk <directory> and find empty folders. 
    If delete_empty_dirs is True, the empty folders will be deleted, otherwise the full paths
    are just printed to sdout. If delete_empty_branches is True, will recurse back up and check if
    parent is empty after removing empty folder(s).
    """
    parents = []
    
    found_empty = False
    
    for root, dirs, files in os.walk(directory):
        if not any((dirs, files)):
            found_empty = True
            if delete_empty_dirs:
                shutil.rmtree(root, onerror=error_handler)
                print(f'Removed empty folder: {root}')
                parents.append(os.path.dirname(root))
            else:
                print(f'Found empty folder: {root}')
    if not found_empty:
        print('No empty folders found..')
            
    if delete_empty_dirs and delete_empty_branches:
        for parent in parents:
            find_empty_folders(parent)
            
            
if __name__ == '__main__':
    
    directory = r'C:\Users\mtroyer\Downloads'
    
    find_empty_folders(
            directory,
#            deleteEmpty=False,
            )
                
            
