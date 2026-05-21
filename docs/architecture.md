# Arquitetura da Plataforma

## Visão geral

```mermaid
flowchart LR
    MySQL[(MySQL<br/>OLTP)]
    MinIO[(MinIO<br/>Data Lake S3)]
    Master[Spark Master]
    Worker[Spark Worker]
    Client[Spark Client<br/>spark-submit]
    Jupyter[Jupyter Lab<br/>Exploração]

    MySQL -->|JDBC| Client
    Client -->|s3a| MinIO
    MySQL -->|JDBC| Jupyter
    Jupyter -->|s3a| MinIO
    Client -.submit.-> Master
    Jupyter -.submit.-> Master
    Master --> Worker

    subgraph Docker Network: data-platform
        Master
        Worker
        Client
        Jupyter
        MySQL
        MinIO
    end
```

## Medallion Architecture (camadas)

```mermaid
flowchart LR
    Source[(MySQL + CSVs)] -->|ingestão| Bronze[Bronze<br/>dados crus]
    Bronze -->|limpeza| Silver[Silver<br/>dados tratados]
    Silver -->|agregação| Gold[Gold<br/>métricas de negócio]
    Gold --> BI[Dashboards / Analytics]
```

## Componentes

| Serviço | Função | Porta (host) |
|---------|--------|--------------|
| spark-master | Coordena o cluster | 8080 (UI), 7077 |
| spark-worker | Executa tarefas | 8081 (UI) |
| spark-client | Submete jobs via spark-submit | — |
| minio | Object storage (data lake) | 9000 (API), 9001 (console) |
| mysql | Banco transacional (fonte) | 3307 |
| jupyter | Exploração interativa | 8888 |

## Fluxo de dados

1. **Ingestão**: Spark lê do MySQL (JDBC) e de arquivos CSV
2. **Bronze**: dados crus salvos em Parquet no MinIO (`s3a://lakehouse/bronze/`)
3. **Silver**: limpeza, padronização e deduplicação (`s3a://lakehouse/silver/`)
4. **Gold**: agregações e métricas de negócio (`s3a://lakehouse/gold/`)