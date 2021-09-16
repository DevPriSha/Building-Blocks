#TODO - fetch user info using username (Username and Honor)
#TODO - fetch list_completed_challenges through API at specific intervals
#if 1st ques == quesAssigned:
#    check honor (should not be equal to prevHonor)


import json
import requests

user = requests.get("https://www.codewars.com/api/v1/users/DevPriSha")
user1 = json.loads(user.text)
print(type(user1.get("honor")))

link = "https://www.codewars.com/kata/57a0556c7cb1f31ab3000ad7/train/"
print(link.split(sep = '/')[4])