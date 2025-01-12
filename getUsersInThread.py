
from slack_sdk.errors import SlackApiError


def get_users_in_thread(client, channel_id, thread_ts):
    """
    Fetch the list of users who participated in a thread.
    
    :param channel_id: The ID of the channel where the thread is located.
    :param thread_ts: The timestamp of the parent message (root of the thread).
    :return: A set of user IDs who participated in the thread.
    """
    try:
        participants = set()
        next_cursor = None

        while True:
            response = client.conversations_replies(
                channel=channel_id,
                ts=thread_ts,
                cursor=next_cursor
            )

            for message in response['messages']:
                if 'user' in message:  # Ensure the message has a user field
                    participants.add(message['user'])

            next_cursor = response['response_metadata'].get('next_cursor')
            if not next_cursor:
                break

        return participants

    except SlackApiError as e:
        print(f"Error fetching thread replies: {e.response['error']}")
        return set()
