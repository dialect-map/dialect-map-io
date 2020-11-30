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

def get_all_paths(all_txt_dir: str, filename = 'all_paths_str.dat') -> str:
    """ input: 
            all_txt_dir: directory contains all articles in txt format
            filename: where the output is stored
        output:
            all_paths_str: a string of comma separated paths of all the files
    """
    if not os.path.exists(os.path.join(all_txt_dir,filename) ):
        globber = os.path.join(all_txt_dir, '**/*.txt') # search expression for glob.glob
        txtfiles = sorted_files(globber)  # a list of path
        all_paths_str = ",".join(txtfiles) 
        print('number of text files: ',len(txtfiles))
        with open(os.path.join(all_txt_dir,filename),'w') as file:
            file.write(all_paths_str)
    else:
        print('comma separated string of paths in row format exist ')
        with open(os.path.join(all_txt_dir,filename),'r') as f:
            all_paths_str = f.readline()   
        print(type(all_paths_str),'number of text files: ', all_paths_str.count(',')+1)
    #log.info('Searching "{}"...'.format(globber))
    return all_paths_str     

def get_all_paths2(all_txt_dir: str, filename = 'all_paths.csv') -> str:
    """ input: 
            all_txt_dir: directory contains all articles in txt format
            filename: where the output is stored, each row is a path to a text file
        output:
            path to filename 
    """
    if not os.path.exists(os.path.join(all_txt_dir,filename) ):
        globber = os.path.join(all_txt_dir, '**/*.txt') # search expression for glob.glob
        txtfiles = sorted_files(globber)  # a list of path
        with open(os.path.join(all_txt_dir,filename),'w') as file:
            writer = csv.writer(file)
            for path in txtfiles:
                writer.writerow([path])
    else:
        print('csv of all paths in column format exists ')
        
    return os.path.join(all_txt_dir,filename)    
    
    
    
def toCSVLine(data):
    return ','.join(str(d) for d in data)


def dir2rdd(all_txt_dir:str, part_num = 1000):

     #  getting all the txt files, put in a string of comma separated string of paths 
    all_paths_str = get_all_paths(all_txt_dir) 
    
    # load all text files into spark rdd. 1000 partition, about MB each. took 1 hour for 20 cores 
    rdd = sc.wholeTextFiles(all_paths_str, part_num) # each element [('file: path',  content<str> ), ( ) ,... ]
    return rdd

if __name__ == "__main__":
    # setting up spark
    #conf = SparkConf().setMaster("local[*]").setAppName("scratch")
    #sc = SparkContext.getOrCreate(conf=conf)
    #sc =SparkContext(master = os.getenv('SPARK_URL'))
    sc.setLogLevel("ERROR")

    #test spark
    nums = range(0,100)
    print(nums)
    rddtest = sc.parallelize(nums,10)
    print("Default parallelism: {}".format(sc.defaultParallelism))
    print("Number of partitions: {}".format(rddtest.getNumPartitions()))
    print("Partitioner: {}".format(rddtest.partitioner))
    print("Partitions structure: {}".format(rddtest.glom().collect())) 
    
    all_txt_dir  = '/scratch/qmn203/txt_arxiv/arxiv' #/arxiv/pdf/0704'
    #all_txt_dir = '/home/qmn203/txtdata_testset' # directory that contain the txt files, could be nested 
    rdd = dir2rdd(all_txt_dir)
    rdd_path=rdd.map(lambda x: x[0])
    rdd_content=rdd.map(lambda x: (x[1],)) 
    rdd_content.saveAsTextFile('/scratch/qmn203/rdd_txt_arxiv_arxiv/rdd_content3')
    rdd_path.saveAsTextFile('/scratch/qmn203/rdd_txt_arxiv_arxiv/rdd_path3') 
    
    #load rdd
    #rdd_txt = sc.textFile('/scratch/qmn203/rdd_txt_arxiv_arxiv/rdd_content')
    #rdd_path = sc.textFile('/scratch/qmn203/rdd_txt_arxiv_arxiv/rdd_path')    
    #rdd_filename = rdd_path.map(lambda x: x.split('/')[-1])
    #rdd_id=rdd_filename.map(lambda x: x[:x.rfind('.txt')])

    print('rdd count: ', rdd.count(), 'partition size: ' )
    print('first file', rdd.take(1)[0][0])
    # print('first content', rdd.take(1)[0][1])
    test_word = 'momentum'
    #rdd.take(10).foreach(println) 
    
