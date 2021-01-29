Set up and run spark on NYU HPC Greene cluster

Prepare directory
```
mkdir /scratch/$USER/spark_py
cd /scratch/$USER/spark_py
```
Get Spark

Go to `https://spark.apache.org/downloads.html` and choose a desired version of spark (pre-builed for Hadoop)
Click to download link - choose mirror - Copy URL, for example `https://mirrors.sonic.net/apache/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz`

download
```
wget <url from above>
```

unzip
```
mkdir sbin
tar -xvf spark-*.tgz -C sbin --strip 1
```

