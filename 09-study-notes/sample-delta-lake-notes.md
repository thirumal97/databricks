# My Delta Lake Study Notes

## Date: [Add date]

## Key Concepts Learned Today

### Delta Lake Fundamentals
- Delta Lake is an open-source storage layer that brings ACID transactions to data lakes
- Built on top of Parquet files with a transaction log
- Transaction log (\_delta_log) maintains metadata and tracks all changes

### ACID Properties
- **Atomicity**: All or nothing - transactions either complete fully or not at all
- **Consistency**: Data remains in a valid state
- **Isolation**: Concurrent operations don't interfere with each other
- **Durability**: Once committed, changes are permanent

### Important Commands I Practiced

```sql
-- Create Delta table
CREATE TABLE users USING DELTA AS SELECT * FROM parquet.`/path/`

-- Optimize (compacts small files)
OPTIMIZE table_name

-- Z-ORDER (co-locates related information)
OPTIMIZE table_name ZORDER BY (column1, column2)

-- Time Travel
SELECT * FROM table_name VERSION AS OF 5
SELECT * FROM table_name TIMESTAMP AS OF '2024-01-01'

-- Vacuum (removes old files)
VACUUM table_name RETAIN 168 HOURS  -- 7 days
```

### MERGE Operations (Upserts)

```python
from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "path/to/table")

deltaTable.alias("target").merge(
    source_df.alias("source"),
    "target.id = source.id"  # merge condition
).whenMatchedUpdate(set = {
    "name": "source.name",
    "updated_at": "current_timestamp()"
}).whenNotMatchedInsert(values = {
    "id": "source.id",
    "name": "source.name",
    "created_at": "current_timestamp()"
}).execute()
```

## Challenges I Faced

1. **Understanding when to optimize**
   - Solution: Optimize when you have many small files or after many updates
   - Use DESCRIBE DETAIL to check number of files

2. **Choosing Z-ORDER columns**
   - Solution: Choose columns commonly used in WHERE clauses
   - Limit to 3-4 columns for best performance

## Practice Questions I Got Wrong

**Q: What happens to deleted data in Delta Lake?**
- ❌ My answer: It's immediately removed
- ✅ Correct answer: It's marked as deleted in the transaction log but files remain until VACUUM

**Q: Can you query deleted versions after VACUUM?**
- ❌ My answer: Yes, using Time Travel
- ✅ Correct answer: No, VACUUM permanently removes old files

## Important Points to Remember for Exam

- [ ] Default retention period for Time Travel is 30 days
- [ ] VACUUM default retention is 7 days (168 hours)
- [ ] Can't time travel past VACUUM retention period
- [ ] OPTIMIZE doesn't change data, just file layout
- [ ] Z-ORDER is particularly useful for high cardinality columns
- [ ] MERGE operations are atomic and support complex logic
- [ ] Schema evolution is supported with .option("mergeSchema", "true")

## Code Snippets to Remember

```python
# Check table history
display(spark.sql("DESCRIBE HISTORY table_name"))

# Restore to previous version
spark.sql("RESTORE TABLE table_name TO VERSION AS OF 5")

# Clone table (shallow copy)
spark.sql("CREATE TABLE cloned_table SHALLOW CLONE source_table")

# Convert Parquet to Delta
spark.sql("CONVERT TO DELTA parquet.`/path/`")
```

## Resources I Used Today

- Databricks Delta Lake documentation
- Delta Lake best practices guide
- Community forum discussion on OPTIMIZE

## Tomorrow's Focus

- [ ] Practice more MERGE scenarios
- [ ] Learn about Change Data Feed
- [ ] Understand partition evolution
- [ ] Study streaming with Delta Lake

## Questions to Research

1. How does Delta Lake handle concurrent writes?
2. What's the difference between shallow and deep clone?
3. When should I partition vs Z-ORDER?

---

## Summary
Today I focused on Delta Lake basics and practiced CRUD operations. The most important takeaway is understanding that Delta Lake maintains data lineage through its transaction log, enabling features like Time Travel and ACID guarantees. Need to practice more MERGE operations as they're commonly used in production.

**Study time today:** X hours
**Exercises completed:** X
**Confidence level:** 7/10
