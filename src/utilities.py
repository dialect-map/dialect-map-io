import os
import re
import glob
import csv


def sorted_files(globber: str):
    # from  https://github.com/quynhneo/arxiv-public-datasets/blob/master/arxiv_public_data/fulltext.py
    """
    Give a globbing expression of files to find. They will be sorted upon
    return.  This function is most useful when sorting does not provide
    numerical order,
    e.g.:
        9 -> 12 returned as 10 11 12 9 by string sort
    In this case use num_sort=True, and it will be sorted by numbers in the
    string, then by the string itself.
    Parameters
    ----------
    globber : str
        Expression on which to search for files (bash glob expression)
    """
    files = glob.glob(globber, recursive=True)  # return a list of path, including sub directories
    files.sort()

    allfiles = []

    for fn in files:
        nums = re.findall(r'\d+', fn)  # regular expression, find number in path names
        data = [str(int(n)) for n in nums] + [fn]
        # a list of [first number, second number,..., filename] in string format otherwise sorted fill fail
        allfiles.append(data) # list of list

    allfiles = sorted(allfiles)
    return [f[-1] for f in allfiles]  # sorted filenames


def get_all_paths(all_txt_dir: str, filename='all_paths_str.dat') -> str:
    """ input:
            all_txt_dir: directory contains all articles in txt format
            filename: where the output is stored, in a single row, csv
        output:
            path to filename
    """
    if not os.path.exists(os.path.join(all_txt_dir, filename)):
        #  if the file containing paths does not exist
        globber = os.path.join(all_txt_dir, '**/*.txt')  # search expression for glob.glob
        txtfiles = sorted_files(globber)  # a list of path
        all_paths_str = ",".join(txtfiles)
        print('the number of text files: {} '.format(len(txtfiles)))

        if len(txtfiles) < 1:
            raise Exception('no text files in directory')
        else:
            with open(os.path.join(all_txt_dir, filename), 'w') as file:
                file.write(all_paths_str)
    else:
        print('file with list of paths exists: ', filename)
        with open(os.path.join(all_txt_dir, filename), 'r') as f:
            all_paths_str = f.readline()

        if all_paths_str.strip() == "":  # empty
            raise Exception('no paths found')

        num_commas = all_paths_str.count(',')
        if num_commas == 0:  # there are no comma
            num_files = 1
        else:
            num_files = num_commas + 1

        print(type(all_paths_str), 'number of text file paths saved: ', num_files)

    # log.info('Searching "{}"...'.format(globber))
    return all_paths_str


def get_all_paths2(all_txt_dir: str, filename='all_paths.csv') -> str:
    """ input:
            all_txt_dir: directory contains all articles in txt format
            filename: where the output is stored, single column, each row is a path to a text file
        output:
            path to filename
    """
    if not os.path.exists(os.path.join(all_txt_dir, filename)):
        globber = os.path.join(all_txt_dir, '**/*.txt') # search expression for glob.glob
        txtfiles = sorted_files(globber)  # a list of path
        with open(os.path.join(all_txt_dir, filename), 'w') as file:
            writer = csv.writer(file)
            for path in txtfiles:
                writer.writerow([path])
    else:
        print('csv of all paths in column format exists ')

    return os.path.join(all_txt_dir, filename)


def to_csv_line(data):
    return ','.join(str(d) for d in data)


def dir2rdd(all_txt_dir: str, sc, part_num=1000):
    """ serialize all text files in a folder """

    #  getting all the txt files, put in a string of comma separated string of paths
    all_paths_str = get_all_paths(all_txt_dir)

    # load all text files into spark rdd. 1000 partition, about MB each. took 1 hour for 20 cores
    rdd = sc.wholeTextFiles(all_paths_str, part_num)  # each element [('file: path',  content<str> ), ( ) ,... ]
    return rdd


def read_or_load_rdd(all_txt_dir: str, sample_size: float, rdd_content_dir: str, sc):
    """ input:
        - all_txt_dir: where all text files are
        - sample_size: float, between 0-1, randomly sample a portion of data
        - rdd_content_dir: where to load/save rdd
        - sc: spark context
        output
        - rdd_content containing tuple of string (file,file_content)
    """
    if not os.path.exists(rdd_content_dir):
        # rdd format of data doesn't exist, read from text
        print('reading data from text files')
        rdd = dir2rdd(all_txt_dir, sc)  # return a list of tuple (path, content)
        rdd_sample = rdd.sample(False, sample_size, 2020)
        rdd_content = rdd_sample
        print('saving rdd')
        rdd_content.saveAsTextFile(rdd_content_dir)  # save all tuples, flatten as string

    # load rdd
    print('loading saved rdd')
    rdd_content = sc.textFile(rdd_content_dir)
    if not rdd_content.take(1):
        raise Exception("empty rdd folder")
    return rdd_content

