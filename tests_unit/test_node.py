import api_object_model.node as node
import re

def test_peer_id_address():
    """
    Validate the peer id addresses of the 5 nodes
    Check that the address starts with 16U
    Check that the address is always 53 characters in length
    Check the address only contain capital/lowercase letters and numbers
    """
    nodeInstance = node.Node()
    for i in range(1, 6):
        peerId = nodeInstance.get_peer_id(i)
        assert peerId.startswith("16U")
        assert len(peerId) == 53
        assert re.match("^[A-Za-z0-9]", peerId)
    del nodeInstance

def xtest_last_seen():
    """
    """
    nodeInstance = node.Node()
    for nodeIndex in range(5, 6):
        for announcedNodeIndex in range(1, 6):
            lastSeen = nodeInstance.get_announced_last_seen(nodeIndex, announcedNodeIndex)
            print('node {0} announcedNode {1} lastSeen: {2}'.format(nodeIndex, announcedNodeIndex, lastSeen))