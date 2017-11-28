# example
# Example of using the git_secret_interface

import os
from git_secret_interface import GitSecretInterface

script_directory = os.path.dirname(os.path.realpath(__file__))

secret_inferface = GitSecretInterface(script_directory)

print "username: {}".format(secret_inferface.get("username"))
print "password: {}".format(secret_inferface.get("password"))
print "client_id: {}".format(secret_inferface.get("client_id"))
print "client_secret: {}".format(secret_inferface.get("client_secret"))
print "security_token: {}".format(secret_inferface.get("security_token"))