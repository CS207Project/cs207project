import sys, random, heapq

class _Node:
    def minimum_distance(self, distances):
        minimum = 0.0
        for i in range(len(distances)):
            if distances[i] < self.lower_bounds[i]:
                minimum = max(minimum, self.lower_bounds[i] - distances[i])
            elif distances[i] > self.upper_bounds[i]:
                minimum = max(minimum, distances[i] - self.upper_bounds[i])
        return minimum

    def help_find(self, item, distances, heap, distance):
        d = distance(self.vantage, item)
        new_distances = distances + (d,)
        
        heapq.heappush(heap, (d, 0, self.vantage))
        
        for child in self.children:
            heapq.heappush(heap, (child.minimum_distance(new_distances), 1, child, new_distances))


def _make_node(items, distance, max_children):
    if not items:
        return None

    node = _Node()
    
    node.lower_bounds = [ ]
    node.upper_bounds = [ ]
    for i in range(len(items[0][1])):
        distance_list = [ item[1][i] for item in items ]
        node.lower_bounds.append(min(distance_list))
        node.upper_bounds.append(max(distance_list))
    
    node.vantage = items[0][0]
    items = items[1:]
    
    node.children = [ ]

    if not items:
        return node
        
    items = [ (item[0], item[1]+(distance(node.vantage, item[0]),)) for item in items ]
    
    distances = { }
    for item in items: distances[item[1][-1]] = True
    distance_list = list(distances.keys())
    distance_list.sort()
    n_children = min(max_children, len(distance_list))
    split_points = [ -1 ]
    for i in range(n_children):
        split_points.append(distance_list[(i+1)*(len(distance_list)-1)//n_children])

    for i in range(n_children):
        child_items = [ item for item in items if split_points[i] < item[1][-1] <= split_points[i+1] ]
        child = _make_node(child_items,distance,max_children)
        if child: node.children.append(child)
    
    return node

        
class vptree:
    def __init__(self, items, distance, max_children=2):
        """ items        : list of items to make tree out of
            distance     : function that returns the distance between two items
            max_children : maximum number of children for each node
            
            Using larger max_children will reduce the time needed to construct the tree,
            but may make queries less efficient.
        """
    
        self.distance = distance
        
        items = [ (item, ()) for item in items ]
        random.shuffle(items)
        self.root = _make_node(items, distance, max_children)

    def find(self, item):
        """ Return iterator yielding items in tree in order of distance from supplied item.
        """
    
        if not self.root: return
        
        heap = [ (0, 1, self.root, ()) ]
        
        while heap:
            top = heapq.heappop(heap)
            if top[1]:
                top[2].help_find(item, top[3], heap, self.distance)
            else:
                yield top[2], top[0]
        

    # def distance(a,b):
    #     """ Calculates the Levenshtein distance between a and b.
    #         (from http://hetland.org/python/) """
    #     global comparison_count
    #     comparison_count += 1
        
    #     n, m = len(a), len(b)
    #     if n > m:
    #         # Make sure n <= m, to use O(min(n,m)) space
    #         a,b = b,a
    #         n,m = m,n

    #     current = list(range(n+1))
    #     for i in range(1,m+1):
    #         previous, current = current, [i]+[0]*n
    #         for j in range(1,n+1):
    #             add, delete = previous[j]+1, current[j-1]+1
    #             change = previous[j-1]
    #             if a[j-1] != b[i-1]:
    #                 change = change + 1
    #             current[j] = min(add, delete, change)

    #     return current[n]