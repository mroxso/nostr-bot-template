import requests
import time
import ssl
import os
from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey

relay_manager = RelayManager()
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
time.sleep(1.25) # allow the connections to open

env_private_key = os.environ.get("PRIVATE_KEY")
if not env_private_key:
    print('The environment variable "PRIVATE_KEY" is not set.')
    exit(1)

private_key = PrivateKey(bytes.fromhex(env_private_key))

old_block_height = 0
while True:
    url = "https://blockchain.info/latestblock"
    response = requests.get(url)
    data = response.json()
    block_height = data["height"]

    if(block_height > old_block_height):
        message = "⚡️ " + str(block_height) + " ⚡️"
        print(message)
        event = Event(
            content=str(message),
            public_key=private_key.public_key.hex()
        )
        private_key.sign_event(event)
        relay_manager.publish_event(event)

        old_block_height = block_height
        
    time.sleep(5)

