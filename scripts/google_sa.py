#!/usr/bin/python

import sys, getopt
import os
from google.oauth2 import service_account
import googleapiclient.discovery

#
# Show usage
#
def usage():
  print('Usage:')
  print('')
  print(f'  Creating a new service account: "{script_name} -c <service account> -n <display name> -p <project id>"')
  print('')

#
# Display arguments information
#
def show_arg_info():
  print ('Number of arguments:', len(sys.argv), 'arguments.')
  print ('Argument List:', str(sys.argv))
  print ('')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Code by Google - Start
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
#
# Create service account
#
def create_service_account(project_id, name, display_name):
    """Creates a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    my_service_account = service.projects().serviceAccounts().create(
        name='projects/' + project_id,
        body={
            'accountId': name,
            'serviceAccount': {
                'displayName': display_name
            }
        }).execute()

    print('Created service account: ' + my_service_account['email'])
    return my_service_account

#
# List service account
#
def list_service_accounts(project_id):
    """Lists all service accounts for the current project."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service_accounts = service.projects().serviceAccounts().list(
        name='projects/' + project_id).execute()

    for account in service_accounts['accounts']:
        print('Name: ' + account['name'])
        print('Email: ' + account['email'])
        print(' ')
    return service_accounts

#
# Update service account
#
def rename_service_account(email, new_display_name):
    """Changes a service account's display name."""

    # First, get a service account using List() or Get()
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    resource = 'projects/-/serviceAccounts/' + email

    my_service_account = service.projects().serviceAccounts().get(
        name=resource).execute()

    # Then you can update the display name
    my_service_account['displayName'] = new_display_name
    my_service_account = service.projects().serviceAccounts().update(
        name=resource, body=my_service_account).execute()

    print('Updated display name for {} to: {}'.format(
        my_service_account['email'], my_service_account['displayName']))
    return my_service_account

#
# Disable service account
#
def disable_service_account(email):
    """Disables a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service.projects().serviceAccounts().disable(
        name='projects/-/serviceAccounts/' + email).execute()

    print("Disabled service account :" + email)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Code by Google - end
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#
# Main Menu
#
def main(argv):

  try:
    opts, args = getopt.getopt(argv,"hclp:a:n:u:d",["project-id=","create","account=","name=","update=","delete=","list"])
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      usage()
      sys.exit()
    elif opt in ("-p", "--project-id"):
      project=arg
    elif opt in ("-c", "--create"):
      action='create'
    elif opt in ("-a", "--account"):
      account=arg
    elif opt in ("-n", "--name"):
      display_name=arg
    elif opt in ("-l", "--list"):
      print (f"Output file {ofile(arg)}")
    elif opt in ("-u", "--update"):
      print (f"Output file {ofile(arg)}")
    elif opt in ("-d", "--delete"):
      print (f"Output file {ofile(arg)}")

  print (f"Action={action}")
  print (f"Project ID={project}")
  print (f"Account={account}")
  print (f"Display name {display_name}")

  if action == "create":
    create_service_account(project, account, display_name)

#
# Main
#
if __name__ == "__main__":
  # Read arguments from command line 
  script_name = sys.argv[0]
  show_arg_info()
  main(sys.argv[1:])  