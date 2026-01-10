# Toronto Public Resource Density

This project is a backend service that analyzes the distribution and density of public resources across Toronto neighbourhoods using open municipal data. It is designed to simulate real-world civic analytics systems, focusing on data ingestion, normalization, aggregation, and API design.

**Tech stack:**
- Python
- FastAPI
- PostgreSQL
- pandas / GeoPandas
- Docker (planned)

**MVP checklist:**
- [ ] Ingest public washroom dataset
- [ ] Ingest childcare facilities dataset
- [ ] Normalize and store resource data
- [ ] Map resources to Toronto neighbourhoods
- [ ] Compute resource counts per neighbourhood
- [ ] Expose REST API endpoints

**Planned API endpoints:**
```bash
GET /neighbourhoods
GET /resources?type=washroom
GET /density?resource_type=childcare
```
