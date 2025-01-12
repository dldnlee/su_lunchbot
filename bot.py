import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from splitIntoGroups import split_into_groups
from splitIntoGroups import split_into_groups
from filterGroup import filter_group
from getLunchConvoInfo import get_lunch_convo_info

# Load environment variables
load_dotenv()
bot_token = os.getenv('SLACK_BOT_TOKEN')
app_token = os.getenv('SLACK_APP_TOKEN')
channel_id = os.getenv('SLACK_CHANNEL_ID')

# Initialize the Bolt app
app = App(token=bot_token)
# Initialize the Client
client = WebClient(token=bot_token)

@app.command("/splitusers")
def handle_split_command(ack, body, say):
    ack()
    # 인트로 텍스트
    say("🥁두근두근..")
    # Get text content within the split command
    text = body.get('text', '')
    print(f"Body text {text}")

    # Turn the split command text content into a list
    command_text = text.strip().split()
    # Get the number of groups to split it into
    num_groups = int(command_text[0])
    # Get the mentioned users
    user_mentions = command_text[1:]
    
    # Get List of Mentioned Ids
    mentioned_ids = [mention.strip('<@>').split("|")[0] for mention in user_mentions]
    print(f"The mentioned users is {mentioned_ids}")

    # Get List of ids that have replied to the convo
    user_list = get_lunch_convo_info(client, channel_id)["reply_users"]
    print(f"The user list is: {user_list}")

    # Remove the mentioned ids from the main list
    filtered_list = filter_group(user_list, mentioned_ids)
    print(f"The filtered list is {filtered_list}")

    # Split the mentioned users into the number of groups defined in the command
    groups = split_into_groups(user_list, num_groups)

    # Send a formatted response message back to the channel
    response_message = "🍖 오늘의 점심 팀 🍖\n"
    for i, group in enumerate(groups, start=1):
        group_mentions = ", ".join([f"<@{user_id}>" for user_id in group])
        response_message += f"Group {i}:\n - {group_mentions}\n"

    # Post the result back in the channel
    say(response_message)


# Main Run
if __name__ == "__main__":
    # Start the Bolt app using Socket Mode
    SocketModeHandler(app, app_token).start()
