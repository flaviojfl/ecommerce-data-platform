import subprocess
import sys
import time

PACKAGES = (
    "org.apache.hadoop:hadoop-aws:3.3.4,"
    "com.amazonaws:aws-java-sdk-bundle:1.12.262,"
    "com.mysql:mysql-connector-j:8.4.0"
)

PIPELINE = [
    ("Bronze - MySQL", "jobs/bronze/ingest_mysql.py"),
    ("Bronze - CSV", "jobs/bronze/ingest_csv.py"),
    ("Silver - Transform", "jobs/silver/transform_orders.py"),
    ("Gold - Metrics", "jobs/gold/build_metrics.py"),
]


def run_job(job_path: str) -> bool:
    cmd = [
        "docker", "compose", "exec", "-T",
        "-e", "PYTHONPATH=/app",
        "spark-client",
        "/opt/spark/bin/spark-submit",
        "--master", "spark://spark-master:7077",
        "--packages", PACKAGES,
        "--conf", "spark.jars.ivy=/tmp/.ivy2",
        f"/app/{job_path}",
    ]
    result = subprocess.run(cmd)
    return result.returncode == 0


def main() -> None:
    print("=" * 60)
    print("INICIANDO PIPELINE: Bronze -> Silver -> Gold")
    print("=" * 60)

    inicio_total = time.time()

    for i, (nome, job_path) in enumerate(PIPELINE, start=1):
        print(f"\n[{i}/{len(PIPELINE)}] Executando: {nome}")
        print("-" * 60)

        inicio = time.time()
        sucesso = run_job(job_path)
        duracao = time.time() - inicio

        if sucesso:
            print(f"\n[OK] {nome} concluido em {duracao:.1f}s")
        else:
            print(f"\n[FALHA] {nome} falhou apos {duracao:.1f}s")
            print("Pipeline interrompido. Corrija o erro e rode novamente.")
            sys.exit(1)

    duracao_total = time.time() - inicio_total
    print("\n" + "=" * 60)
    print(f"PIPELINE CONCLUIDO COM SUCESSO em {duracao_total:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()