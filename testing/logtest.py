from wowlib import mongoconnection

users = mongoconnection.userconnection()


print(users.find_one())