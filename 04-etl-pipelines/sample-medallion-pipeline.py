# Sample ETL Pipeline: Bronze to Silver Transformation

## Overview
This notebook demonstrates a simple medallion architecture ETL pipeline.

## Architecture
Bronze (Raw) → Silver (Cleaned) → Gold (Aggregated)

## Use Case
Processing e-commerce order data through multiple layers.

## Bronze Layer - Raw Data Ingestion

```python
# Read raw CSV data
raw_orders_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("/mnt/raw/orders/*.csv")

# Write to Bronze Delta table with minimal transformation
raw_orders_df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("/mnt/bronze/orders")

# Create Bronze table
spark.sql("""
    CREATE TABLE IF NOT EXISTS bronze.orders
    USING DELTA
    LOCATION '/mnt/bronze/orders'
""")
```

## Silver Layer - Data Cleaning and Standardization

```python
from pyspark.sql.functions import *

# Read from Bronze
bronze_df = spark.read.format("delta").load("/mnt/bronze/orders")

# Clean and transform data
silver_df = bronze_df \
    .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd")) \
    .withColumn("order_amount", col("order_amount").cast("decimal(10,2)")) \
    .withColumn("customer_email", lower(trim(col("customer_email")))) \
    .withColumn("processed_timestamp", current_timestamp()) \
    .filter(col("order_amount") > 0) \
    .dropDuplicates(["order_id"]) \
    .na.drop(subset=["order_id", "customer_id"])

# Write to Silver Delta table
silver_df.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("order_date") \
    .save("/mnt/silver/orders")

# Create Silver table
spark.sql("""
    CREATE TABLE IF NOT EXISTS silver.orders
    USING DELTA
    LOCATION '/mnt/silver/orders'
""")
```

## Gold Layer - Business Aggregations

```python
# Read from Silver
silver_df = spark.read.format("delta").load("/mnt/silver/orders")

# Create daily aggregations
daily_summary_df = silver_df \
    .groupBy("order_date") \
    .agg(
        count("order_id").alias("total_orders"),
        sum("order_amount").alias("total_revenue"),
        avg("order_amount").alias("avg_order_value"),
        countDistinct("customer_id").alias("unique_customers")
    ) \
    .orderBy("order_date")

# Write to Gold Delta table
daily_summary_df.write.format("delta") \
    .mode("overwrite") \
    .save("/mnt/gold/daily_order_summary")

# Create Gold table
spark.sql("""
    CREATE TABLE IF NOT EXISTS gold.daily_order_summary
    USING DELTA
    LOCATION '/mnt/gold/daily_order_summary'
""")
```

## Incremental Processing Pattern

```python
from delta.tables import DeltaTable

# Get the maximum processed timestamp from Silver
max_timestamp = spark.sql("""
    SELECT MAX(processed_timestamp) as max_ts 
    FROM silver.orders
""").collect()[0]["max_ts"]

# Read only new records from Bronze
new_records_df = spark.read.format("delta") \
    .load("/mnt/bronze/orders") \
    .filter(col("ingestion_timestamp") > max_timestamp)

# Transform and merge into Silver
if new_records_df.count() > 0:
    # Transform
    transformed_df = new_records_df \
        .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd")) \
        .withColumn("order_amount", col("order_amount").cast("decimal(10,2)")) \
        .withColumn("customer_email", lower(trim(col("customer_email")))) \
        .withColumn("processed_timestamp", current_timestamp())
    
    # Merge into Silver table
    silver_table = DeltaTable.forPath(spark, "/mnt/silver/orders")
    
    silver_table.alias("target").merge(
        transformed_df.alias("source"),
        "target.order_id = source.order_id"
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()
    
    print(f"Processed {new_records_df.count()} new records")
else:
    print("No new records to process")
```

## Data Quality Checks

```python
# Check for null values in critical columns
quality_check = spark.sql("""
    SELECT 
        COUNT(*) as total_records,
        COUNT(CASE WHEN order_id IS NULL THEN 1 END) as null_order_ids,
        COUNT(CASE WHEN customer_id IS NULL THEN 1 END) as null_customer_ids,
        COUNT(CASE WHEN order_amount <= 0 THEN 1 END) as invalid_amounts
    FROM silver.orders
""")

display(quality_check)

# Alert if quality issues found
quality_result = quality_check.collect()[0]
if quality_result["null_order_ids"] > 0 or quality_result["invalid_amounts"] > 0:
    print("⚠️ Data quality issues detected!")
else:
    print("✅ Data quality checks passed")
```

## Optimization

```python
# Optimize Silver table
spark.sql("OPTIMIZE silver.orders ZORDER BY (customer_id)")

# Optimize Gold table
spark.sql("OPTIMIZE gold.daily_order_summary")

# Vacuum old files (older than 7 days)
spark.sql("VACUUM silver.orders RETAIN 168 HOURS")
```

## Monitoring and Logging

```python
# Log pipeline execution
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_pipeline_metrics(layer, record_count, execution_time):
    logger.info(f"""
        Pipeline Execution Metrics:
        Layer: {layer}
        Records Processed: {record_count}
        Execution Time: {execution_time} seconds
        Timestamp: {datetime.now()}
    """)

# Example usage
start_time = datetime.now()
record_count = silver_df.count()
execution_time = (datetime.now() - start_time).total_seconds()
log_pipeline_metrics("Silver", record_count, execution_time)
```

## Best Practices Demonstrated

1. **Layered Architecture**: Clear separation between Bronze, Silver, and Gold
2. **Incremental Processing**: Only process new/changed data
3. **Data Quality**: Validate and clean data at each stage
4. **Partitioning**: Partition by date for query optimization
5. **Idempotency**: Use MERGE operations for upserts
6. **Optimization**: Regular OPTIMIZE and VACUUM operations
7. **Monitoring**: Log metrics and execution details

## Next Steps

- Add error handling and retry logic
- Implement CDC patterns for real-time processing
- Add more sophisticated data quality checks
- Set up alerting for pipeline failures
- Create streaming versions of these pipelines
