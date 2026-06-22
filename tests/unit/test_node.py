import pytest
from src.huffman.node import Node

@pytest.mark.unit
def test_create_leaf_node():
    node = Node(byte_val=ord('a'), freq=5)
    assert node.byte_val == ord('a')
    assert node.freq == 5
    assert node.left is None
    assert node.right is None

@pytest.mark.unit
def test_create_internal_node():
    left = Node(byte_val=ord('a'), freq=2)
    right = Node(byte_val=ord('b'), freq=3)
    node = Node(byte_val=None, freq=5, left=left, right=right)
    
    assert node.byte_val is None
    assert node.freq == 5
    assert node.left is left
    assert node.right is right

@pytest.mark.unit
def test_node_comparison():
    node1 = Node(byte_val=ord('a'), freq=2)
    node2 = Node(byte_val=ord('b'), freq=5)
    
    assert node1 < node2
    assert not (node2 < node1)

@pytest.mark.unit
def test_node_equality():
    node1 = Node(byte_val=ord('a'), freq=2)
    node2 = Node(byte_val=ord('a'), freq=2)
    
    assert node1 == node2
    assert node1 is not node2
