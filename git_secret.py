# git_secret
# CLI tool to aid developers in managing secrets when sharing code publicly. 
#
# Usage:
#   python git_secret.py --mode [spec|enter]
#       spec --> generate the secret specification JSON
#       enter --> enter secret information according to the specification

import os
import json
import click

# The spec file name
SPEC_FILE_NAME = "secrets.spec"

# The private secrets file name
SECRET_FILE_NAME = "secrets.private"

# Ensure the .gitignore contains the private secrets file
def setup_gitignore(git_path):
    with open(os.path.join(git_path, ".gitignore"), 'r+') as f:
        for line in f:
            if line == SECRET_FILE_NAME:
                print "Secret file already in .gitignore"
                break
        else:
            f.write("\n# For git-secret\n{}".format(SECRET_FILE_NAME))
            print "Added secret file to .gitignore"

# Generate the secret specification JSON
def do_spec(git_path):
    # Prompt for the secret information as a comma-separated list
    print "Enter secret information as a comma-separated list (example: client_id,client_secret):"
    input_list = raw_input()

    # Parse the input list and prepare JSON object
    secrets = [secret.strip() for secret in input_list.split(",")]
    secrets_obj = {secret: None for secret in secrets}
    secrets_json = json.dumps(secrets_obj, sort_keys=False, indent=4)
    
    # Write object to file
    spec_file_path = os.path.join(git_path, SPEC_FILE_NAME)
    with open(spec_file_path, 'w+') as f:
        f.write(secrets_json)

    # Report status
    print ""
    print "Your input: {}".format(",".join(secrets))
    print "Output to {}:\n{}".format(spec_file_path, secrets_json)

    # Write secret file to .gitignore (if not already there)
    setup_gitignore(git_path)

# Enter secret information according to the specification
def do_enter(git_path):
    # Read in the spec, if it exists
    spec_file_path = os.path.join(git_path, SPEC_FILE_NAME)
    if not os.path.exists(spec_file_path):
        print "Specification file does not exist! Run \"git_secret.py --mode spec\" first."
        exit(1)
    with open(spec_file_path, "r") as f:
        secrets_json = f.read()

    # Parse spec as json
    secrets_obj = json.loads(secrets_json)

    # Prompt user for each secret
    for secret in secrets_obj:
        user_input = raw_input("Enter your value for {}: ".format(secret))
        secrets_obj[secret] = user_input

    # Write out the user's secrets to file
    secret_file_path = os.path.join(git_path, SECRET_FILE_NAME)
    with open(secret_file_path, 'w+') as f:
        json.dump(secrets_obj, f, sort_keys=False, indent=4)

    # Report status
    print ""
    print "Output your secrets to {}".format(secret_file_path)
    print "DO NOT COMMIT THIS FILE! It will be added to your .gitignore if not already present."

    # Write secret file to .gitignore (if not already there)
    setup_gitignore(git_path) 

@click.command()
@click.option("--mode", required=True, type=click.Choice(["spec", "enter"]), help="Mode to run the tool in")
@click.option("--git-path", default=".", type=click.Path(exists=True), help="Path of the git repo")
def main(mode, git_path):
    # Verify git path is a git repo
    git_folder_path = os.path.join(git_path, ".git")
    if not os.path.isdir(git_folder_path):
        print "{} is not a valid .git folder".format(git_path)
        exit(1)

    if mode == "spec":
        do_spec(git_path)
    elif mode == "enter":
        do_enter(git_path)
    else:
        print "Unrecognized mode!"
        exit(1)

if __name__ == '__main__':
    main()