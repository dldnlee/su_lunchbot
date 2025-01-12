from slack_sdk.errors import SlackApiError

def get_all_users_in_channel(client, channel_id):
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
            username = member_info['user']['id']
            # Exclude bots
            if member_info['user']['is_bot']:
                continue
            usernames.append(username)

        return usernames

    except SlackApiError as e:
        print(f"Error fetching users: {e.response['error']}")
        return []