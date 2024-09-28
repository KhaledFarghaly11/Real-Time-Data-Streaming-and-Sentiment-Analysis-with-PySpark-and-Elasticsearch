import pyspark
import google.generativeai as genai
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when, udf
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from config.config import config
from time import sleep
# customers_review
# def sentiment_analysis(comment) -> str:
#     if comment:
#         openai.api_key = config['openai']['api_key']
#         openai.organization = ''
#         completion = openai.chat.completions.create(
#             model='gpt-3.5-turbo',
#             messages = [
#                 {
#                     "role": "system",
#                     "content": """
#                         You're a machine learning model with a task of classifying comments into POSITIVE, NEGATIVE, NEUTRAL.
#                         You are to respond with one word from the option specified above, do not add anything else.
#                         Here is the comment:
                        
#                         {comment}
#                     """.format(comment=comment)
#                 }
#             ]
#         )
#         return completion.choices[0].message['content']
#     return "Empty"

def sentiment_analysis(comment) -> str:
    if comment:
        genai.configure(api_key=config['gemini']['api_key'])
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
                    """
                        You're a machine learning model with a task of classifying comments into POSITIVE, NEGATIVE, NEUTRAL.
                        You are to respond with one word from the option specified above, do not add anything else.
                        Here is the comment:
                        
                        {comment}
                    """.format(comment=comment)
        )
        print(response)
        print("="*50)
        if response.candidates[0].finish_reason:
            return response.text.strip()
    return "Empty"

def start_streaming(spark):
    topic = 'customers_review'
    while True:
        try:
            stream_df = (spark.readStream.format("socket")
                        .option("host", "0.0.0.0")
                        .option("port", 9999)
                        .load())
            
            schema = StructType([
                StructField("review_id", StringType()),
                StructField("user_id", StringType()),
                StructField("business_id", StringType()),
                StructField("stars", FloatType()),
                StructField("date", StringType()),
                StructField("text", StringType())
            ])
            
            stream_df = stream_df.select(from_json(col('value'), schema).alias("data")).select(("data.*"))

            sentiment_analysis_udf = udf(sentiment_analysis, StringType())

            stream_df = stream_df.withColumn('feedback',
                                             when(col('text').isNotNull(), sentiment_analysis_udf(col('text')))
                                             .otherwise(None)
                                             )

            kafka_df = stream_df.selectExpr("CAST(review_id AS STRING) AS key", "to_json(struct(*)) AS value")

            query = (kafka_df.writeStream
                    .format("kafka")
                    .option("kafka.bootstrap.servers", config['kafka']['bootstrap.servers'])
                    .option("kafka.security.protocol", config['kafka']['security.protocol'])
                    .option('kafka.sasl.mechanism', config['kafka']['sasl.mechanisms'])
                    .option('kafka.sasl.jaas.config',
                            'org.apache.kafka.common.security.plain.PlainLoginModule required username="{username}" '
                            'password="{password}";'.format(
                                username=config['kafka']['sasl.username'],
                                password=config['kafka']['sasl.password']
                            ))
                    .option('checkpointLocation', '/tmp/checkpoint')
                    .option('topic', topic)
                    .start()
                    .awaitTermination()
                    )
        except Exception as e:
                print(f'Exception encountered: {e}. Retrying in 10 seconds')
                sleep(10)

if __name__ == '__main__':
    spark_conn = SparkSession.builder.appName("SocketStreamConsumer").getOrCreate()

    start_streaming(spark_conn)