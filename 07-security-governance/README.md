# Security and Governance

## Overview
This section covers security, access control, and data governance in Databricks.

## Topics to Study

### 1. Unity Catalog
- Unity Catalog architecture
- Metastore concepts
- Catalogs, schemas, and tables hierarchy
- Benefits of Unity Catalog

### 2. Access Control
- Table ACLs (Access Control Lists)
- Column-level security
- Row-level security
- Dynamic views for access control

### 3. Identity and Access Management
- Users and service principals
- Groups and group management
- Authentication methods
- SSO and SCIM integration

### 4. Data Security
- Encryption at rest and in transit
- Secrets management with Databricks Secrets
- Secret scopes
- Credential passthrough

### 5. Auditing and Compliance
- Audit logs
- Monitoring data access
- Compliance features
- Data lineage

### 6. Best Practices
- Principle of least privilege
- Securing notebooks and jobs
- Managing credentials securely
- Data classification and tagging

## Key Concepts to Master
- Unity Catalog three-level namespace
- Implementing least privilege access
- Using secrets securely
- Understanding different authentication methods
- Data lineage and governance

## Practice Areas
- Set up table and column permissions
- Create secure views with row-level filtering
- Manage secrets using secret scopes
- Grant and revoke permissions
- Implement data access patterns

## Common Commands
```sql
-- Grant permissions
GRANT SELECT ON TABLE catalog.schema.table TO `user@example.com`;
GRANT MODIFY ON SCHEMA catalog.schema TO `data-engineers`;

-- Revoke permissions
REVOKE SELECT ON TABLE catalog.schema.table FROM `user@example.com`;

-- Show grants
SHOW GRANTS ON TABLE catalog.schema.table;

-- Create secure view with row-level security
CREATE VIEW secure_view AS
SELECT * FROM table
WHERE region = current_user();
```

## Security Checklist
- [ ] Enable Unity Catalog
- [ ] Configure appropriate access controls
- [ ] Use secrets for credentials
- [ ] Enable audit logging
- [ ] Implement data classification
- [ ] Regular access reviews
- [ ] Encrypt sensitive data

## Resources
Add your security configurations, policies, and governance documentation here.
