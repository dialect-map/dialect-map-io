import os
import re
import glob
import pyspark

from pyspark import SparkConf, SparkContext

def sorted_files(globber: str):# from  https://github.com/quynhneo/arxiv-public-datasets/blob/master/arxiv_public_data/fulltext.py
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
    files = glob.glob(globber, recursive = True) # return a list of path, including sub directories
    files.sort()

    allfiles = []

    for fn in files:
        nums = re.findall(r'\d+', fn) # regular expression, find number in path names
        data = [str(int(n)) for n in nums] + [fn]
        # a list of [first number, second number,..., filename] in string format otherwise sorted fill fail
        allfiles.append(data) # list of list

    allfiles = sorted(allfiles)
    return [f[-1] for f in allfiles] # sorted filenames

if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("test")
    sc = SparkContext(conf=conf)

    ## test if spark is working properly
    nums= sc.parallelize([1,2,3,4])       
    nums.take(1)    

    squared = nums.map(lambda x: x*x).collect()
    f = open("test.txt",'w')
    f.write(str(sc))
    for num in squared:
        print('%i ' % (num))
        f.write(str(num)+'\n')
    f.close()

    # getting all the txt files  
    path = '/scratch/qmn203/txt_arxiv/acc-phys'
    globber = os.path.join(path, '**/*.txt') # search expression for glob.glob
    txtfiles = sorted_files(globber)  # a list of path
    print(len(txtfiles))
    #log.info('Searching "{}"...'.format(globber))
    #log.info('Found: {} pdfs'.format(len(pdffiles)))
    
    rdd = sc.wholeTextFiles(",".join(txtfiles)) # a string of comma separated paths
    print('rdd count: ',rdd.count())
