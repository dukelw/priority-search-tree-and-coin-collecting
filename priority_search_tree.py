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


def PSTSearch(x1, x2, y1, node):
    if node is None:
        return []

    if node.point[1] < y1:
        return []

    result = []
    if x1 <= node.point[0] <= x2:
        result.append(node.point)

    if x1 <= node.median:
        result.extend(PSTSearch(x1, x2, y1, node.left))
    if x2 > node.median:
        result.extend(PSTSearch(x1, x2, y1, node.right))

    return result


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
        if node.left.point[0] < x2:
            result.extend(PSTSearchLeft(x1, y1, y2, node.left))
        if node.right.point[0] > x1:
            result.extend(PSTSearchRight(x2, y1, y2, node.right))
    # Recursively search in left and right subtrees based on the x-range
    elif node.point[0] < x1:  # Check right subtree
        result.extend(PSTRangeSearch(x1, x2, y1, y2, node.right))
    else:  # Check right subtree
        result.extend(PSTRangeSearch(x1, x2, y1, y2, node.left))
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


def test_search():
    import matplotlib.pyplot as plt

    def test_and_measure_with_queries(points, queries):
        print(f"Testing with {len(points)} points...")

        points.sort(key=lambda p: p[0])

        pst = buildPST(points)

        search_times = []
        range_search_times = []
        search_results = []
        range_search_results = []

        for query in queries:
            x1, x2, y1, y2 = query

            start_time = time.perf_counter()
            result = PSTSearch(x1, x2, y1, pst)
            search_time = time.perf_counter() - start_time

            start_time = time.perf_counter()
            range_result = PSTRangeSearch(x1, x2, y1, y2, pst)
            range_search_time = time.perf_counter() - start_time

            search_times.append(search_time)
            range_search_times.append(range_search_time)
            search_results.append(len(result))
            range_search_results.append(len(range_result))

            print(f"Query: x1={x1}, x2={x2}, y1={y1}, y2={y2}")
            if len(result) < 10 and len(range_result) < 10:
                print(f"Search result: {result}")
                print(f"Range search result: {range_result}")
            print(f"Search time: {search_time:.6f} seconds, Results: {len(result)}")
            print(
                f"Range search time: {range_search_time:.6f} seconds, Results: {len(range_result)}\n"
            )

        return search_times, range_search_times, search_results, range_search_results

    def plot_results(queries, search_times, range_search_times):
        query_labels = [f"({q[0]}, {q[1]}, {q[2]}, {q[3]})" for q in queries]

        plt.figure(figsize=(10, 6))

        # Plot search times
        plt.plot(
            query_labels, search_times, label="Search Time (PSTSearch)", marker="o"
        )
        plt.plot(
            query_labels,
            range_search_times,
            label="Range Search Time (PSTRangeSearch)",
            marker="s",
        )

        plt.xlabel("Queries (x1, x2, y1, y2)")
        plt.ylabel("Time (seconds)")
        plt.title("Search Times for PSTSearch and PSTRangeSearch")
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        plt.tight_layout()
        plt.show()

    points = [
        (60, 75),
        (90, 5),
        (50, 10),
        (85, 15),
        (5, 45),
        (35, 40),
        (80, 65),
        (25, 35),
    ]

    queries = [
        (10, 60, 10, 40),
        (10, 30, 5, 20),
        (5, 20, 20, 50),
        (0, 100, 0, 100),
    ]

    search_times, range_search_times, search_results, range_search_results = (
        test_and_measure_with_queries(points, queries)
    )

    # points = generate_points(40000)
    # queries = [
    #     (40, 60, 0, 100),
    #     (0, 100, 80, 100),
    #     (40, 60, 70, 90),
    #     (0, 100, 60, 100),
    #     (0, 100, 0, 100),
    # ]

    # search_times, range_search_times, search_results, range_search_results = (
    #     test_and_measure_with_queries(points, queries)
    # )
    # plot_results(queries, search_times, range_search_times)


def test_build():
    def test_and_measure(points):
        print(f"Testing with {len(points)} points...")

        points.sort(key=lambda p: p[0])

        # Build time
        start_time = time.perf_counter()
        pst = buildPST(points)
        if len(points) < 10:
            printTree(pst)
        build_time = time.perf_counter() - start_time
        print(f"Build PST time: {build_time:.6f} seconds")

    # Generate test data and run tests
    points_5 = [(50, 10), (85, 15), (5, 45), (35, 40), (80, 65)]
    points_8 = [
        (60, 75),
        (90, 5),
        (50, 10),
        (85, 15),
        (5, 45),
        (35, 40),
        (80, 65),
        (25, 35),
    ]
    points_100 = generate_points(100)
    points_2000 = generate_points(2000)
    points_40000 = generate_points(40000)

    test_and_measure(points_5)
    test_and_measure(points_8)
    test_and_measure(points_100)
    test_and_measure(points_2000)
    test_and_measure(points_40000)


def basic_test():
    points = [
        (60, 75),
        (90, 5),
        (50, 10),
        (85, 15),
        (5, 45),
        (35, 40),
        (80, 65),
        (25, 35),
    ]
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


# Call
# test_build()
test_search()
