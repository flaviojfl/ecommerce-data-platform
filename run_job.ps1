

param(
    [Parameter(Mandatory=$true)]
    [string]$JobPath
)

$packages = "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262"

docker compose exec -e PYTHONPATH=/app spark-client `
    /opt/spark/bin/spark-submit `
    --master spark://spark-master:7077 `
    --packages $packages `
    --conf spark.jars.ivy=/tmp/.ivy2 `
    "/app/$JobPath"