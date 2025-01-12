from convertTimeToSlackTs import convert_time_to_slack_ts
def get_lunch_convo_info(client, channel_id) :
    # 앞으로 시간만 바꿔주면됨
    ts = convert_time_to_slack_ts("13:29")
    response = client.conversations_history(
        channel=channel_id, 
        oldest=ts,
        limit=5)
    
    for message in response['messages']:
        if "오늘의 점심 팀은" in message['text']:
            lunch_msg_info = message
            break
    return lunch_msg_info