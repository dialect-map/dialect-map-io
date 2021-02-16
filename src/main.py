import os
import requests
import datetime
import json
import timeit

import click
from pyspark import SparkConf, SparkContext

from nlp.textprocess import path2id, terms_freq
from utilities import read_or_load_rdd
from nlp.metrics import FuzzyMetricsEngine  # in job repos, this will be replace by importing the package


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
@click.option('--terms_file', default="/Users/qmn203/clones/dialect-map-data/data/jargons.json",
              help='path to file where jargon terms are store, one per line')
@click.option('--text_dir', default='/Users/qmn203/temp/txtdata_testset',
              help='directory that contains the txt files, including nested subdirectories')
@click.option('--rdd_dir', default='/Users/qmn203/temp/', help='directory to store rdd format of all txt')
@click.option('--sample_size', default=1.0,
              help='between 0.0-1.0, how much to randomly sample from all the data')
@click.option('--json_dir', default='/Users/qmn203/temp',
              help='directory to store json file of computed term frequency')
def main(text_dir, rdd_dir, sample_size, terms_file, json_dir):
    start = timeit.default_timer()
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
    rdd_content_dir = os.path.join(rdd_dir, "rdd_content_sample_" + str(sample_size))  #

    rdd_content = read_or_load_rdd(text_dir, sample_size, rdd_content_dir, sc=sc)

    # ---- get the list of jargon terms from file ---- #
    jargons_list = []
    with open(terms_file) as file:
        jsonlist = json.load(file)
        for group in jsonlist:
            for term in group['terms']:
                jargons_list.append(term['name'])

    # get term frequency, group by paperID
    # [{'paperID': str, 'jargon_tf': [{'jargon': str, 'tf_norm': float}, {...}, ...]},{...},...]
    # rdd_tf = rdd_content.map(lambda x: {"paperID": path2id(x),
    #                                     "jargon_tf": terms_freq(jargons_list, x, similarity=85, method='norm')})

    fuzzy_tf = FuzzyMetricsEngine()
    rdd_tf = rdd_content.map(lambda x: {"paperID": path2id(x),
                                        "jargon_tf": fuzzy_tf.compute_rel_freq(jargons_list, x)})

    # keep only paper which has at least 1 non zero term frequency
    rdd_drop = rdd_tf.filter(lambda x: any([y["tf"] for y in x["jargon_tf"]]))

    # explode the jargon list of each paper into multiple elements,
    # reorder each is a 2-tuple (jargon,{'paperID':'','tf':''})
    rdd_flat = rdd_drop.flatMap(
        lambda x: [(y['jargon'], {"paperID": x['paperID'], "tf": y['tf']}) for y in x['jargon_tf']])

    # drop tuple element where term frequency = 0
    rdd_jargon_paper_tf = rdd_flat.filter(lambda x: x[1]['tf'] != 0)

    # group by jargons to create {"jargon": jargon, "paper_tf":[{paper1: tf},{paper2:tf},]}
    rdd_jargon_group = \
        rdd_jargon_paper_tf.combineByKey(
            lambda value: [value],  # create combiner: first value (a dict) -> list[dict]
            lambda list0, other_value: list0 + [other_value],
            # combine the combiner with other values of the same key: concat 2 list[dict] (same partition)
            lambda list_i, list_j: list_i + list_j).map(  # combine combiners (across partitions)
            lambda x: {"jargon": x[0], "paper_tf": x[1]}  # format to dict
        )

    # save to json
    json_file = os.path.join(json_dir, "jargonGroup.json")
    rdd2json(rdd_jargon_group, json_file)

    # lazy read test
    gen = json_reader(json_file)
    for row in gen:
        print(row['jargon'], row['paper_tf'][0]['paperID'], row['paper_tf'][0]['tf'])

    stop = timeit.default_timer()
    runtime = (stop - start) / 3600
    print(f'run time is {runtime} hour')

    # TODO:
    # share /scratch with setfacl
    # copy pdfs over /scarch
    # include both norm and raw TF?
    # supply options with spark submit
    # in parallel: get as much text files as possible?
    # fuzziness must be based on the length of the term
    # missing terms (97->88)?
    # options: parallelization level?
    # discuss output format
    # what tests to run?
    # run larger data set?
    # configure spark on greene : scale up the nodes?

    # improve docs instruction to run spark: why two ways of running spark

    # progress information

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
