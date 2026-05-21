from pyspark.sql import SparkSession

spark = (
    SparkSession
    .builder
    .appName("UrbanMind Weather Processing")
    .getOrCreate()
)

INPUT = "data/processed/weather_clean.csv"

df = spark.read.csv(
    INPUT,
    header=True,
    inferSchema=True
)

print("\nRaw Dataset")
df.show()

processed = (
    df
    .withColumnRenamed(
        "temperature",
        "temperature_celsius"
    )
)

OUTPUT = "data/processed/spark_weather"

processed.write.mode(
    "overwrite"
).parquet(
    OUTPUT
)

print("\nSpark processing completed")

spark.stop()