import api_object_model.node as node
import logging

logger = logging.getLogger('test_node')

def test_last_seen():
    nodeInstance = node.Node()
    for nodeIndex in range(5, 6):
        for announcedNodeIndex in range(1, 6):
            lastSeen = nodeInstance.get_announced_last_seen(nodeIndex, announcedNodeIndex)
            print('node {0} announcedNode {1} lastSeen: {2}'.format(nodeIndex, announcedNodeIndex, lastSeen))