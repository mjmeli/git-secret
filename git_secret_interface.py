# git_secret_interface
# Tool and library to aid developers in managing secrets when sharing code publicly. 
# This is the source code interface (for Python).
#
# Usage:
#   from git_secret_interface import GitSecretInterface
#   secret_inferface = GitSecretInterface([git file path])
#   secret = secret_interface.get([secret key])

import os
import json

# The private secrets file name
SECRET_FILE_NAME = "secrets.private"

class GitSecretException(Exception):
    pass

class GitSecretInterface:
    # Requires the git repository base path
    def __init__(self, git_path="."):
        # Verify git path is a git repo
        git_folder_path = os.path.join(git_path, ".git")
        if not os.path.isdir(git_folder_path):
            raise GitSecretException("{} is not a valid .git folder".format(git_path))
        self.git_path = git_path

        # Read in the secrets file (if it exists)
        secret_file_path = os.path.join(git_path, SECRET_FILE_NAME)
        if not os.path.exists(secret_file_path):
            raise GitSecretException("Secret file does not exist! Run \"git_secret.py --mode secrets\" first.")
        with open(secret_file_path, 'r') as f:
            self.secrets = json.load(f)

    # Returns a secret by key
    def get(self, key):
        if key not in self.secrets:
            raise GitSecretException("Secret file does not contain the key {}".format(key))
        else:
            return self.secrets[key]