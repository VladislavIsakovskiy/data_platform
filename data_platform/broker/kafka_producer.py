from aiokafka import AIOKafkaProducer
from data_platform.config import settings

from data_platform.logger_config import logger

async def send_to_topic(message: str, entry_id: int) -> None:
    """
    Send content message for specific Kafka topic
    :param message: str
    :param entry_id: int
    :return: None
    """
    producer = AIOKafkaProducer(bootstrap_servers=settings.broker.url)
    await producer.start()
    try:
        logger.info(f'Sending message with id {entry_id} to Kafka {settings.broker.TOPIC} topic')
        await producer.send_and_wait(settings.broker.TOPIC, message.encode('utf-8'))
        logger.info(f'Message successfully sent!')
    finally:
        await producer.stop()
