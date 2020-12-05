# ds-dialect-map-computing

Source code for mining arxiv text files.  
# prerequisite
- a folder containing text files of arxiv articles
- spark environtment setup

In `scratch.py`, set the folder to `all_txt_dir`, choose a `sample_size` to sub sample the data, and a path for holding intermediate data at `rdd_content_dir`

To run the test:
`spark-submit scratch.py`

To download all arxiv pdfs: https://arxiv.org/help/bulk_data.  
To convert all pdfs in a directory to text: https://github.com/quynhneo/arxiv-public-datasets/blob/master/arxiv_public_data/fulltext.py#L281. 
