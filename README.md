# Overview

This interface layer handles the communication between Apache Zookeeper and its clients.
The provider part is the Zookeeper service providing a host name and a port.


# Usage

## Provides

Charms providing the Zookeeper service make use of the provides interface.

This interface layer will set the following states, as appropriate:

  * `{relation_name}.connected`   The relation to a client has been
    established, though the service list may not be available yet. At this point the
    provider should broadcast the connection properties using:
      * `send_port(port)`

  * `{relation_name}.available`   The connection to the agent is now available and correctly setup.


Here is an example of using this interface is:

```python
@when('zookeeper.installed', 'zkclient.connected')
def zk_client_connected(client):
    config = dist_config()
    port = config.port('zookeeper')
    client.send_port(port)
```


## Requires

A client charm makes use of the requires part of the interface to connect to Zookeeper.

This interface layer will set the following states, as appropriate:

  * `{relation_name}.connected` The charm has connected to Zookeeper. 
    At this point the requires interface waits for connection details (port, IP).

  * `{relation_name}.available` The connection has been established, and the client charm
    can get the connection details via the following calls:
      * `get_zookeeper_ip()`
      * `get_zookeeper_port()`

Example:

```python
@when('zookeeper.connected')
@when_not('zookeeper.available')
def waiting_for_zookeeper(zk):
    hookenv.status_set('waiting', 'Waiting for Zookeeper to become available')


@when('zookeeper.available')
def configure_client(zk):
    port = zk.get_zookeeper_port()
    ip = zk.get_zookeeper_ip()
```


# Contact Information

- <bigdata@lists.ubuntu.com>
