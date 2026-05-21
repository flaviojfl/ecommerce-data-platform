# E-commerce Data Platform

End-to-end data platform built with PySpark, Delta Lake, and Docker to process Brazilian e-commerce data using the medallion architecture (Bronze → Silver → Gold).

## 🚧 Status

Work in progress.
- ✅ Phase 0: Project setup + local PySpark
- ✅ Phase 1: Docker environment (Spark cluster, MinIO, MySQL, Jupyter)
- ⬜ Phase 2: Bronze layer (ingestion)

## 🏗️ Architecture

Full diagram in [docs/architecture.md](docs/architecture.md).

```
MySQL (OLTP) ──JDBC──► Spark Cluster ──s3a──► MinIO (Data Lake)
                            ▲
                       Jupyter Lab
```

## 🛠️ Tech Stack

- **Processing:** Apache Spark 3.5 (PySpark), running as a standalone cluster
- **Storage:** MinIO (S3-compatible object storage)
- **Database:** MySQL 8 (transactional source)
- **Exploration:** Jupyter Lab
- **Infra:** Docker Compose
- **Language:** Python 3.11

## 🚀 Getting Started

### Prerequisites

- Docker Desktop
- Python 3.11 (for local development outside Docker)
- Java 17 (for running PySpark locally — optional, the cluster runs in Docker)

### Setup

1. Clone the repo:
```bash
   git clone https://github.com/flaviojfl/ecommerce-data-platform.git
   cd ecommerce-data-platform
```

2. Create your `.env` from the example:
```bash
   cp .env.example .env
   # Edit .env with your own values
```

3. Start the environment:
```powershell
   .\manage.ps1 up
```

### Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Spark Master UI | http://localhost:8080 | — |
| MinIO Console | http://localhost:9001 | from `.env` |
| Jupyter Lab | http://localhost:8888 | no auth (dev) |
| MySQL | localhost:3307 | from `.env` |

### Running jobs

```powershell
.\run_job.ps1 jobs/test_minio.py
```

## 📋 Roadmap

- [x] Phase 0: Project setup
- [x] Phase 1: Docker environment
- [ ] Phase 2: Bronze layer (ingestion)
- [ ] Phase 3: Silver layer (cleaning)
- [ ] Phase 4: Gold layer (business aggregations)
- [ ] Phase 5: Streaming with Kafka
- [ ] Phase 6: Orchestration with Airflow

## 📄 License

MIT