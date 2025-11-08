# Data Modeling

## Overview
This section covers data modeling best practices in Databricks and Delta Lake.

## Topics to Study

### 1. Database Design
- Databases and schemas
- Managed vs External tables
- Table types (Delta, Parquet, CSV, etc.)
- Naming conventions and organization

### 2. Schema Management
- Defining schemas explicitly vs inference
- Schema evolution strategies
- Column data types
- Nested structures (arrays, structs, maps)

### 3. Tables and Views
- Managed tables vs External tables
- Temporary views vs Global temporary views
- Materialized views considerations
- When to use each type

### 4. Partitioning Strategies
- Benefits and trade-offs of partitioning
- Choosing partition columns
- Over-partitioning pitfalls
- Partition pruning

### 5. Data Organization
- File sizes and number of files
- Bucketing vs partitioning
- Table location and storage
- Data layout optimization

### 6. Constraints and Data Types
- NOT NULL constraints
- CHECK constraints
- Primary and foreign key concepts
- Choosing appropriate data types

## Key Concepts to Master
- When to use managed vs external tables
- Effective partitioning strategies
- Schema evolution without breaking pipelines
- Working with complex and nested data types
- Trade-offs in data organization

## Practice Areas
- Design schemas for different use cases
- Practice partitioning strategies
- Work with nested data structures
- Convert between different table types
- Implement schema evolution

## Common Commands
```sql
-- Create database
CREATE DATABASE IF NOT EXISTS my_db LOCATION 'dbfs:/path/';

-- Create managed table
CREATE TABLE my_db.users (
    id INT,
    name STRING,
    email STRING,
    created_date DATE
) USING DELTA
PARTITIONED BY (created_date);

-- Create external table
CREATE EXTERNAL TABLE my_db.external_data
LOCATION 'dbfs:/external/path/'
USING DELTA;

-- Temporary view
CREATE TEMPORARY VIEW temp_view AS
SELECT * FROM table WHERE condition;

-- Show partitions
SHOW PARTITIONS table_name;
```

## Resources
Add your data modeling examples, schemas, and reference materials here.
