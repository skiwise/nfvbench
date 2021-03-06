# Copyright 2016 Cisco Systems, Inc.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#


class Interface(object):
    """A class to hold the RX and TX counters for a virtual or physical interface."""

    def __init__(self, name, device, tx_packets, rx_packets):
        """Create a new interface instance."""
        self.name = name
        self.device = device
        self.packets = {
            'tx': tx_packets,
            'rx': rx_packets
        }

    def set_packets(self, tx, rx):
        """Set tx and rx counters for this interface."""
        self.packets = {
            'tx': tx,
            'rx': rx
        }

    def set_packets_diff(self, tx, rx):
        """Subtract current counters from new set of counters and update with results."""
        self.packets = {
            'tx': tx - self.packets['tx'],
            'rx': rx - self.packets['rx'],
        }

    def is_no_op(self):
        """Check if this interface is a no-opn interface."""
        return self.name is None

    def get_packet_count(self, traffic_type):
        """Get packet count for given direction."""
        return self.packets.get(traffic_type, 0)

    @staticmethod
    def no_op():
        """Return an interface that doe snot pass any traffic."""
        return Interface(None, None, 0, 0)


class Network(object):
    """This class holds all interfaces that make up a logical neutron network.

    A loopback packet path has exactly 2 networks.
    The first interface is always one of the 2 traffic gen interface.
    Subsequent interfaces are sorted along the path from the TG to the loopback point
    which could be interfaces in a switch, a vswitch or a VM.
    """

    def __init__(self, interfaces=None, reverse=False):
        """Create a network with initial interface list and direction.

        :param interfaces: initial interface list
        :param reverse: specifies the order of interfaces returned by get_interfaces
        """
        if interfaces is None:
            interfaces = []
        self.interfaces = interfaces
        self.reverse = reverse

    def add_interface(self, interface):
        """Add one more interface to this network.

        Order if important as interfaces must be added from traffic generator ports towards then
        looping back device.
        """
        self.interfaces.append(interface)

    def get_interfaces(self):
        """Get interfaces associated to this network.

        Returned interface list is ordered from traffic generator port towards looping device if
        reverse is false. Else returms the list in the reverse order.
        """
        return self.interfaces[::-1] if self.reverse else self.interfaces
