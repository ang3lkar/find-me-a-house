import argparse

# Setup command line arguments
PARSER = argparse.ArgumentParser(description='Fetch the latest appartments')
PARSER.add_argument('-d', '--dry-run', default=False, action='store_true',
                    help='Display the results in terminal but do not broadcast')
PARSER.add_argument('-r', '--reset', default=False, action='store_true',
                    help='Drop all tables')
ARGS = PARSER.parse_args()

def get():
    return ARGS
