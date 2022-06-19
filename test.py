import os

try:
        sg = (os.environ['EMAIL_API_KEY'])
except Exception as e:
        print("Environment Variable {} not found!".format(e))
        exit()
    