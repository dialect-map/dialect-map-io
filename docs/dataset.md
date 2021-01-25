# ArXiv dataset


## About
ArXiv provides different and heterogeneous procedures to access their data.

The full list of accessing methods is available within the ArXiv [Help section][arxiv-data-guide].


## Data types
ArXiv data is clearly split into two categories

### Metadata
This type is usually formalize as `XML` or `JSON`, and represents metadata fields
for each paper submissions. These metadata records contain information such as
the paper ID, paper authors, paper categories ...

## Papers
This type represents the `PDF`, `PostScript` or `HTML` paper content files that are
uploaded in each ArXiv paper submission. They contain the texts from which this
NLP metrics computational pipeline must feed from.


## Data operations
The way of accessing and operating each type of data types is different.

On one hand, metadata records can be easily accessed at run-time, as they are light-weight.
On the other hand, paper files are heavier, and it is recommended to have a fully-downloaded
corpus before starting the pipeline.

### Metadata
Records can be retrieved through the ArXiv public APIs, either using:
- The [Open Archives Initiative][arxiv-oai-guide] protocol.
- A [more common API interface][arxiv-api-guide].

### Papers
Files can be retrieved from different cloud buckets, although, the simplest source may be
the Google Cloud Storage bucket that the [Kaggle ArXiv dataset][kaggle-arxiv-dataset]
references to (`gs://arxiv-dataset/arxiv`).

However, this bucket is organized in an **heterogeneous** manner. Depending on the submission
date, papers are stored:

- A) Until **April 2007**, by their category: `gs://arxiv-dataset/arxiv/<category>/<format>/...`
- B) From **April 2007**, by their month: `gs://arxiv-dataset/arxiv/arxiv/<format>/<YYMM>/...`

Where `<format>` can be: `html`, `pdf` or `ps`.


## Data updates
ArXiv data sources updates occur with different periodicity.

As a rule of thumb, the following approximations can be used:
- **Metadata API:** immediate (hourly? daily?).
- **GCS Bucket:** slow (monthly?).


[arxiv-api-guide]: https://arxiv.org/help/api/basics
[arxiv-data-guide]: https://arxiv.org/help/bulk_data
[arxiv-oai-guide]: https://arxiv.org/help/oa/index
[kaggle-arxiv-dataset]: https://www.kaggle.com/Cornell-University/arxiv
