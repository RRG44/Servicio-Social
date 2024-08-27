"""This function transforms string hh:mm-hh:mm to float"""

def separateHours(hours):
  split = hours.split("-")

  for i in range(len(split)):
      split[i] = split[i].replace(":00", "")
      if split[i][0] == "0":
          split[i] = split[i][1:]

  return float(split[0]), float(split[1]) # Example hours: 8:00-9:00, output: 8.0, 9.0