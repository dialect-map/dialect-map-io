import requests
import datetime

from pyspark import SparkConf, SparkContext

from src.textprocess import path2id, terms_freq
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

    # all_txt_dir = '/Users/qmn203/temp/emptydir' #/arxiv/pdf/0704'
    all_txt_dir = '/Users/qmn203/temp/txtdata_testset'  # directory that contain the txt files, could be nested
    sample_size = 1  # float, between 0-1 , how much to sample from all the data

    # where to store rdd format of all txt:
    # rdd_content_dir = '/Users/qmn203/temp/rdd_txt_arxiv_arxiv/rdd_content_sample_' + str(sample_size)
    rdd_content_dir = '/Users/qmn203/temp/rdd' + str(sample_size)  #

    rdd_content = read_or_load_rdd(all_txt_dir, sample_size, rdd_content_dir, sc=sc)

    jargons_list = ['perceptual capability', 'physics', 'conclusion']
    rdd_tf = rdd_content.map(lambda x: {'paperID': path2id(x),
                                        'jargon_tf': terms_freq(jargons_list, x, similarity=85, method='norm')})

    # keep only paper which has at least 1 term frequency non zero
    rdd_tf_drop = rdd_tf.filter(lambda x: any([y['tf_norm'] for y in x['jargon_tf']]))

    # explode the jargon list of each paper into multiple elements, each is a tuple (jargon,[paperID,tf])
    rdd_tf_flat = rdd_tf_drop.flatMap(lambda x: [(y['jargon'], [x['paperID'], y['tf_norm']]) for y in x['jargon_tf']])

    # drop element where term frequency = 0
    rdd_paper_jargon_tf = rdd_tf_flat.filter(lambda x: x[1][1] != 0)

    #group by jargons to create {"jargon": jargon, "paper_tf":[{paper1: tf},{paper2:tf},]}

    # #  --- SQL test code --- #
    # import random
    #
    # for j in jargons_list:
    #     r = requests.post(
    #         url="http://0.0.0.0:8080/jargon",
    #         json={
    #             "jargon_id": str(int(random.random()*1000)),
    #             "jargon_str": j,
    #             "created_at": datetime.datetime.now().isoformat(),
    #             "num_words": 10
    #         }
    #     )

    # insert all jargon to database one by one jargon, paper, metrics
