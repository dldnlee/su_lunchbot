


def filter_group(main_list, exclusion_list):
  filtered_list = []
  for id in main_list:
      if id in exclusion_list:
          continue
      else:
          filtered_list.append(id)
  return filtered_list