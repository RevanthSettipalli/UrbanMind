from pyspark.sql import SparkSession
from pyspark.sql.functions import avg


spark = (
    SparkSession
    .builder
    .appName("UrbanMind Aggregation")
    .getOrCreate()
)

INPUT = "data/processed/spark_weather"

df = spark.read.parquet(INPUT)

print("\nLoaded Dataset")
df.show()

summary = (
    df.select(
        avg("temperature_celsius")
        .alias("avg_temperature")
    )
)

print("\nWeather Summary")

summary.show()

OUTPUT = "data/processed/weather_summary"

summary.write.mode(
    "overwrite"
).csv(
    OUTPUT,
    header=True
)

print("\nAggregation completed")

spark.stop()