

from pyspark import SparkConf, SparkContext

import src.textprocess
from src.utilities import read_or_load_rdd


if __name__ == "__main__":
    #  ---- setting up spark, turn off if run interactively ---- #
    conf = SparkConf().setMaster("local[*]").setAppName("scratch")
    sc = SparkContext.getOrCreate(conf=conf)
    # sc =SparkContext(master = os.getenv('SPARK_URL'))
    sc.setLogLevel("ERROR")

    # ----  test spark  ---- #
    nums = range(0, 100)
    print(nums)
    rddtest = sc.parallelize(nums, 10)
    print("Default parallelism: {}".format(sc.defaultParallelism))
    print("Number of partitions: {}".format(rddtest.getNumPartitions()))
    print("Partitioner: {}".format(rddtest.partitioner))
    print("Partitions structure: {}".format(rddtest.glom().collect()))

    # ---- set up directories ---- #
    all_txt_dir = '/Users/qmn203/temp/txtdata_testset' #/arxiv/pdf/0704'
    # all_txt_dir = '/home/qmn203/txtdata_testset' # directory that contain the txt files, could be nested
    sample_size = 1  # float, between 0-1 , how much to sample from all he data
    rdd_content_dir = '/Users/qmn203/temp/rdd_txt_arxiv_arxiv/rdd_content_sample_' + str(sample_size)
    # where to store rdd format of all txt

    rdd_content = read_or_load_rdd(all_txt_dir, sample_size, rdd_content_dir, sc=sc)

    jargons_list = ['arxiv', 'physics', 'conclusion']
    rdd_count = rdd_content.map(lambda x: (src.textprocess.path2id(x),  src.textprocess.terms_freq(jargons_list, x, 'norm')))

    #  run SQL test code here

