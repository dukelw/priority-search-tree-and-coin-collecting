class TreeNode:
    def __init__(self, point=None):
        self.point = point
        self.left = None
        self.right = None
        self.priority_tree = None


class Node:
    def __init__(self, median=None, point=None):
        self.point = point
        self.left = None
        self.right = None
        self.median = median


def build_balanced_bst(points):
    """
    Build a balanced binary search tree (BST) from the given sorted points.
    Args:
        points (list of tuples): List of points sorted by x-coordinate.
    Returns:
        TreeNode: Root of the balanced BST.
    """
    if not points:
        return None

    mid = len(points) // 2
    root = TreeNode(points[mid])
    root.left = build_balanced_bst(points[:mid])
    root.right = build_balanced_bst(points[mid + 1 :])

    return root


def build_pst(points):
    """
    Build a Priority Search Tree (PST) from the given points.
    Args:
        points (list of tuples): List of points.
    Returns:
        Node: Root of the PST.
    """
    if not points:
        return None

    max_y_point = max(points, key=lambda p: p[1])
    points.remove(max_y_point)

    mid = len(points) // 2
    median = max_y_point[0]
    if mid >= 1:
        median = (points[mid - 1][0] + points[mid][0]) // 2

    left_points = points[: mid + 1]
    right_points = points[mid + 1 :]

    root = Node(median=median, point=max_y_point)
    root.left = build_pst(left_points)
    root.right = build_pst(right_points)

    return root


def augment_with_pst(bst):
    """
    Augment a balanced BST with Priority Search Trees (PSTs) at each node.
    Args:
        bst (TreeNode): Root of the balanced BST.
    Returns:
        TreeNode: Root of the augmented Priority Range Tree.
    """
    if bst is None:
        return None

    # Collect all points in the subtree
    points = collect_points(bst)
    bst.priority_tree = build_pst(points)

    # Recur for left and right children
    augment_with_pst(bst.left)
    augment_with_pst(bst.right)

    return bst


def collect_points(node):
    """
    Collect all points in the subtree rooted at the given node.
    Args:
        node (TreeNode): Root of the subtree.
    Returns:
        list of tuples: List of points in the subtree.
    """
    if node is None:
        return []

    return collect_points(node.left) + [node.point] + collect_points(node.right)


def print_tree(node, level=0):
    """
    Print the Priority Range Tree.
    Args:
        node (TreeNode): Root of the tree.
        level (int): Current level in the tree (used for indentation).
    """
    if node is not None:
        print_tree(node.right, level + 1)
        print(" " * 4 * level + f"-> {node.point}, PST: {node.priority_tree}")
        print_tree(node.left, level + 1)


# Example Usage
points = [(3, 5), (4, 2), (5, 4), (1, 1), (2, 3)]
points.sort(key=lambda p: p[0])  # Sort by x-coordinate

# Build a balanced BST
bst = build_balanced_bst(points)

# Augment with Priority Search Trees
priority_range_tree = augment_with_pst(bst)

# Print the Priority Range Tree
print_tree(priority_range_tree)


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
        result.extend(PSTSearch(x1, y1, y2, node.left))
        result.extend(PSTSearch(x2, y1, y2, node.right))

    # Recursively search in left and right subtrees based on the x-range
    elif node.point[0] < x1:  # Check right subtree
        result.extend(PSTRangeSearch(x1, x2, y1, y2, node.right))
    else:  # Check right subtree
        result.extend(PSTRangeSearch(x1, x2, y1, y2, node.left))

    return result


x1, x2, y1, y2 = 10, 60, 20, 50
range_result = PSTRangeSearch(x1, x2, y1, y2, priority_range_tree)
print("Range result", range_result)
