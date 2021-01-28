import requests
import datetime
import json

import click
from pyspark import SparkConf, SparkContext

from textprocess import path2id, terms_freq
from utilities import read_or_load_rdd


def json_reader(filename):
    """lazy json reader, return a generator"""
    with open(filename) as f:
        for line in f:
            yield json.loads(line)


def rdd2json(RDD, filename):
    """save rdd to new line delimited json (NDJSON)"""
    # load to json
    jsonRDD = RDD.map(lambda x: str(x).replace("'", '"')).map(json.loads).coalesce(1, shuffle=True)

    # map jsons back to string
    json_str = jsonRDD.map(json.dumps)

    # reduce to one big string with one json on each line
    json_longStr = json_str.reduce(lambda x, y: x + "\n" + y)

    # write your string to a file
    with open(filename, "w") as f:
        f.write(json_longStr)


@click.command()
@click.option('--terms_file', default='/Users/qmn203/clones/ds-dialect-map-computing/terms_file.txt',
              help='path to file where jargon terms are store, one per line')
@click.option('--text_dir', default='/Users/qmn203/temp/txtdata_testset',
              help='directory that contain the txt files, including nested subdirectories')
@click.option('--rdd_dir', default='/Users/qmn203/temp/', help='path to store rdd format of all txt')
@click.option('--sample_size', default=1, help='float, between 0-1 , how much to sample from all the data')
def main(text_dir, rdd_dir, sample_size, terms_file):
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
    # text_dir = '/Users/qmn203/temp/emptydir' #/arxiv/pdf/0704'
    # where to store rdd format of all txt:
    # rdd_content_dir = '/Users/qmn203/temp/rdd_txt_arxiv_arxiv/rdd_content_sample_' + str(sample_size)
    rdd_content_dir = rdd_dir + str(sample_size)  #

    rdd_content = read_or_load_rdd(text_dir, sample_size, rdd_content_dir, sc=sc)

    jargons_list = []
    with open(terms_file) as file:
        for line in file.read().splitlines():
            jargons_list.append(line)

    # group by paperID [{'paperID': str, 'jargon_tf': [{'jargon': str, 'tf_norm': float}, {...}, ...]},{...},...]
    rdd_tf = rdd_content.map(lambda x: {"paperID": path2id(x),
                                        "jargon_tf": terms_freq(jargons_list, x, similarity=85, method='norm')})

    # keep only paper which has at least 1 term frequency non zero
    rdd_drop = rdd_tf.filter(lambda x: any([y["tf_norm"] for y in x["jargon_tf"]]))

    # explode the jargon list of each paper into multiple elements, each is a tuple (jargon,[{'paperID':'','tf':''}])
    rdd_flat = rdd_drop.flatMap(
        lambda x: [(y['jargon'], {"paperID": x['paperID'], "tf":y['tf_norm']}) for y in x['jargon_tf']])

    # drop element where term frequency = 0
    rdd_jargon_paper_tf = rdd_flat.filter(lambda x: x[1]['tf'] != 0)

    # group by jargons to create {"jargon": jargon, "paper_tf":[{paper1: tf},{paper2:tf},]}
    rdd_jargonGroup = rdd_jargon_paper_tf.combineByKey(lambda value: [value],  # create combiner
                                                       lambda x, value: x+value,  # combine in the same partition
                                                       lambda x, y: x+y).map(  # combine across partitions
        lambda x: {"jargon": x[0], "paper_tf": x[1]}  # format to dict
    )

    rdd2json(rdd_jargonGroup, "/Users/qmn203/temp/jargonGroup.json")

    # lazy read
    gen = json_reader('/Users/qmn203/temp/jargonGroup.json')
    for row in gen:
        print(row['jargon'], row['paper_tf'][0]['paperID'], row['paper_tf'][0]['tf'])

    # TODO:
    #  modularize & write tests?
    #  run larger data set?
    #  write out json?
    #  take CLI arguments: read list of jargon from textfile
    #  options: parallelization level,


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


if __name__ == "__main__":
    main()

