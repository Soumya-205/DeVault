import hashlib

class ConsistentHash:
    def __init__(self,replicas=3):
        """
        replicas=how many virtual nodes per real node.
        More replicas=more even distribution
        """
        self.replicas=replicas
        self.ring={}
        self.sorted_keys=[]

    def _hash(self,key):
        """Convert any string to a position on the ring (0 to 2^32)."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node):
        """Add a node to the ring with multiple virtual positions."""
        for i in range(self.replicas):
            virtual_key=f"{node}:{i}"
            position=self._hash(virtual_key)
            self.ring[position]=node
            self.sorted_keys.append(position)
        self.sorted_keys.sort()

    def remove_node(self, node):
        """Remove a node and all its virtual positions."""
        for i in range(self.replicas):
            virtual_key=f"{node}:{i}"
            position=self._hash(virtual_key)
            del self.ring[position]
            self.sorted_keys.remove(position)

    def get_node(self, key):
        """Finding which node owns this key."""
        if not self.ring:
            return None
        
        position=self._hash(key)

        #Going clockwise to find the next node
        for node_position in self.sorted_keys:
            if position<=node_position:
                return self.ring[node_position]
        
        #If we passed all nodes, wrap around to the first one
        return self.ring[self.sorted_keys[0]]