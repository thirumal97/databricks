# Delta Lake Practice Exercise 1: Basic Operations

## Objective
Practice creating Delta tables and performing basic CRUD operations.

## Difficulty Level
Beginner

## Prerequisites
- Databricks workspace access
- Understanding of basic SQL and DataFrames

## Scenario
You are tasked with creating a customer database and performing various operations on it.

## Exercise Steps

### 1. Create a Delta Table
Create a Delta table named `customers` with the following schema:
- `customer_id` (INT) - Primary identifier
- `first_name` (STRING)
- `last_name` (STRING)
- `email` (STRING)
- `registration_date` (DATE)
- `country` (STRING)

### 2. Insert Sample Data
Insert at least 10 sample customer records.

### 3. Update Records
Update the email address for customers with `customer_id` between 1 and 5.

### 4. Delete Records
Delete customers from a specific country.

### 5. Query the Data
- Select all customers
- Count customers by country
- Find customers registered in the last 30 days

### 6. Explore Delta Features
- Check the table history using `DESCRIBE HISTORY`
- Query a previous version of the table using Time Travel
- Optimize the table

## Sample Solution

```python
# 1. Create Delta Table
spark.sql("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT,
        first_name STRING,
        last_name STRING,
        email STRING,
        registration_date DATE,
        country STRING
    ) USING DELTA
""")

# 2. Insert sample data
sample_data = [
    (1, 'John', 'Doe', 'john.doe@email.com', '2024-01-15', 'USA'),
    (2, 'Jane', 'Smith', 'jane.smith@email.com', '2024-01-16', 'UK'),
    (3, 'Bob', 'Johnson', 'bob.j@email.com', '2024-01-17', 'Canada'),
    (4, 'Alice', 'Williams', 'alice.w@email.com', '2024-01-18', 'USA'),
    (5, 'Charlie', 'Brown', 'charlie.b@email.com', '2024-01-19', 'Australia'),
    (6, 'Eva', 'Davis', 'eva.d@email.com', '2024-01-20', 'Germany'),
    (7, 'Frank', 'Miller', 'frank.m@email.com', '2024-01-21', 'France'),
    (8, 'Grace', 'Wilson', 'grace.w@email.com', '2024-01-22', 'USA'),
    (9, 'Henry', 'Moore', 'henry.m@email.com', '2024-01-23', 'UK'),
    (10, 'Ivy', 'Taylor', 'ivy.t@email.com', '2024-01-24', 'Canada')
]

columns = ['customer_id', 'first_name', 'last_name', 'email', 'registration_date', 'country']
df = spark.createDataFrame(sample_data, columns)
df.write.format("delta").mode("append").saveAsTable("customers")

# 3. Update records
spark.sql("""
    UPDATE customers
    SET email = CONCAT('updated_', email)
    WHERE customer_id BETWEEN 1 AND 5
""")

# 4. Delete records
spark.sql("""
    DELETE FROM customers
    WHERE country = 'Australia'
""")

# 5. Query the data
# All customers
display(spark.sql("SELECT * FROM customers"))

# Count by country
display(spark.sql("""
    SELECT country, COUNT(*) as customer_count
    FROM customers
    GROUP BY country
    ORDER BY customer_count DESC
"""))

# Recent registrations
display(spark.sql("""
    SELECT *
    FROM customers
    WHERE registration_date >= CURRENT_DATE - INTERVAL 30 DAYS
"""))

# 6. Delta features
# Check history
display(spark.sql("DESCRIBE HISTORY customers"))

# Time travel - query version 0 (before updates and deletes)
display(spark.sql("SELECT * FROM customers VERSION AS OF 0"))

# Optimize table
spark.sql("OPTIMIZE customers")
```

## Expected Outcomes
1. Delta table created successfully
2. Data inserted and visible in the table
3. Email addresses updated for specified customers
4. Records from Australia deleted
5. Query results show filtered and aggregated data
6. Table history shows all operations
7. Time travel query shows original data
8. Table optimized

## Discussion Questions
1. What happens to deleted data in Delta Lake?
2. How does Delta Lake maintain ACID properties?
3. When would you use OPTIMIZE?
4. What are the benefits of Time Travel?

## Extension Challenges
1. Add a new column to the table using ALTER TABLE
2. Implement a MERGE operation for upserts
3. Create a partitioned version of this table
4. Set up a streaming read from this table

## Notes
- Delta Lake maintains a transaction log
- VACUUM removes old files (use carefully!)
- Time Travel is useful for auditing and recovery
- OPTIMIZE improves query performance
