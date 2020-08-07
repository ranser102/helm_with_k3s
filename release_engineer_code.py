#!/usr/bin/env python3

import cryptography.fernet as crypt
import os
from slack import WebClient
from slack.errors import SlackApiError

ENCRYPT_CHANNEL = b"gAAAAABfKw8MuDVt12kinZm6Rl3srHXQMmP4im6BB7d7BtkXPr0uWUgjL1-VqRL3IDgTtYdh9vcGY0QXujVo1BeBn_I3eqULsAWv24_Ue52mFYciwN3Zqhs="
ENCRYPT_SLACK_TOKEN = b"gAAAAABfK_1FUMhw6gamMAXovnVGAiQODfGkXX-AuiXaI08PVYNaBoLfDiVbBBOx1c_kM0mXAN4iVJp79j2v-zywZ3nwLFSiLA7I1y9KXUumMfdKCD-W9AJ5uSKv57nQJEOm-yGxEN9fZxjJbAlX7NYQWTO8h6mDVw=="
POD_NAME = os.environ["HOSTNAME"]


def decrypt_something(binary_key, enc_binary):
    key = crypt.Fernet(binary_key)
    return key.decrypt(enc_binary)


def send_slack_message(token, channel, message):
    client = WebClient(token=token)

    try:
        response = client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        assert e.response["error"]
        return False

    return True


def main():
    binary_key = bytes(os.environ["KUBE_SECRET"], "utf-8")
    channel = decrypt_something(binary_key, ENCRYPT_CHANNEL).decode("utf-8")
    token = decrypt_something(binary_key, ENCRYPT_SLACK_TOKEN).decode("utf-8")
    message = "Sending this message from {}".format(POD_NAME)
    send_slack_message(token, channel, message)


if __name__ == "__main__":

    main()
