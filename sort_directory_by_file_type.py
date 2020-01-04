# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 18:49:44 2020

@author: mtroyer
"""

import os
import shutil

from collections import defaultdict


SHAPEFILES = ('.prj', '.dbf', '.shp', '.shx', '.sbx', '.sbn', '.cpg')


def safe_copy(file_path, out_dir, dst=None):
    """Safely copy a file to the specified directory. If a file with the same name already 
    exists, the copied file name is altered to preserve both.

    :param str file_path: Path to the file to copy.
    :param str out_dir: Directory to copy the file into.
    :param str dst: New name for the copied file. If None, use the name of the original
        file.
    """
    name = dst or os.path.basename(file_path)
    if not os.path.exists(os.path.join(out_dir, name)):
        shutil.copy(file_path, os.path.join(out_dir, name))
    else:
        base, extension = os.path.splitext(name)
        i = 1
        while os.path.exists(os.path.join(out_dir, '{}_({}){}'.format(base, i, extension))):
            i += 1
        shutil.copy(file_path, os.path.join(out_dir, '{}_({}){}'.format(base, i, extension)))
        
        
def sort_directory_by_file_type(input_dir, output_dir):
    """
    Copy all the files in input_dir to output_dir, while resorting into folders according to
    file type. Will group geodatabases (directories ending in .gdb) and shapefile components
    (extensions listed in SAHPEFILES)
    """
    extensions = defaultdict(list) 
    
    for root, dirs, files in os.walk(input_dir):
        if root.lower().endswith('.gdb'):
            # Don't enter these - treat as a file
            extensions['.gdb'].append(root)
            
        else:
            for file in files:
                filepath = os.path.join(root, file)
                
                name, ext = os.path.splitext(file)
                ext = ext.lower()
                
                # Sweep for shapefiles..
                if ext in SHAPEFILES:
                    extensions['.shp'].append(filepath)
                    
                #ADDITIONAL FILTERES HERE
                
                else:
                    extensions[ext].append(filepath)
    
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        
    for ext, files in extensions.items():
        outdir = os.path.join(output_dir, ext)
        if not os.path.exists(outdir):
            os.mkdir(outdir)
            
        if ext == '.gdb':
            # These are actually directories, so use copytree
            for gdb in files:
                outgdb = os.path.join(outdir, os.path.basename(gdb))
                shutil.copytree(gdb, outgdb)
        else:    
            for file in files:
                safe_copy(file, outdir)
        
        
if __name__ == '__main__':

    input_dir = r'.\Input'
    output_dir = r'.\Output'    
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    sort_directory_by_file_type(input_dir, output_dir)
        