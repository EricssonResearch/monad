from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("testin").setMaster("spark://130.238.15.246:7077")
sc = SparkContext(conf = conf)

a = sc.parallelize([1,2,3,4,5,6,7,8,9,10])
b = a.collect()

for element in b:
    print element
