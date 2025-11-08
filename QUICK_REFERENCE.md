# Databricks Data Engineer Associate - Quick Reference Guide

## Common PySpark DataFrame Operations

### Creating DataFrames
```python
# From list
df = spark.createDataFrame(data, schema)

# From file
df = spark.read.format("csv").option("header", "true").load("path")
df = spark.read.json("path")
df = spark.read.parquet("path")

# From Delta table
df = spark.read.format("delta").load("path")
df = spark.table("table_name")
```

### Basic Transformations
```python
# Select columns
df.select("col1", "col2")
df.select(col("col1"), col("col2").alias("new_name"))

# Filter
df.filter(col("age") > 18)
df.where("age > 18")

# Add column
df.withColumn("new_col", col("old_col") * 2)

# Rename column
df.withColumnRenamed("old_name", "new_name")

# Drop column
df.drop("col_name")

# Distinct
df.distinct()
df.dropDuplicates(["col1", "col2"])
```

### Aggregations
```python
# Group by
df.groupBy("category").count()
df.groupBy("category").agg(sum("amount"), avg("price"))

# Multiple aggregations
from pyspark.sql.functions import sum, avg, max, min, count
df.groupBy("category").agg(
    sum("amount").alias("total_amount"),
    avg("price").alias("avg_price"),
    count("*").alias("count")
)
```

### Joins
```python
# Inner join (default)
df1.join(df2, "key")
df1.join(df2, df1.key == df2.key)

# Left join
df1.join(df2, "key", "left")

# Other join types: "right", "outer", "left_semi", "left_anti"
```

### Writing Data
```python
# Write to format
df.write.format("parquet").mode("overwrite").save("path")
df.write.mode("append").parquet("path")

# Write to Delta
df.write.format("delta").mode("overwrite").save("path")
df.write.saveAsTable("table_name")

# Partitioned write
df.write.partitionBy("date").parquet("path")
```

## Delta Lake Commands

### Create Table
```sql
CREATE TABLE table_name (
    id INT,
    name STRING,
    date DATE
) USING DELTA
PARTITIONED BY (date)
LOCATION 'path';
```

### Insert/Update/Delete
```sql
-- Insert
INSERT INTO table_name VALUES (1, 'Alice', '2024-01-01');

-- Update
UPDATE table_name SET name = 'Bob' WHERE id = 1;

-- Delete
DELETE FROM table_name WHERE id = 1;
```

### Merge (Upsert)
```python
from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "path")
deltaTable.alias("target").merge(
    source.alias("source"),
    "target.id = source.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

```sql
MERGE INTO target
USING source
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

### Optimization
```sql
-- Optimize
OPTIMIZE table_name;

-- Z-Order
OPTIMIZE table_name ZORDER BY (column);

-- Vacuum (remove old files)
VACUUM table_name RETAIN 168 HOURS;
```

### Time Travel
```sql
-- Query by version
SELECT * FROM table_name VERSION AS OF 5;

-- Query by timestamp
SELECT * FROM table_name TIMESTAMP AS OF '2024-01-01';

-- Describe history
DESCRIBE HISTORY table_name;

-- Restore to version
RESTORE TABLE table_name TO VERSION AS OF 5;
```

## Structured Streaming

### Read Stream
```python
# Read from Delta
streamDF = spark.readStream.format("delta").load("path")

# Read from Kafka
streamDF = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "host:port") \
    .option("subscribe", "topic") \
    .load()
```

### Write Stream
```python
# Write to Delta
query = streamDF.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "checkpoint_path") \
    .start("output_path")

# Output modes: "append", "complete", "update"
```

### Triggers
```python
# Process once
.trigger(once=True)

# Process available data
.trigger(availableNow=True)

# Continuous processing
.trigger(processingTime="10 seconds")
```

## Performance Optimization

### Caching
```python
# Cache
df.cache()
df.persist()

# Unpersist
df.unpersist()
```

