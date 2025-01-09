import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import random

# Load environment variables
load_dotenv()
bot_token = os.getenv('SLACK_BOT_TOKEN')
app_token = os.getenv('SLACK_APP_TOKEN')

# Initialize the Bolt app
app = App(token=bot_token)
client = WebClient(token=bot_token)


def get_all_users_in_channel(channel_id):
    try:
        members = []
        usernames = []
        next_cursor = None

        while True:
            response = client.conversations_members(
                channel=channel_id,
                cursor=next_cursor
            )
            members.extend(response['members'])

            next_cursor = response['response_metadata'].get('next_cursor')
            if not next_cursor:
                break

        for member in members:
            member_info = client.users_info(user=member)
            username = member_info['user']['real_name']
            # Exclude bots
            if member_info['user']['is_bot']:
                continue
            usernames.append(username)

        return usernames

    except SlackApiError as e:
        print(f"Error fetching users: {e.response['error']}")
        return []


def split_into_groups(usernames, num_groups):
    random.shuffle(usernames)
    groups = [[] for _ in range(num_groups)]
    for index, username in enumerate(usernames):
        groups[index % num_groups].append(username)
    return groups


@app.command("/splitusers")
def handle_split_command(ack, body, say):
    """Handles the /splitusers command"""
    ack()  # Acknowledge the slash command immediately
    #
    # # Extract the mentioned users from the command text
    # text = body.get('text', '')
    # user_mentions = text.strip().split()
    #
    # # Extract user IDs from mentions (formatted as <@USERID>)
    # user_ids = [mention.strip('<@>') for mention in user_mentions]

    # Fetch real names for each mentioned user (for group splitting)
    # mentioned_users = []
    # for user_id in user_ids:
    #     try:
    #         user_info = client.users_info(user=user_id)
    #         username = user_info['user']['real_name']
    #         mentioned_users.append(username)
    #     except SlackApiError as e:
    #         print(f"Error fetching user info for {user_id}: {e.response['error']}")

    # Split the mentioned users into two groups
    num_groups = 2  # You can make this dynamic if needed
    usernames = get_all_users_in_channel("C086VHF8YTG")

    groups = split_into_groups(usernames, num_groups)

    # Send a formatted response message back to the channel
    response_message = "Here are the split groups:\n"
    for i, group in enumerate(groups, start=1):
        group_mentions = ", ".join([f"@{user}" for user in group])
        response_message += f"Group {i}:\n - {group_mentions}\n"

    # Post the result back in the channel
    say(response_message)


if __name__ == "__main__":
    # Start the Bolt app using Socket Mode
    SocketModeHandler(app, app_token).start()
