import orjson

from json.decoder import JSONDecodeError

from data_platform.broker.kafka_producer import send_to_topic

from data_platform.crud.data_entry import create_data_entry
from data_platform.exceptions import InvalidContent
from data_platform.logger_config import logger
from data_platform.schemas.data_entry import DataEntryCreate, DataEntryCreated
from data_platform.services.base import BaseService




class DEService(BaseService):
    async def create_data_entry(self, data: DataEntryCreate) -> DataEntryCreated:
        """
        Save content data into data_entries PG table, publish data into Kafka topic
        :param data: DataEntryCreate
        :return: int
        """
        self.validate_content(data.content)
        new_entry = await create_data_entry(self.session, data)
        logger.info(f'Successfully added new entry to DB. Id is {new_entry.id}')
        await send_to_topic(data.content, new_entry.id)
        return DataEntryCreated(id=new_entry.id)

    def validate_content(self, content: str) -> None:
        """
        Check if content is valid JSON str or not
        :param content: str
        :return: None
        """
        try:
            orjson.loads(content)
        except JSONDecodeError as e:
            raise InvalidContent(logger)
