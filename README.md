# DevOps Entry Task

### Recall Task Requirements

### Phase 1: Deploy
Use docker to initialize two services:
1. Python `fastapi` API service
2. MySQL Database service

### Phase 2: Migration
1. Initialize another PostgreSQL service in another container
2. Migrate the data from existing MySQL to PostgreSQL
3. Run and test the API service, using the new PostgreSQL database instead

### Difference betweem Phase_1/Version_1 and Phase_1/Version_2
1-1_v1 built the python image itself, and 1-1_v2 pulled the image directly.
