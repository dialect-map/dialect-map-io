# ds-dialect-map-computing

Source code for mining arxiv text files.  Curernt functionalities:
- convert pdfs to texts
- parse article ID from text
- get term frequency in each article


# prerequisites
- a folder containing text files of arxiv articles
- spark environtment setup

In `scratch.py`, set the folder to `all_txt_dir`, choose a `sample_size` to sub sample the data, and a path for holding intermediate data at `rdd_content_dir`

To run the test:
`spark-submit scratch.py`

# how to get arxiv articles and convert them to text for processing
To download all arxiv pdfs: https://arxiv.org/help/bulk_data.  
To convert all pdfs in a directory to text:
clone https://github.com/quynhneo/arxiv-public-datasets_for_kaggle
`python pdfs_to_dir_txt_dir.py`
