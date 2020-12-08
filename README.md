# ds-dialect-map-computing (in development)

Source code for nlp mining of arxiv text files. This is a part of the larger project [ds-dialect-map](https://github.com/ds3-nyu-archive/ds-dialect-map)
Current functionalities:
- convert pdfs to texts
- parse article ID from text
- get term frequency in each article

# How to get arxiv articles and convert them to text for processing
To download all arxiv pdfs: https://arxiv.org/help/bulk_data.  
To convert all pdfs in a directory to text:
First clone this

```
git clone https://github.com/quynhneo/arxiv-public-datasets_for_kaggle
```
then run

```
python pdfs_to_dir_txt_dir.py
```

# Prerequisites for running nlp analysis test
- a folder containing text files of arxiv articles
- spark environtment setup

In `scratch.py`, set the folder to `all_txt_dir`, choose a `sample_size` to sub sample the data, and a path for holding intermediate data at `rdd_content_dir`

To run the test from shell:
```
$spark-submit scratch.py
```

or to run interactively:
```
$pyspark
```

then

```
>> exec(open('scratch.py').read())
```

Currently, given a hard-coded list of `[ term1, term2, ...]`, this will return rdd objects `rdd_count` which is a dictionary `{paper1,[ tf11, tf12 ,...], paper2,[tf21,tf22..}...}` where tfij is term frequency of term j in paper i.

Eventually, the dictionary will be transformed into a different schema and saved into a databased that faccilitate server access. 
