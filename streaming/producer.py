import json
import random
import time
from datetime import datetime, timezone

from faker import Faker
from kafka import KafkaProducer

fake = Faker("pt_BR")

ESTADOS = ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE", "CE", "GO"]
ACOES = ["page_view", "product_view", "add_to_cart", "purchase", "search"]
CATEGORIAS = ["eletronicos", "moda", "casa", "esporte", "livros", "beleza"]


def gerar_evento() -> dict:
    return {
        "event_id": fake.uuid4(),
        "user_id": f"user_{random.randint(1, 5000)}",
        "action": random.choices(ACOES, weights=[50, 30, 10, 5, 15])[0],
        "category": random.choice(CATEGORIAS),
        "state": random.choice(ESTADOS),
        "value": round(random.uniform(10, 2000), 2),
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    producer = KafkaProducer(
        bootstrap_servers="localhost:29092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    print("Produzindo eventos no topico 'clickstream'. Ctrl+C para parar.")
    contador = 0
    try:
        while True:
            evento = gerar_evento()
            producer.send("clickstream", value=evento)
            contador += 1
            if contador % 10 == 0:
                print(f"  {contador} eventos enviados | ultimo: {evento['action']} em {evento['state']}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\nParado. Total enviado: {contador} eventos.")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()