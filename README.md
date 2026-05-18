# E-commerce Data Platform

End-to-end data platform built with PySpark, Delta Lake, and Docker to process Brazilian e-commerce data using the medallion architecture (Bronze → Silver → Gold).

## 🚧 Status

Work in progress. Currently on Phase 0: project setup ✅

## 🛠️ Tech Stack

- **Processing:** Apache Spark 3.5 (PySpark)
- **Storage:** Delta Lake, MinIO (S3-compatible)
- **Database:** MySQL 8
- **Orchestration:** Apache Airflow (planned)
- **Infra:** Docker Compose
- **Language:** Python 3.11

## 📁 Project Structure

```
├── docker/          # Docker configs
├── jobs/            # PySpark jobs (bronze/silver/gold)
├── notebooks/       # Exploratory analysis
├── utils/           # Shared utilities
├── tests/           # Unit tests
└── docs/            # Extra documentation
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.11** (3.12 has known PySpark worker issues on Windows)
- **Java 17** (Temurin recommended) — download from [adoptium.net](https://adoptium.net)
- **Hadoop winutils** (Windows only) — download `winutils.exe` and `hadoop.dll` from [cdarlint/winutils](https://github.com/cdarlint/winutils/tree/master/hadoop-3.3.6/bin) and place them in `C:\hadoop\bin\`
- Docker Desktop (coming in Phase 1)

### Setup

```bash
git clone https://github.com/SEU_USUARIO/ecommerce-data-platform.git
cd ecommerce-data-platform

python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # Mac/Linux

python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.x.x-hotspot
HADOOP_HOME=C:\hadoop
```

### Run hello-world job

```bash
python -m jobs.hello_spark
```

Expected output: aggregated purchase totals grouped by Brazilian state (SP, RJ, MG).

## 📋 Roadmap

- [x] Phase 0: Project setup
- [ ] Phase 1: Docker environment
- [ ] Phase 2: Bronze layer (ingestion)
- [ ] Phase 3: Silver layer (cleaning)
- [ ] Phase 4: Gold layer (business aggregations)
- [ ] Phase 5: Streaming with Kafka
- [ ] Phase 6: Orchestration with Airflow

## 📄 License

MIT