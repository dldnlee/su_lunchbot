from slack_sdk.errors import SlackApiError

def get_users_info(client, user_list) :
  user_information_list = []


  try:
    for user in user_list:
      result = client.users_info(
        user=user
      )
      user_information_list.append(result['user']['real_name'])
      print(user_information_list)
  except SlackApiError as e:
        print(f"Error fetching users: {e.response['error']}")
        return []

  return user_information_list