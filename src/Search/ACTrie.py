from collections import deque

class ACTrieNode:

        def __init__(self):
                self.children = {}
                self.output = [] # List to store patterns that end at this node
                self.fail_link = None # Pointer to the failure link node
        
class ACTrie:
        def __init__(self):
                self.root = ACTrieNode()
        
        def insert(self, pattern):
                node = self.root
                for char in pattern:
                        if char not in node.children:
                                node.children[char] = ACTrieNode()
                        node = node.children[char]
                node.output.append(pattern)
        
        def build_failure_links(self):

                # we perform a BFS to build the fail links
                queue = deque()
                
                # First depth failure links
                for child in self.root.children.values():
                        child.fail_link = self.root
                        queue.append(child)
                
                while queue:
                        current_node = queue.popleft()
                        
                        for char, child_node in current_node.children.items():
                                
                                fail_node = current_node.fail_link
                                
                                while fail_node is not None and char not in fail_node.children:
                                        fail_node = fail_node.fail_link
                                
                                if fail_node is None:
                                        child_node.fail_link = self.root
                                else:
                                        child_node.fail_link = fail_node.children[char]
                                        child_node.output.extend(child_node.fail_link.output)
                                
                                queue.append(child_node)