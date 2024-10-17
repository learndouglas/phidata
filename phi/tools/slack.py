import json
from typing import Optional, Dict, Any

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from phi.tools.toolkit import Toolkit
from phi.utils.log import logger


class SlackTools(Toolkit):
    def __init__(self, token: str):
        super().__init__(name="slack")
        self.client = WebClient(token=token)
        self.register(self.send_message)
        self.register(self.list_channels)
        self.register(self.get_channel_history)

    def send_message(self, channel: str, text: str) -> str:
        """
        Send a message to a Slack channel.
        
        Args:
            channel (str): The channel ID or name to send the message to.
            text (str): The text of the message to send.
        
        Returns:
            str: A JSON string containing the response from the Slack API.
        """
        try:
            response = self.client.chat_postMessage(channel=channel, text=text)
            return json.dumps(response.data)
        except SlackApiError as e:
            logger.error(f"Error sending message: {e}")
            return json.dumps({"error": str(e)})

    def list_channels(self) -> str:
        """
        List all channels in the Slack workspace.
        
        Returns:
            str: A JSON string containing the list of channels.
        """
        try:
            response = self.client.conversations_list()
            channels = [{"id": channel["id"], "name": channel["name"]} for channel in response["channels"]]
            return json.dumps(channels)
        except SlackApiError as e:
            logger.error(f"Error listing channels: {e}")
            return json.dumps({"error": str(e)})

    def get_channel_history(self, channel: str, limit: int = 100) -> str:
        """
        Get the message history of a Slack channel.
        
        Args:
            channel (str): The channel ID to fetch history from.
            limit (int): The maximum number of messages to fetch. Defaults to 100.
        
        Returns:
            str: A JSON string containing the channel's message history.
        """
        try:
            response = self.client.conversations_history(channel=channel, limit=limit)
            messages = [{"text": msg["text"], "user": msg["user"], "ts": msg["ts"]} for msg in response["messages"]]
            return json.dumps(messages)
        except SlackApiError as e:
            logger.error(f"Error getting channel history: {e}")
            return json.dumps({"error": str(e)})