#import findspark
#findspark.init('/usr/local/spark')
import pyspark
from pyspark import RDD
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

fruitsdict = {}

def printy(a, b):
  listy = b.collect()
  # print(listy)
  for l in listy:
    if l[0] in fruitsdict:
      fruitsdict[l[0]] += l[1]
    else:
      fruitsdict[l[0]] = l[1]
    
    print('Fruit is %s and total sold is %s' % (l[0], l[1]))
    # for key in fruitsdict:
      # print('Fruit is %s and total sold is %s' % (key, fruitsdict[key]))

def another(b, a):
    listy = a.collect()
    for l in listy:
      print(a)

def displaydata(entry):
  for line in entry.collect():
    for entries in line:
      if entries[0] == 'username':
        print('username is %s' % entries[1])
      if entries[0] == 'domain':
        print('domain is %s' % entries[1])

    # entries = line.map(lambda tupler: (tupler[0], tupler[1]))
  # print(entry.collect())

#Spark context details
sc = SparkContext(appName="PythonSparkStreamingKafka")
ssc = StreamingContext(sc,65)
#Creating Kafka direct stream
dks = KafkaUtils.createDirectStream(ssc, ["unconfirmed-transactions"], {"metadata.broker.list":"178.162.213.34:9092"})
# counts = dks.pprint()
counts = dks.map(lambda x: json.loads(x[1])).map(lambda dict: dict.items()).foreachRDD(displaydata)
# counts = dks.map(lambda x: json.loads(x[1])).map(lambda dict: dict.items()).map(lambda tupler: (tupler[0], tupler[1])).pprint()
# counts = dks.map(lambda x: json.loads(x[1])).map(lambda dict: dict.items()).map(lambda tupler: (tupler[1][1], tupler[0][1])).reduceByKey(lambda a, b: a+b).foreachRDD(printy)

# counts = dks.map(lambda x: json.loads(x[1])).map(lambda dict: dict.items()).map(lambda tupler: (tupler[1][1], tupler[2][1])).reduceByKey(lambda a, b: a+b).foreachRDD(printy)
# counts = dks.map(lambda x: json.loads(x[1])).map(lambda dict: dict.items()).map(lambda tupler: (tupler[1][1], tupler[2][1])).foreachRDD(another)
#Starting Spark context
ssc.start()
ssc.awaitTermination()

