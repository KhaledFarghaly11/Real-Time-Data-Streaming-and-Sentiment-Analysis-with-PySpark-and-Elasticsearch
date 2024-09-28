# Real-Time Data Streaming and Sentiment Analysis with PySpark and Elasticsearch

## Project Overview

This project demonstrates a real-time data streaming pipeline that reads customer reviews from a JSON file, processes the data using PySpark, performs sentiment analysis with gemini, and indexes the results in Elasticsearch for efficient search and analysis.

## Project Objectives

- **Socket-Based Data Transmission**: Implement a system to read JSON records from a file, process them into pandas DataFrames, and send them in chunks over a network connection.
- **PySpark Streaming Application**: Develop a PySpark streaming application to consume data from a socket connection, parse it into a structured format, and output the parsed data to the console.
- **Sentiment Analysis**: Enhance the streaming application to classify comments into POSITIVE, NEGATIVE, or NEUTRAL categories using a generative AI model.
- **Elasticsearch Integration**: Utilize Elasticsearch to index and search customer reviews efficiently, enabling full-text search, phrase matching, and aggregation of feedback data.


## Setup Instructions

### Prerequisites

- Docker
- Docker Compose
- Python 3.11
- Apache Spark
- Elasticsearch
- Kafka

### Step-by-Step Guide

1. **Clone the Repository**

   ```bash
   git clone https://github.com/KhaledFarghaly11/Real-Time-Data-Streaming-and-Sentiment-Analysis-with-PySpark-and-Elasticsearch
   ```
Sure! Here’s the continuation in Markdown:

### Build and Run Docker Containers

1. **Build and Run Docker Images**

   Navigate to the project directory and build the Docker images using the following command:

   ```bash
   docker-compose up -d --build
   ```

   This command will start all the services defined in the `docker-compose.yml` file, including PySpark

### Configure API Keys and Service Credentials

Update the `config.py` file with your API keys and service credentials. This file should include configurations for OpenAI, Gemini, Kafka, and Elasticsearch.

### Start the Socket Data Transmission

Run the `streaming_socket.py` script to start sending JSON data over the socket connection:

```bash
python streaming_socket.py
```

### Start the PySpark Streaming Application

Run the `spark_streaming.py` script to start the PySpark streaming application:

```bash
python spark_streaming.py
```

### Elasticsearch Queries

You can use the following Elasticsearch queries to search and analyze the indexed customer reviews:

- **Match All Reviews**

  ```json
  GET customers_review/_search
  {
    "query": {
      "match_all": {}
    }
  }
  ```

- **Match Phrase in Reviews**

  ```json
  GET customers_review/_search
  {
    "query": {
      "match_phrase": {
        "text": "amazing"
      }
    }
  }
  ```

- **Aggregate Feedback Data**

  ```json
  GET customers_review/_search
  {
    "size": 0,
    "aggs": {
      "group_by_feedback": {
        "terms": {
          "field": "feedback.keyword"
        },
        "aggs": {
          "total_count": {
            "value_count": {
              "field": "feedback.keyword"
            }
          }
        }
      }
    }
  }
  ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.


## Acknowledgements

- [Apache Spark](https://spark.apache.org/)
- [Elasticsearch](https://www.elastic.co/cloud)
- [Kafka](https://www.confluent.io/confluent-cloud/tryfree/)
- [Docker](https://www.docker.com/)

Feel free to customize this further to fit your project specifics! Let me know if you need any more details or adjustments.
