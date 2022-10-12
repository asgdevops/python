#!/usr/bin/python

import sys, getopt
import os
import googleapiclient.discovery

from collections import defaultdict
from google.oauth2 import service_account
from google.cloud import compute_v1
from typing import Iterable
from typing import Dict, Iterable

#
# List all VM instances by rpoject_id
#
def list_all_instances(
    project_id: str,
) -> Dict[str, Iterable[compute_v1.Instance]]:
    """
    Returns a dictionary of all instances present in a project, grouped by their zone.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
    Returns:
        A dictionary with zone names as keys (in form of "zones/{zone_name}") and
        iterable collections of Instance objects as values.
    """
    instance_client = compute_v1.InstancesClient()
    request = compute_v1.AggregatedListInstancesRequest()
    request.project = project_id
    # Use the `max_results` parameter to limit the number of results that the API returns per response page.
    request.max_results = 50

    agg_list = instance_client.aggregated_list(request=request)

    all_instances = defaultdict(list)
    print("Instances found:")
    # Despite using the `max_results` parameter, you don't need to handle the pagination
    # yourself. The returned `AggregatedListPager` object handles pagination
    # automatically, returning separated pages as you iterate over the results.
    for zone, response in agg_list:
        if response.instances:
            all_instances[zone].extend(response.instances)
            print(f" {zone}:")
            for instance in response.instances:
                print(f" - {instance.name} ({instance.machine_type})")
    return all_instances

#
# List VM Instances by project_id and zone
#
def list_instances(project_id: str, zone: str) -> Iterable[compute_v1.Instance]:
    """
    List all instances in the given zone in the specified project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
    Returns:
        An iterable collection of Instance objects.
    """
    instance_client = compute_v1.InstancesClient()
    instance_list = instance_client.list(project=project_id, zone=zone)

    print(f"Instances found in zone {zone}:")
    for instance in instance_list:
        print(f" - {instance.name} ({instance.machine_type})")

    return instance_list

#
# Show usage
#
def usage():
  print('Usage:')
  print(f'{script_name} -p <project_id> -z <zone>"')
  print('')

#
# Display arguments information
#
def show_arg_info():
  print ('Number of arguments:', len(sys.argv), 'arguments.')
  print ('Argument List:', str(sys.argv))
  print ('')

#
# Main Menu
#
def main(argv):

  action=''

  try:
    opts, args = getopt.getopt(argv,"hap:z:",["project_id=","zone=","all"])
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      usage()
      sys.exit()
    elif opt in ("-p", "--project_id"):
      project_id=arg
    elif opt in ("-z", "--zone"):
      zone=arg
    elif opt in ("-a", "--all"):
      action='all'

  show_arg_info()

  if action == "all":
    list_all_instances(project_id)
  else:
    list_instances(project_id,zone)

  
#
# Main
#
if __name__ == "__main__":
  """ 
  Read arguments from command line 
  """
  script_name = sys.argv[0]
  main(sys.argv[1:]) 