from .messages_templates import MessagesTemplates

def test_case1():
    """
    Test case 1: Test send message directly from Node1 to Node2 (no hops)
    """
    # Define test data for this scenario
    senderNode = 1
    receiverNode = 2
    testMessage = "Hello from future"
    expectedEncodedMessage = "217,145,72,101,108,108,111,32,102,114,111,109,32,102,117"
    visitationPath = [[1, 2]]

    # Call the common template and feed it with the prepared test data
    messagesTemplate = MessagesTemplates()
    messagesTemplate.template1(senderNode, receiverNode, testMessage, expectedEncodedMessage, visitationPath)

def test_case2():
    """
    Test case 2: Test send message from Node1 to Node2 with one defined hop
    """
    # Define test data for this scenario
    senderNode = 1
    receiverNode = 2
    testMessage = "Hello from future"
    expectedEncodedMessage = "217,145,72,101,108,108,111,32,102,114,111,109,32,102,117"
    visitationPath = [[1, 3], [3, 2]]
    path = [3]

    # Call the common template and feed it with the prepared test data
    messagesTemplate = MessagesTemplates()
    messagesTemplate.template1(senderNode, receiverNode, testMessage, expectedEncodedMessage, visitationPath, path)

def test_case3():
    """
    Test case 3: Test send message from Node1 to Node2 with one defined hop and a random hop
    Note: the random hop has to be ignored in this case
    """
    # Define test data for this scenario
    senderNode = 1
    receiverNode = 2
    testMessage = "Hello from future"
    expectedEncodedMessage = "217,145,72,101,108,108,111,32,102,114,111,109,32,102,117"
    visitationPath = [[1, 3], [3, 2]]
    path = [3]
    hops = 1

    # Call the common template and feed it with the prepared test data
    messagesTemplate = MessagesTemplates()
    messagesTemplate.template1(senderNode, receiverNode, testMessage, expectedEncodedMessage, visitationPath, path, hops)

def test_case4():
    """
    Test case 4: Test send message from Node1 to Node2 with one random hop and no defined hop
    TODO - Here the tricky part is to extend the template to check which node from the other 3 nodes is visited
    """
    pass
