# consulctl
Basic command line utility for [Consul.io](http://www.consul.io) Key/Value Store. 
It can be used in scripts or for administrators to explore a Consul cluster.

## Dependencies

```
$ pip install requests
```

## Usage

```
$ python consulctl.py -h

A simple command line utility for Consul Service Discovery.
 Usage: consulctl.py [-a address | -h | -m | <command> <options>]
   -a: Set Consul Agent Address (default=http://localhost:8500)
   -h: Help
   -m: Menu mode
   Command mode {nodes, ls, set, get}
     nodes: Display nodes in cluster
     ls: List all keys
     set <key> <value>: Set a key
     get -d <key>: Get all details for a key
     get <key>: Get a key value
```

### Menu Mode

```
$ python consulctl.py -m
-----------------------------
Consul Service Discovery Menu
-----------------------------
1 - Cluster
2 - Get Key Details
3 - Get Key Value
4 - List Keys
5 - Set Key
99 Exit
Enter number Consul Command: __
```

### Command Mode

#### Setting Key Values

Set a value on the `/foo/bar` key:

```
$ python consulctl.py set /foo/bar "Hello world"
Hello world
```

#### Retrieving a key value

Get the current value for a single key in cluster:

```
$ python consulctl.py get /foo/bar
Hello world
```

Get the current value for a single key a cluster with a specific agent address:

```
$ python consulctl.py -a http://172.17.41.28:8500 get /foo/bar
Hello world
```

Get the value of a key with additional metadata in json format:

```
$ python consulctl.py get -d /foo/bar
[
    {
        "CreateIndex": 1288,
        "Flags": 0,
        "Key": "foo",
        "LockIndex": 0,
        "ModifyIndex": 1526,
        "Value": "Hello world"
    }
]
```

#### Listing a directory

Recursively explore the key store using the `ls` command

```
$ python consulctl.py ls
[
    {
        "CreateIndex": 3208,
        "Flags": 0,
        "Key": "Number",
        "LockIndex": 0,
        "ModifyIndex": 3208,
        "Value": "2"
    },
    {
        "CreateIndex": 2796,
        "Flags": 0,
        "Key": "Letter",
        "LockIndex": 0,
        "ModifyIndex": 2796,
        "Value": "A"
    }
]
```

#### Deleting a key 

**Note**: *This feature is currently unsupported*.

Delete a key:

```
$ python consulctl.py rm /foo/bar
```

Delete an empty directory or a key-value pair

```
$ python consulctl.py rmdir /path/to/dir
```

## Project Details

### Motivation

Inspired by [etcdctl](https://github.com/coreos/etcd/tree/master/etcdctl) which is a command line client for [etcd](https://github.com/coreos/etcd). 

### Installation

```consulctl``` is a Python utility. It can be installed directly from [GitHub](https://github.com/vinomaster/consulctl.git).

### Dependencies

```consulctl``` has the following runtime dependences:

1. Python 2.7.6
2. [python-consul](http://python-consul.readthedocs.org/en/latest/) 
```
$ pip install python-consul
```

### License

```consulctl``` is under the Apache 2.0 license. See the [LICENSE](https://github.com/coreos/consulctl/blob/master/LICENSE) file for details.

### To Do

1. Support for Python3; Possible issues with raw_input().
2. Add UpdateKey support
3. Add DeleteKey support
4. Expand listing support based on key paths
