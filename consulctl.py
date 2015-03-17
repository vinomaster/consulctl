#!/usr/bin/python

import sys
import time
import getopt
import json
import base64
import requests
import logging

# Global Consul Agent Address
consul_agent_address = 'http://localhost:8500' 

def print_response(result):
    '''Print query results in json format.'''
    jobj = json.loads(result.text)
    for item in jobj:
        if item['Value']:
            item['Value'] = base64.b64decode(item['Value'])
    print json.dumps(jobj, sort_keys=True, indent=4, separators=(',', ': '))

def cluster(plist):
    '''Print json list of cluster members (agents and clients).'''
    r = requests.get(consul_agent_address + '/v1/catalog/nodes')
    print json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': '))

def listkeys(plist):
    '''Print json list of all keys.'''
    r = requests.get(consul_agent_address + '/v1/kv/?recurse')
    print_response(r)
    
def get(plist):
    '''Fetch a specific key and display the value or all details.'''
    key = plist['Key']
    detail = plist['Details']
    r = requests.get(consul_agent_address + '/v1/kv/'+key)
    if detail:
        print_response(r)
    else:
        jobj = json.loads(r.text)
        for item in jobj:
            if item['Value']:
                item['Value'] = base64.b64decode(item['Value'])
            # print("Key[ {0} ] = Value[ {1} ]").format(item['Key'], item['Value'])
            print item['Value']

def set(plist):
    '''Set a key/value pair.'''
    key = plist['Key']
    value = plist['Value']
    r = requests.put(consul_agent_address + '/v1/kv/'+key, data=value)
    print("Key[ {0} ] set to Value[ {1} ]").format(key, value)

# Menu Mode Options with action methods
menu_options = {'Cluster' : cluster,
                'List Keys' : listkeys,
                'Set Key' : set,
                'Get Key Value' : get,
                'Get Key Details' : get,
}

def display_menu():
    '''Display menu to console.'''
    print
    print("-----------------------------")
    print("Consul Service Discovery Menu")
    print("-----------------------------")
    menu_items = sorted(menu_options.keys())
    for index, value in enumerate(menu_items, start=1):
        print("{0} - {1}").format(index, value)
    print("99 Exit")

def command_mode(cmdstr):
    '''Peocess command line options.'''
    try:
        param_list = {}
        if cmdstr[0] == "nodes": 
            cluster(param_list)
        elif cmdstr[0] == "ls":
            listkeys(param_list)
        elif cmdstr[0] == "get":
            if (len(cmdstr) == 3) & (cmdstr[1] == '-d'):
                param_list['Key'] = cmdstr[2]
                param_list['Details'] = True
                get(param_list)
            elif (len(cmdstr) == 2):
                param_list['Key'] = cmdstr[1]
                param_list['Details'] = False
                get(param_list)
            else:
                raise Exception('Improper usage of Get command.')
        elif cmdstr[0] == "set":
            if (len(cmdstr) == 3):
                param_list['Key'] = cmdstr[1]
                param_list['Value'] = cmdstr[2]
                set(param_list)
            else:
                raise Exception('Improper usage of Set command.')
        else:
            raise Exception('Invalid command. Refer to help (-h).')
    except Exception as err:
        # Report error and exit
        logging.error("Error: %s", str(err))

def menu_mode():
    '''Menu mode handler.'''
    flag = 1
    # Establish an infinite loop
    while flag == 1:
        try:
            param_list = {}
            display_menu()
            msg_num = raw_input("Enter number Consul Command: ")
            if not msg_num.isdigit():
               raise TypeError  
            if (msg_num) == "99":
                raise SystemExit
            if (int(msg_num) < 1) or (int(msg_num) > len(menu_options)):
                raise Exception('Enter a valid option')
            print
            menu_items = sorted(menu_options.keys())
            menu_item = menu_items[int(msg_num)-1]
            if menu_item == 'Set Key':
                key_name = raw_input("Enter name of key to set: ")
                key_val = raw_input("Enter value for Key[ " + key_name + " ]: ")
                param_list['Key'] = key_name
                param_list['Value'] = key_val
            elif menu_item == 'Get Key Value':
                key_name = raw_input("Enter name of key to get: ")
                param_list['Key'] = key_name
                param_list['Details'] = False
            elif menu_item == 'Get Key Details':
                key_name = raw_input("Enter name of key to get: ")
                param_list['Key'] = key_name
                param_list['Details'] = True
            menu_options[menu_item](param_list)
        except Exception as err:
            # Report error and proceed
            logging.error("Error: %s. Please try again.", str(err))

def set_agent_address(arg):
    '''Set hostname and port for Consul agent.'''
    global consul_agent_address
    consul_agent_address = arg
    logging.info("Info: Consul Agent Address set to %s.", consul_agent_address)

def usage():
    '''Utility help.'''
    print
    print('ConsulCtl')
    print(' A simple command line utility for Consul Service Discovery.')
    print(' Usage: consulctl.py [-a address | -h | -m | <command> <options>]')
    print('   -a: Set Consul Agent Address (default=http://localhost:8500)')
    print('   -h: Help')
    print('   -m: Menu mode')
    print('   Command mode {nodes, ls, set, get}')
    print('     nodes: Display nodes in cluster')
    print('     ls: List all keys')
    print('     set <key> <value>: Set a key')
    print('     get -d <key>: Get all details for a key')
    print('     get <key>: Get a key value')
    print

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "a:hm")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in sorted(opts):
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ('-m'):
            FORMAT = "%(asctime)-15s [%(module)s:%(lineno)s %(funcName)s] %(message)s"
            logging.basicConfig(format=FORMAT, level=logging.DEBUG)
            menu_mode()
        elif opt in ('-a'):
            set_agent_address(arg)
    if not args:
        logging.info("Error: Please select either Command or Menu Mode.")
        sys.exit(2)
    else:
        FORMAT = "%(asctime)-15s [%(module)s:%(lineno)s %(funcName)s] %(message)s"
        logging.basicConfig(format=FORMAT, level=logging.ERROR)
        command_mode(args)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as err:
        print
        print("ConsulCtl: " + str(err))
        sys.exit()