### Broadcast Join
```python
from pyspark.sql.functions import broadcast
df1.join(broadcast(df2), "key")
```

### Repartition/Coalesce
```python
# Increase partitions
df.repartition(100)
df.repartition(100, "partition_col")

# Decrease partitions
df.coalesce(10)
```

### Explain Plan
```python
df.explain()
df.explain("extended")
df.explain("formatted")
```

## Common SQL Commands

### Database Operations
```sql
-- Create database
CREATE DATABASE IF NOT EXISTS db_name LOCATION 'path';

-- Use database
USE db_name;

-- Show databases
SHOW DATABASES;

-- Drop database
DROP DATABASE IF EXISTS db_name CASCADE;
```

### Table Operations
```sql
-- Show tables
SHOW TABLES IN db_name;

-- Describe table
DESCRIBE table_name;
DESCRIBE EXTENDED table_name;

-- Show table properties
SHOW TBLPROPERTIES table_name;

-- Drop table
DROP TABLE IF EXISTS table_name;
```

### Views
```sql
-- Temporary view
CREATE TEMPORARY VIEW view_name AS SELECT * FROM table;

-- Global temporary view
CREATE GLOBAL TEMPORARY VIEW view_name AS SELECT * FROM table;

-- Drop view
DROP VIEW IF EXISTS view_name;
```

## Useful Functions

### Date/Time Functions
```python
from pyspark.sql.functions import *

# Current date/time
current_date(), current_timestamp()

# Date operations
date_add(col("date"), 7)
date_sub(col("date"), 7)
datediff(col("end_date"), col("start_date"))

# Extract parts
year(col("date")), month(col("date")), dayofmonth(col("date"))

# Format
date_format(col("timestamp"), "yyyy-MM-dd")
```

### String Functions
```python
# String operations
concat(col("first"), lit(" "), col("last"))
lower(col("name")), upper(col("name"))
trim(col("name")), ltrim(col("name")), rtrim(col("name"))
substring(col("name"), 1, 3)
regexp_replace(col("text"), "pattern", "replacement")
```

### Window Functions
```python
from pyspark.sql.window import Window

windowSpec = Window.partitionBy("category").orderBy("date")

df.withColumn("row_number", row_number().over(windowSpec))
df.withColumn("rank", rank().over(windowSpec))
df.withColumn("running_total", sum("amount").over(windowSpec))
```

## Important Configurations

### Spark Configuration
```python
# Set config
spark.conf.set("spark.sql.shuffle.partitions", "200")
spark.conf.set("spark.sql.adaptive.enabled", "true")

# Get config
spark.conf.get("config.name")
```

### Common Configs
- `spark.sql.shuffle.partitions` - Number of partitions for shuffles (default: 200)
- `spark.sql.adaptive.enabled` - Enable Adaptive Query Execution
- `spark.sql.adaptive.coalescePartitions.enabled` - Coalesce partitions
- `spark.databricks.delta.optimizeWrite.enabled` - Optimize writes
- `spark.databricks.delta.autoCompact.enabled` - Auto compact small files

## Exam Tips

### Time Management
- 90 minutes for 45 questions (~2 min per question)
- Flag difficult questions and return later
- Don't spend too much time on any single question

### Common Question Types
1. Which command/approach should be used?
2. What will this code output?
3. Best practice for scenario X?
4. How to optimize query Y?
5. What is the purpose of feature Z?

### Key Areas to Master
- Delta Lake operations (MERGE, OPTIMIZE, Time Travel)
- DataFrame transformations and actions
- When to use different join types
- Incremental processing patterns
- Performance optimization techniques
- Understanding execution plans

### Remember
- Filter and select early in the query
- Use Delta Lake for production tables
- Partition large tables wisely (but avoid over-partitioning)
- Use broadcast joins for small tables
- Cache strategically, unpersist when done
- Optimize Delta tables regularly
