# Technical Decisions

This document explains the key technical choices made in this project, their rationale, and trade-offs considered.

## 1. Medallion Architecture (Bronze → Silver → Gold)

**Decision:** organize the data lake in three layers — raw, cleaned, and aggregated.

**Why:**
- **Traceability** — Bronze preserves the original data, so any issue downstream can be reprocessed without re-fetching from sources
- **Separation of concerns** — each layer has one job (ingest, clean, aggregate); easier to maintain and test
- **Industry standard** — adopted by Databricks, AWS Lake Formation, and most modern data platforms

**Trade-off:** more storage (data is duplicated across layers). Acceptable because object storage is cheap and the benefits in maintainability outweigh the cost.

## 2. MinIO as Object Storage

**Decision:** use MinIO instead of saving Parquet files to a local filesystem or Hadoop HDFS.

**Why:**
- **S3-compatible** — same `s3a://` URLs used in AWS. Migrating to production S3 is a configuration change, not a code change.
- **Accessible from any cluster node** — files on a local filesystem only exist on one node; object storage is reachable by all workers over the network (this was learned the hard way — see decision #6).
- **Standard for modern data lakes** — Delta Lake, Iceberg, and Hudi all assume object storage as the foundation.

**Trade-off:** slightly more complex setup than a local folder. Worth it for realism and portability.

## 3. Parquet as the Storage Format

**Decision:** all data in Bronze/Silver/Gold is stored as Parquet (not CSV or JSON).

**Why:**
- **Columnar** — reads only the columns needed, much faster for analytics
- **Compressed by default** (Snappy) — typically 5–10x smaller than raw CSV
- **Schema embedded** — no need for separate schema files; types are preserved across reads
- **Splittable** — Spark can parallelize reads across partitions

**Trade-off:** not human-readable like CSV. Acceptable because the data lake is consumed by code, not by humans.

## 4. Splitting Sources between MySQL and CSV

**Decision:** load 4 Olist tables (orders, customers, products, sellers) into MySQL and keep the other 5 as CSV files.

**Why:**
- **Simulates a realistic scenario** — real companies ingest from multiple heterogeneous sources (transactional DBs + partner files + APIs)
- **Demonstrates two key connectors** — JDBC (for relational sources) and the Spark CSV reader (for files), both with `s3a` as the destination
- **Forces multi-source orchestration** — the pipeline must coordinate ingestion from different systems

**Trade-off:** more moving parts in the setup. The realism is worth it for the portfolio.

## 5. Standalone Spark Cluster (Master + Worker) instead of Local Mode

**Decision:** run Spark as a real cluster in Docker (master + worker), not in `local[*]` mode.

**Why:**
- **Realistic** — production Spark always runs as a cluster (YARN, Kubernetes, standalone)
- **Reveals networking issues early** — driver, master, and workers must communicate over a network; same challenges as production
- **Submitting via `spark-submit`** — the standard way to deploy jobs, not just calling Python directly

**Trade-off:** more memory consumed (master, worker, and client containers). Acceptable on a development machine with 8+ GB RAM.

## 6. Mounting `./data` on the Spark Worker (not only on the client)

**Decision:** the CSV files volume is mounted on both `spark-client` and `spark-worker`.

**Why:** initially I mounted only on the client and the CSV ingestion failed at runtime with `FileNotFoundException`. The reason: when reading a local file, Spark distributes the read task to executors (which run on the worker), and the worker had no access to the file.

**Lesson:** in a real cluster, you avoid this entirely by storing source data in object storage (S3/MinIO) — every node accesses it over HTTP. The volume mount in this project is a development shortcut; the production-correct approach is to upload raw files to MinIO first, then read from `s3a://`.

## 7. Pipeline Orchestrator as a Python Script (instead of Airflow)

**Decision:** orchestrate Bronze → Silver → Gold using a simple Python script (`scripts/run_pipeline.py`) instead of Apache Airflow.

**Why:**
- **Lower infrastructure cost** — Airflow requires a webserver, scheduler, and metadata database; significant overhead on a development machine
- **Captures the core concepts** — sequential dependencies, error handling, and pipeline interruption on failure — without the operational complexity
- **Easy to upgrade later** — the same job structure (each step is a self-contained `spark-submit`) maps directly to Airflow `BashOperator` or `SparkSubmitOperator` tasks

**Trade-off:** no UI, no scheduling, no retry policies. Adding Airflow is on the roadmap.

## 8. Secrets in `.env`, never in code or compose

**Decision:** all credentials (MinIO keys, MySQL passwords) live in a `.env` file, referenced by `docker-compose.yml` via `${VARIABLE}` syntax.

**Why:**
- **`.env` is in `.gitignore`** — secrets never reach the repository
- **`docker-compose.yml` can be public** — only describes structure, no values
- **`.env.example` documents required variables** — anyone cloning the repo knows what they need to provide

**Trade-off:** requires manual setup of `.env` on each new environment. This is the standard practice; trade-off is purely cosmetic.

## 9. Java 17 for Spark, with explicit JVM flags

**Decision:** use Java 17 (not 21 or 25) and pass `--add-opens` flags to the JVM.

**Why:**
- **Java 17 is officially supported by Spark 3.5** — newer versions (21, 25) work in some cases but are not validated by the Spark project
- **The `--add-opens` flags are required** because Spark accesses internal JDK classes through reflection; since Java 9, the module system blocks this by default

**Trade-off:** older Java version than what some new projects use. Stability matters more than recency for production data systems.

## 10. Streaming with Kafka in KRaft mode (no Zookeeper)

**Decision:** use Kafka 3.8 in KRaft mode for streaming, not the older Zookeeper-based setup.

**Why:**
- **One less service to run** — KRaft replaces Zookeeper with internal Kafka metadata management
- **Future-proof** — Zookeeper is being deprecated; KRaft is the production-ready successor
- **Easier configuration** — fewer moving parts, simpler `docker-compose.yml`

**Trade-off:** KRaft is newer (production-ready since Kafka 3.3), so fewer tutorials and community examples. Worth it for the simpler architecture.