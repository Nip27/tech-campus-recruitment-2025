import sys

from pyspark.sql import SparkSession

from pyspark.sql.functions import regexp_extract, col

 

def filter_logs_by_date(log_file_path, date):

    # Create a Spark session

    spark = SparkSession.builder.appName("LogFileFilter").getOrCreate()

 

    # Read the log file into a DataFrame

    log_df = spark.read.text(log_file_path)

 

    # Define a regex pattern to extract timestamp, log level, and message

    log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.*)'

 

    # Extract the components into separate columns

    parsed_log_df = log_df.select(

        regexp_extract('value', log_pattern, 1).alias('timestamp'),

        regexp_extract('value', log_pattern, 2).alias('log_level'),

        regexp_extract('value', log_pattern, 3).alias('message')

    )

 

    # Filter logs for the specified date

    filtered_logs = parsed_log_df.filter(col('timestamp').startswith(date))

 

    # Write the filtered logs to a new file

    output_path = f"output/output_{date}.txt"

    filtered_logs.write.mode("overwrite").text(output_path)

 

    print(f"Filtered logs for {date} saved to {output_path}")

 

if __name__ == "__main__":

    # Check if the date argument is provided

    if len(sys.argv) != 3:

        print("Usage: spark-submit log_filter.py <log_file_path> <YYYY-MM-DD>")

        sys.exit(1)

 

    log_file_path = sys.argv[1]

    date = sys.argv[2]

 

    # Call the function to filter logs by date

    filter_logs_by_date(log_file_path, date)
