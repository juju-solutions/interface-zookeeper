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
    can get the connection details via the following call:
      * `get_zookeeper_units()` returns a list of (remote address, port) tuples  

  * `{relation_name}.departing` A

  * `{relation_name}.joining` A new Zookeeper unit is added. The charm can call the  `dismiss_joining()` method so that is will not be notified again for the joining of the same unit during a status update.

  * `{relation_name}.departing` A new Zookeeper unit is removed. The charm can call the  `dismiss_departing()` method so that is will not be notified again for the departure of the same unit during a status update.

Example:

```python
@when('zookeeper.connected')
@when_not('zookeeper.available')
def waiting_for_zookeeper(zk):
    hookenv.status_set('waiting', 'Waiting for Zookeeper to become available')


@when('kafka.started', 'zookeeper.departing', 'zookeeper.available')
def reconfigure_kafka_zk_instances_leaving(zkdeparting, zkavailable):
    try:
        zk_units = zkavailable.get_zookeeper_units()
        hookenv.status_set('maintenance', 'Updating Kafka with departing Zookeeper instances ')
        kafka = Kafka(dist_config())
        kafka.configure_kafka(zk_units)
        kafka.restart()
        zkdeparting.dismiss_departing()
        hookenv.status_set('active', 'Ready')
    except:
        hookenv.log("Relation with Zookeeper not established. Stopping Kafka.")        
        kafka = Kafka(dist_config())
        kafka.stop()
        remove_state('kafka.started')
        hookenv.status_set('blocked', 'Waiting for connection to Zookeeper')
```


# Contact Information

- <bigdata@lists.ubuntu.com>
