import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("Pipeline iniciado")
logging.info("A extrair commits do GitHub")
logging.warning("Atenção: poucos pedidos disponíveis na API")
logging.error("Exemplo de erro na extração")