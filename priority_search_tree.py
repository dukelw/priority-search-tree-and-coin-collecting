class Node:
    def __init__(self, median=None, point=None):
        self.point = point
        self.left = None
        self.right = None
        self.median = median


def buildPST(points):
    if not points:
        return None

    # Find point with maximum  value
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
    print("Median", median)

    left_points = [point for point in points if point[0] <= median]
    right_points = [point for point in points if point[0] > median]

    # Create nodes
    root = Node(median=median, point=max_y_point)

    # Recursional build
    root.left = buildPST(left_points)
    root.right = buildPST(right_points)

    return root


def printTree(node, level=0):
    if node is not None:
        printTree(node.right, level + 1)  # Print the right tree
        print(" " * 4 * level + f"-> {node.point}")  # Node value
        printTree(node.left, level + 1)  # Print the left tree


def PSTSearch(x1, x2, y1, node):
    """
    Perform a three-sided range search in a Priority Search Tree (PST).
    Args:
        x1: Lower bound for x-coordinate
        x2: Upper bound for x-coordinate
        y1: Upper bound for y-coordinate
        node: The current node in the PST
    Returns:
        A list of points (x, y) that satisfy the range conditions.
    """
    # Base case: If the node is None, return an empty list
    if node is None:
        return []

    # If the y-coordinate of the point at the node is greater than y1, exclude this node
    if node.point[1] < y1:
        return []

    # Check if the point at the node satisfies the x-range [x1, x2]
    result = []
    if x1 <= node.point[0] and node.point[0] <= x2:
        result.append(node.point)

    # Check the left and right subtrees based on the x-coordinate at this node
    # Sometimes the medium is calculated by plus the left and right values so the node values is not the correct medium value
    if x1 <= node.median:
        result.extend(PSTSearch(x1, x2, y1, node.left))
    if x2 > node.median:
        result.extend(PSTSearch(x1, x2, y1, node.right))

    return result


def PSTRangeSearch(x1, x2, y1, y2, node):
    """
    Perform a three-sided range search in a Priority Search Tree (PST).
    Args:
        x1: Lower bound for x-coordinate
        x2: Upper bound for x-coordinate
        y1: Upper bound for y-coordinate
        node: The current node in the PST
    Returns:
        A list of points (x, y) that satisfy the range conditions.
    """
    # Base case: If the node is None, return an empty list
    if node is None:
        return []

    # Check if the point at the node satisfies the x-range [x1, x2]
    result = []
    if (
        x1 <= node.point[0]
        and node.point[0] <= x2
        and node.point[1] >= y1
        and node.point[1] <= y2
    ):
        result.append(node.point)

    # Check the left and right subtrees based on the x-coordinate at this node
    # Sometimes the medium is calculated by plus the left and right values so the node values is not the correct medium value
    if x1 <= node.median:
        result.extend(PSTRangeSearch(x1, x2, y1, y2, node.left))
    if node.median <= x2:
        result.extend(PSTRangeSearch(x1, x2, y1, y2, node.right))

    return result


# def PSTRangeSearch(x1, x2, y1, y2, node):
#     """
#     Perform a four-sided range search in a Priority Search Tree (PST).
#     Args:
#         x1: Lower bound for x-coordinate
#         x2: Upper bound for x-coordinate
#         y1: Lower bound for y-coordinate
#         y2: Upper bound for y-coordinate
#         node: The current node in the PST
#     Returns:
#         A list of points (x, y) that satisfy the range conditions.
#     """
#     # Base case: If the node is None, return an empty list
#     if node is None:
#         return []

#     # Check if the point at the node satisfies the x-range [x1, x2]
#     result = []
#     if x1 <= node.point[0] and node.point[0] <= x2:
#         # If the y-coordinate of the point at the node is outside the range [y1, y2], exclude this node
#         if y1 <= node.point[1] and node.point[1] <= y2:
#             result.append(node.point)
#         result.extend(PSTSearch(x1, y1, y2, node.left))
#         result.extend(PSTSearch(x2, y1, y2, node.right))

#     # Recursively search in left and right subtrees based on the x-range
#     elif node.point[0] < x1:  # Check right subtree
#         result.extend(PSTRangeSearch(x1, x2, y1, y2, node.right))
#     else:  # Check right subtree
#         result.extend(PSTRangeSearch(x1, x2, y1, y2, node.left))

#     return result


# points = [(3, 5), (4, 2), (5, 4), (1, 1), (2, 3)]
points = [(50, 10), (85, 15), (5, 45), (35, 40), (80, 65)]
# points = [(24, 28), (35, 39), (36, 43), (42, 13), (68, 90), (56, 70), (20, 96), (5, 55)]
# points = [(60, 75), (90, 5), (50, 10), (85, 15), (5, 45), (35, 40), (80, 65), (25, 35)]
# points = [(50, 10), (85, 15), (35, 45), (35, 40), (80, 65)]
points.sort(key=lambda p: p[0])  # Sort by x

# Build Priority Search Tree
pst = buildPST(points)
x1, x2, y1, y2 = 10, 60, 10, 50
result = PSTSearch(x1, x2, y1, pst)
print("Points in range:", result)

# Print the tree
print("Priority Search Tree:")
printTree(pst)

range_result = PSTRangeSearch(x1, x2, y1, y2, pst)
print("Range result", range_result)
