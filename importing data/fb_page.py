import os
import json
import facebook
from argparse import ArgumentParser

def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--page')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    
    token = os.environ.get('FACEBOOK_TEMP_TOKEN')
    token = 'EAACEdEose0cBAPEztTxEgezYFvA4383zNxONemmZB8byw16OcZByUlv2MJBc2sgfUL4l9ZB92XgpC9h44S9XKjMsNBlces1anZANhVALJ3J00hvSNx8tDYtX5kDZA910rl29J2NdpGssfsZCCQmqrEf3ReZCLGYyBSB9Ijf0gLKnZBqXhFDjVnSejg2T3w3rMsWEKxl15WhtFAZDZD'
    token = 'EAACEdEose0cBADc6rDZB69LLZAOvLw5e16QQHK6ZCl3TacOwInYXUT5jbsMBaXKqmzNKwINuAm7WW1BHnZChXKnZChJ0jsQJ3cIKQwGfEdlcm5ZBEtpmgYbZBBXSZATxtNT8Uz508DZAZAB4yYBSX9LxWZCrZAzCQ8PBuFqNnj2AUONarn9inadNWfUJGw67eYXzMsnUjZBGuxi4BZCZC1ZBtue0uEzSLN9YzVVSeYz75j7QcGtqZCwZDZD'
    fields = [
        'id',
        'name',
        'about',
        'likes',
        'website',
        'links'
        ]
    fields = ','.join(fields)
    
    graph = facebook.GraphAPI(token, version=2.3)
    page = graph.get_object(args.page, fields=fields)
    print(json.dumps(page, indents=4))
