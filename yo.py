import random
import time


class Node:
    def __init__(self, median=None, point=None):
        self.point = point
        self.left = None
        self.right = None
        self.median = median


def buildPST(points):
    if not points:
        return None

    # Find point with maximum y value
    max_y_point = max(points, key=lambda p: p[1])

    median = 0

    if len(points) == 2:
        min_y_point = min(points, key=lambda p: p[1])
        median = (max_y_point[0] + min_y_point[0]) // 2

    # Remove it from the list of points
    points.remove(max_y_point)

    # Divide into 2 subsets by x
    mid = len(points) // 2
    if mid >= 1:
        median = (points[mid - 1][0] + points[mid][0]) // 2

    left_points = [point for point in points if point[0] <= median]
    right_points = [point for point in points if point[0] > median]

    # Create nodes
    root = Node(median=median, point=max_y_point)

    # Recursive build
    root.left = buildPST(left_points)
    root.right = buildPST(right_points)

    return root


def PSTSearchLeft(x1, y1, y2, node):
    if node is None:
        return []

    result = []
    # Check condition y1 <= y <= y2
    if y1 <= node.point[1] <= y2:
        # Check condition x >= x1
        if node.point[0] >= x1:
            result.append(node.point)

    # Traverse left subtree x1 <= median
    if x1 <= node.median:
        result.extend(PSTSearchLeft(x1, y1, y2, node.left))

    # Traverse right subtree
    result.extend(PSTSearchLeft(x1, y1, y2, node.right))

    return result


def PSTSearchRight(x2, y1, y2, node):
    if node is None:
        return []

    result = []
    # Check condition y1 <= y <= y2
    if y1 <= node.point[1] <= y2:
        # Check condition x <= x2
        if node.point[0] <= x2:
            result.append(node.point)

    # Traverse left subtree
    result.extend(PSTSearchRight(x2, y1, y2, node.left))

    # Traverse right subtree if x2 > median
    if x2 > node.median:
        result.extend(PSTSearchRight(x2, y1, y2, node.right))

    return result


def generate_points(num_points, x_range=(0, 100), y_range=(0, 100)):
    return [
        (random.randint(*x_range), random.randint(*y_range)) for _ in range(num_points)
    ]


def printTree(node, level=0):
    if node is not None:
        printTree(node.right, level + 1)  # Print the right tree
        print(" " * 4 * level + f"-> {node.point}")  # Node value
        printTree(node.left, level + 1)  # Print the left tree


def PSTRangeSearch(x1, x2, y1, y2, node):
    """
    Perform a four-sided range search in a Priority Search Tree (PST).
    Args:
        x1: Lower bound for x-coordinate
        x2: Upper bound for x-coordinate
        y1: Lower bound for y-coordinate
        y2: Upper bound for y-coordinate
        node: The current node in the PST
    Returns:
        A list of points (x, y) that satisfy the range conditions.
    """
    # Base case: If the node is None, return an empty list
    if node is None:
        return []
    # Check if the point at the node satisfies the x-range [x1, x2]
    result = []
    if x1 <= node.point[0] and node.point[0] <= x2:
        # If the y-coordinate of the point at the node is outside the range [y1, y2], exclude this node
        if y1 <= node.point[1] and node.point[1] <= y2:
            result.append(node.point)
        result.extend(PSTSearchLeft(x1, y1, y2, node.left))
        result.extend(PSTSearchRight(x2, y1, y2, node.right))
    # Recursively search in left and right subtrees based on the x-range
    elif node.point[0] < x1:  # Check right subtree
        result.extend(PSTRangeSearch(x1, x2, y1, y2, node.right))
    else:  # Check right subtree
        result.extend(PSTRangeSearch(x1, x2, y1, y2, node.left))
    return result


points = [(60, 75), (90, 5), (50, 10), (85, 15), (5, 45), (35, 40), (80, 65), (25, 35)]
points.sort(key=lambda p: p[0])  # Sort by x

# Build Priority Search Tree
pst = buildPST(points)
x1, x2, y1, y2 = 10, 60, 10, 50

# Print the tree
print("Priority Search Tree:")
printTree(pst)

range_result = PSTRangeSearch(x1, x2, y1, y2, pst)
print("Range result", range_result)


