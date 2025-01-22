from convertTimeToSlackTs import convert_time_to_slack_ts
def get_lunch_convo_info(client, channel_id) :
    # 앞으로 시간만 바꿔주면됨
    ts = convert_time_to_slack_ts("08:25")
    response = client.conversations_history(
        channel=channel_id, 
        oldest=ts,
        limit=1)
    return response['messages'][0]