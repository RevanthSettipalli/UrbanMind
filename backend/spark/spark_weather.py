from pyspark.sql import SparkSession


def run():

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

    spark.stop()


if __name__ == "__main__":
    run()