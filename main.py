import sys
import os
from os import listdir
from os.path import isfile, join

import utils
from dataanalysis import dataanalysis  as da
from inputoutput import inputoutput as iod

dataset_columns = dict()
ncol_dist = dict()
tcol_dist = dict()

def get_dataset_files(dataset_path):
    '''
        Get all non-hidden files in a given directory
    '''
    files = iod.get_files_in_dir(dataset_path)
    print("Dataset with: " + str(len(files)) + " files")
    return files

def get_dataset_columns_from_files(files):
    ''' 
        Extracts all columns from dataset provided as list of filepaths 
    '''
    #global dataset_columns
    dataset_columns = iod.get_column_iterator_csv(files)
    print("Extracted " + str(len(dataset_columns.items())) +" columns")
    return dataset_columns

def dataset_columns(path):
    '''
       Parses all files in the path and return columns in the dataset 
    '''
    files = get_dataset_files(path)
    columns = get_dataset_columns_from_files(files)
    return columns

def show_columns_of(filename, dataset_columns):
    '''
        Returns the columns of a given file
    '''
    columns = []
    for (fname, cname) in dataset_columns.keys():
        if fname == filename:
            columns.append(cname)
    return columns
    
def get_column(filename, columname, dataset_columns):
    ''' 
        Return the column values
    '''
    key = (filename, columname)
    if key in dataset_columns:
        return dataset_columns[key]

def get_signature_for(column, method):
    ''' 
        Return the distribution for the indicated column,
        according to the provided method
    '''
    return da.get_column_signature(column, method)

def get_similarity_columns(columnA, columnB, method):
    '''
        Return similarity metric given a method (ks)
    '''
    if method == "ks":
        return da.compare_num_columns_dist_ks(columnA, columnB)
    elif method == "odsvm":
        return da.compare_num_columns_dist_odsvm(columnA, columnB)

#def compare_pair_columns(columnA, columnB, method):
#    if method == "ks":
#        return da.compare_num_columns_dist(columnA, columnB)

def columns_similar_to(filename, column):
    '''
        Return columns similar to the provided one,
        according to some notion of similarity
    ''' 
    key = (filename, column)
    sim_vector = None
    if key in ncol_dist:
        dist = ncol_dist[key] 
        sim_vector = da.get_sim_vector_numerical(key, ncol_dist)
    elif key in tcol_dist:
        dist = tcol_dist[key]
        sim_vector = da.get_sim_vector_text(key, tcol_dist)
    # apply filter to get only those 'similar'
    return sim_vector

def analyze_dataset(list_path):
    ''' Gets files from directory, columns from dataset, and distribution for
        each column 
    '''
    all_files_in_dir = iod.get_files_in_dir(list_path)
    print("FILES:")
    for f in all_files_in_dir:
        print(str(f))
    print("Processing " + str(len(all_files_in_dir))+ " files")
    global dataset_columns
    dataset_columns = get_dataset_columns_from_files(all_files_in_dir)

    # Store dataset info in mem
    global ncol_dist
    global tcol_dist
    (ncol_dist, tcol_dist) = get_column_signatures(dataset_columns)
    return (ncol_dist, tcol_dist)

def get_column_signatures(dataset_columns):
    ''' Get signatures for the columns of the dataset '''
    # Get columns of the input table
    # columns = extract_column_information(files)
    (ncol_dist, tcol_dist) = da.get_columns_signature(dataset_columns)
    return (ncol_dist, tcol_dist)

def process_files(files):
    dataset_columns = get_dataset_columns_from_files(files)

    (ncol_dist, tcol_dist) = get_column_signatures(dataset_columns)
    sim_matrix_num = da.get_sim_matrix_numerical(ncol_dist)
    sim_matrix_text = da.get_sim_matrix_text(tcol_dist)
    print("")
    print("Similarity for numerical columns")
    utils.print_dict(sim_matrix_num)
    print("")
    print("Similarity for textual columns")
    utils.print_dict(sim_matrix_text)

def main():
    # Parse input parameters
    mode = sys.argv[1]
    arg = sys.argv[2]
    # Container for files to parse
    files = [] 
    if mode == "-p":
        print('Working on path: ' + str(arg))
        all_files_in_dir = iod.get_files_in_dir(arg)
        for f in all_files_in_dir:
            print(str(f))
        files.extend(all_files_in_dir)
    elif mode == "-f":
        print('Working on file: ' + str(arg))
        files.append(arg)
    print("Processing " + str(len(files))+ " files")
    process_files(files)
   

if __name__ == "__main__":
    if len(sys.argv) is not 3:
        print("HELP")
        print("-p  <path> to directory with CSV files")
        print("-f  <path> to CSV file")
        exit()
    main()
