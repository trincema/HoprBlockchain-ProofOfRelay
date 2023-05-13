import api_object_model.node as node
import logging

logger = logging.getLogger('test_node')

def test_peer_id():
    nodeInstance = node.Node()
    peerId1 = nodeInstance.get_peer_id(1)
    peerId2 = nodeInstance.get_peer_id(2)
    peerId3 = nodeInstance.get_peer_id(3)
    peerId4 = nodeInstance.get_peer_id(4)
    peerId5 = nodeInstance.get_peer_id(5)
    assert peerId1.startswith("16U")
    assert peerId2.startswith("16U")
    assert peerId3.startswith("16U")
    assert peerId4.startswith("16U")
    assert peerId5.startswith("16U")

def test_last_seen():
    nodeInstance = node.Node()
    for nodeIndex in range(5, 6):
        for announcedNodeIndex in range(1, 6):
            lastSeen = nodeInstance.get_announced_last_seen(nodeIndex, announcedNodeIndex)
            print('node {0} announcedNode {1} lastSeen: {2}'.format(nodeIndex, announcedNodeIndex, lastSeen))