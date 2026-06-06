from pyspark.sql import SparkSession


spark = (
    SparkSession
    .builder
    .appName(
        "UrbanMind"
    )
    .getOrCreate()
)


print(
    "Spark Running"
)