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
current_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)

bot_token = os.getenv('SLACK_BOT_TOKEN')
app_token = os.getenv('SLACK_APP_TOKEN')
channel_id = os.getenv('SLACK_CHANNEL_ID')

# Initialize the Bolt app
app = App(token=bot_token)
# Initialize the Client
client = WebClient(token=bot_token)


@app.command("/lunch")
def handle_split_command(ack, body, say):
    ack()
    # 인트로 텍스트
    say("🥁그룹 생성중...")
    # Slash Command 이후의 텍스트 불러오기
    text = body.get('text', '')
    # print(f"Body text {text}")
    try:

        # Slash Command 리스트로 변환
        command_text = text.strip().split()
        # Get the number of groups to split it into
        if command_text: num_groups = int(command_text[0])
        else : num_groups = 3 # default = 3
        # Get the mentioned users
        user_mentions = command_text[1:]
        
        # Get List of Mentioned Ids
        mentioned_ids = [mention.strip('<@>').split("|")[0] for mention in user_mentions]
        # debugging
        # print(f"The mentioned users is {mentioned_ids}")

        # Get List of ids that have replied to the convo
        lunch_convo_info = get_lunch_convo_info(client, "C060ML4KF8E")
        user_list = lunch_convo_info['reply_users']
        # user_list = get_lunch_convo_info(client, "C060ML4KF8E")
        # debugging
        # print(f"The user list is: {user_list}")


        # Exclude 영현님
        mentioned_ids.append('U060RBWE6FP') # 영현님 아이디 제외 리스트에 추가
        # debugging
        # print(mentioned_ids)

        # Exclude users that have reacted to the '공지채널 데일리 스크럼' message
        if "reactions" in lunch_convo_info: 
            for reaction in lunch_convo_info["reactions"]:
                for user_id in reaction.get("users", []):
                    if user_id not in mentioned_ids:
                        mentioned_ids.append(user_id)
        else: 
            pass

        # Remove the mentioned ids from the main list
        filtered_list = filter_group(user_list, mentioned_ids)

        # 현존님 추가
        # filtered_list.append("U060T6810VC")
        # print(f"The filtered list is {filtered_list}")

        # Split the mentioned users into the number of groups defined in the command
        groups = split_into_groups(filtered_list, num_groups)
        # print(groups)

        # Send a formatted response message back to the channel
        response_message = "🍖 오늘의 점심 팀 🍖\n\n"
        for i, group in enumerate(groups, start=1):
            group_mentions = ", ".join([f"<@{user_id}>" for user_id in group])
            response_message += f"점심 팀 {i}:\n - {group_mentions}\n\n"

        # Post the result back in the channel
        say(response_message)
        say("점심 맛있게 드세요!")
    except:
        say("입력 형식을 지켜주세요:\n/lunch (그룹 수) @제외인원 @제외인원 ..")


# Main Run
if __name__ == "__main__":
    # Start the Bolt app using Socket Mode
    SocketModeHandler(app, app_token).start()
