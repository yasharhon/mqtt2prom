from contextlib import asynccontextmanager
from json import loads as jsonloads
from typing import Any

from fastapi import FastAPI
from paho.mqtt.client import Client as MqttClient, CallbackAPIVersion, MQTTMessage

from routes import metrics_router
from settings import AppSettings

settings = AppSettings(_env_file=".env")


# This should possibly be structured differently so that it could lie somewhere else
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dictionary mapping topic name to latest polled data
    app.state.polled_data: dict[str, dict[str, Any]] = {}

    client = MqttClient(CallbackAPIVersion.VERSION2)

    # This needs to handle arbitrary auth
    if settings.mqtt_username:
        client.username_pw_set(settings.mqtt_username, settings.mqtt_password)

    def on_message(client: MqttClient, userdata: Any, msg: MQTTMessage):
        topic_name = msg.topic
        app.state.polled_data[topic_name] = jsonloads(msg.payload)

    client.on_message = on_message
    client.connect(settings.mqtt_host, settings.mqtt_port, 60)
    client.loop_start()

    yield

    client.disconnect()
    client.loop_stop()


app = FastAPI(lifespan=lifespan)

app.include_router(metrics_router)
