"""
Seed data loader — populates the database with sample subjects, topics,
questions, a demo student, and a demo admin account.

All data here is synthetic, used for initial testing and demonstration.
"""

from sqlalchemy.orm import Session
from models import Subject, Topic, Question, Student
from auth import hash_password


def seed_database(db: Session):
    """Populate database with sample data if empty."""

    # Skip if data already exists
    if db.query(Subject).count() > 0:
        return

    print("[*] Seeding database with sample data...")

    # ── Create Admin & Demo Student ───────────────────────────────────

    admin = Student(
        name="Admin User",
        email="admin@example.com",
        password_hash=hash_password("admin123"),
        is_admin=True,
    )
    demo_student = Student(
        name="Demo Student",
        email="student@example.com",
        password_hash=hash_password("student123"),
        is_admin=False,
    )
    db.add_all([admin, demo_student])
    db.flush()

    # ── Subject 1: Data Structures & Algorithms ──────────────────────

    dsa = Subject(name="Data Structures & Algorithms", description="Fundamental data structures and algorithmic techniques")
    db.add(dsa)
    db.flush()

    topics_dsa = [
        ("Arrays & Strings", 2),
        ("Linked Lists", 3),
        ("Stacks & Queues", 2),
        ("Trees & Binary Search Trees", 4),
        ("Sorting Algorithms", 3),
        ("Dynamic Programming", 5),
    ]

    dsa_topic_objs = {}
    for name, diff in topics_dsa:
        t = Topic(subject_id=dsa.id, name=name, difficulty=diff)
        db.add(t)
        db.flush()
        dsa_topic_objs[name] = t

    # ── Subject 2: Artificial Intelligence ───────────────────────────

    ai_subj = Subject(name="Artificial Intelligence", description="Core AI concepts including search, logic, and learning")
    db.add(ai_subj)
    db.flush()

    topics_ai = [
        ("Search Algorithms", 3),
        ("Heuristic Functions", 3),
        ("Constraint Satisfaction Problems", 4),
        ("Knowledge Representation", 4),
        ("Machine Learning Basics", 3),
        ("Neural Networks", 5),
    ]

    ai_topic_objs = {}
    for name, diff in topics_ai:
        t = Topic(subject_id=ai_subj.id, name=name, difficulty=diff)
        db.add(t)
        db.flush()
        ai_topic_objs[name] = t

    # ── Subject 3: Database Management Systems ───────────────────────

    dbms = Subject(name="Database Management Systems", description="Relational databases, SQL, and database design")
    db.add(dbms)
    db.flush()

    topics_dbms = [
        ("SQL Basics", 2),
        ("Normalization", 3),
        ("Transactions & Concurrency", 4),
        ("Indexing & Query Optimization", 4),
    ]

    dbms_topic_objs = {}
    for name, diff in topics_dbms:
        t = Topic(subject_id=dbms.id, name=name, difficulty=diff)
        db.add(t)
        db.flush()
        dbms_topic_objs[name] = t

    # ── Questions: Data Structures & Algorithms ──────────────────────

    questions = []

    # Arrays & Strings
    t = dsa_topic_objs["Arrays & Strings"]
    questions.extend([
        Question(topic_id=t.id, text="What is the time complexity of accessing an element in an array by index?", option_a="O(1)", option_b="O(n)", option_c="O(log n)", option_d="O(n²)", correct_option="A", difficulty=1),
        Question(topic_id=t.id, text="Which operation is most expensive in an unsorted array?", option_a="Access", option_b="Search", option_c="Insertion at end", option_d="Reading length", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="What is the space complexity of reversing a string in-place?", option_a="O(n)", option_b="O(1)", option_c="O(log n)", option_d="O(n²)", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="In a 2D array of size m×n, what is the total number of elements?", option_a="m + n", option_b="m × n", option_c="m²", option_d="2(m+n)", correct_option="B", difficulty=1),
        Question(topic_id=t.id, text="Which algorithm is most efficient for finding a pair with a given sum in a sorted array?", option_a="Brute force O(n²)", option_b="Two-pointer O(n)", option_c="Binary search O(n log n)", option_d="Hashing O(n²)", correct_option="B", difficulty=3),
    ])

    # Linked Lists
    t = dsa_topic_objs["Linked Lists"]
    questions.extend([
        Question(topic_id=t.id, text="What is the time complexity of inserting at the beginning of a singly linked list?", option_a="O(n)", option_b="O(1)", option_c="O(log n)", option_d="O(n²)", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Which pointer(s) does a doubly linked list node contain?", option_a="Only next", option_b="Only prev", option_c="Both next and prev", option_d="None", correct_option="C", difficulty=1),
        Question(topic_id=t.id, text="How do you detect a cycle in a linked list efficiently?", option_a="Use a hash set", option_b="Floyd's cycle detection (slow/fast pointers)", option_c="Reverse the list", option_d="Both A and B", correct_option="D", difficulty=3),
        Question(topic_id=t.id, text="What is the time complexity to delete a node at position k in a singly linked list?", option_a="O(1)", option_b="O(k)", option_c="O(n)", option_d="O(log n)", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Which is NOT an advantage of linked lists over arrays?", option_a="Dynamic size", option_b="Ease of insertion/deletion", option_c="Random access in O(1)", option_d="No memory waste", correct_option="C", difficulty=2),
    ])

    # Stacks & Queues
    t = dsa_topic_objs["Stacks & Queues"]
    questions.extend([
        Question(topic_id=t.id, text="Which principle does a stack follow?", option_a="FIFO", option_b="LIFO", option_c="Priority-based", option_d="Random access", correct_option="B", difficulty=1),
        Question(topic_id=t.id, text="What data structure is used to implement function call recursion?", option_a="Queue", option_b="Stack", option_c="Array", option_d="Linked list", correct_option="B", difficulty=1),
        Question(topic_id=t.id, text="Which application does NOT typically use a queue?", option_a="BFS traversal", option_b="Print spooling", option_c="Undo operations", option_d="CPU scheduling", correct_option="C", difficulty=2),
        Question(topic_id=t.id, text="What is the time complexity of push and pop operations in a stack implemented using a linked list?", option_a="O(n) each", option_b="O(1) each", option_c="O(log n) each", option_d="O(1) push, O(n) pop", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="A circular queue solves which problem of a linear queue?", option_a="Memory overflow", option_b="Wasted space after dequeue", option_c="Stack overflow", option_d="Sorting", correct_option="B", difficulty=3),
    ])

    # Trees & BST
    t = dsa_topic_objs["Trees & Binary Search Trees"]
    questions.extend([
        Question(topic_id=t.id, text="What is the maximum number of nodes at level k in a binary tree?", option_a="k", option_b="2^k", option_c="2k", option_d="k²", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="In a Binary Search Tree, the left subtree of a node contains:", option_a="Values greater than the node", option_b="Values equal to the node", option_c="Values less than the node", option_d="Random values", correct_option="C", difficulty=1),
        Question(topic_id=t.id, text="What is the worst-case time complexity of search in an unbalanced BST?", option_a="O(1)", option_b="O(log n)", option_c="O(n)", option_d="O(n log n)", correct_option="C", difficulty=3),
        Question(topic_id=t.id, text="Which traversal of a BST gives elements in sorted order?", option_a="Preorder", option_b="Inorder", option_c="Postorder", option_d="Level order", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="What is the height of a balanced BST with n nodes?", option_a="O(n)", option_b="O(log n)", option_c="O(n²)", option_d="O(1)", correct_option="B", difficulty=3),
    ])

    # Sorting Algorithms
    t = dsa_topic_objs["Sorting Algorithms"]
    questions.extend([
        Question(topic_id=t.id, text="What is the average time complexity of Quick Sort?", option_a="O(n)", option_b="O(n log n)", option_c="O(n²)", option_d="O(log n)", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Which sorting algorithm is stable and has O(n log n) worst-case performance?", option_a="Quick Sort", option_b="Heap Sort", option_c="Merge Sort", option_d="Selection Sort", correct_option="C", difficulty=3),
        Question(topic_id=t.id, text="What is the best-case time complexity of Bubble Sort?", option_a="O(n²)", option_b="O(n log n)", option_c="O(n)", option_d="O(1)", correct_option="C", difficulty=2),
        Question(topic_id=t.id, text="Which sorting algorithm works by repeatedly selecting the minimum element?", option_a="Insertion Sort", option_b="Selection Sort", option_c="Merge Sort", option_d="Bubble Sort", correct_option="B", difficulty=1),
        Question(topic_id=t.id, text="What is the space complexity of Merge Sort?", option_a="O(1)", option_b="O(log n)", option_c="O(n)", option_d="O(n²)", correct_option="C", difficulty=3),
    ])

    # Dynamic Programming
    t = dsa_topic_objs["Dynamic Programming"]
    questions.extend([
        Question(topic_id=t.id, text="What are the two key properties of a problem that make it suitable for dynamic programming?", option_a="Greedy choice and sorting", option_b="Optimal substructure and overlapping subproblems", option_c="Divide and conquer and sorting", option_d="Recursion and iteration", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="What is the time complexity of the DP solution for the 0/1 Knapsack problem with n items and capacity W?", option_a="O(n × W)", option_b="O(2^n)", option_c="O(n²)", option_d="O(n log n)", correct_option="A", difficulty=4),
        Question(topic_id=t.id, text="Which approach builds up solutions from the smallest subproblems?", option_a="Top-down (memoization)", option_b="Bottom-up (tabulation)", option_c="Greedy", option_d="Backtracking", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="The Fibonacci sequence computed recursively without memoization has time complexity:", option_a="O(n)", option_b="O(n²)", option_c="O(2^n)", option_d="O(log n)", correct_option="C", difficulty=2),
        Question(topic_id=t.id, text="Which problem is NOT typically solved using dynamic programming?", option_a="Longest Common Subsequence", option_b="Finding connected components", option_c="Matrix Chain Multiplication", option_d="Edit Distance", correct_option="B", difficulty=4),
    ])

    # ── Questions: Artificial Intelligence ────────────────────────────

    # Search Algorithms
    t = ai_topic_objs["Search Algorithms"]
    questions.extend([
        Question(topic_id=t.id, text="Which search algorithm explores the shallowest nodes first?", option_a="DFS", option_b="BFS", option_c="A*", option_d="Hill Climbing", correct_option="B", difficulty=1),
        Question(topic_id=t.id, text="DFS uses which data structure internally?", option_a="Queue", option_b="Stack", option_c="Priority Queue", option_d="Hash Map", correct_option="B", difficulty=1),
        Question(topic_id=t.id, text="What is the time complexity of BFS on a graph with V vertices and E edges?", option_a="O(V)", option_b="O(E)", option_c="O(V + E)", option_d="O(V × E)", correct_option="C", difficulty=2),
        Question(topic_id=t.id, text="Uniform Cost Search is optimal when:", option_a="All costs are equal", option_b="All costs are non-negative", option_c="The graph is acyclic", option_d="The heuristic is admissible", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="Iterative Deepening DFS combines the advantages of:", option_a="BFS and Greedy", option_b="BFS and DFS", option_c="A* and DFS", option_d="DFS and Hill Climbing", correct_option="B", difficulty=3),
    ])

    # Heuristic Functions
    t = ai_topic_objs["Heuristic Functions"]
    questions.extend([
        Question(topic_id=t.id, text="A heuristic function h(n) is admissible if it:", option_a="Always overestimates the cost", option_b="Never overestimates the cost", option_c="Is always zero", option_d="Equals the true cost", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="In A* search, f(n) is defined as:", option_a="g(n) only", option_b="h(n) only", option_c="g(n) + h(n)", option_d="g(n) × h(n)", correct_option="C", difficulty=2),
        Question(topic_id=t.id, text="Which heuristic is commonly used for grid-based pathfinding?", option_a="Euclidean distance", option_b="Manhattan distance", option_c="Hamming distance", option_d="Both A and B", correct_option="D", difficulty=2),
        Question(topic_id=t.id, text="A consistent (monotonic) heuristic satisfies:", option_a="h(n) ≤ c(n,n') + h(n')", option_b="h(n) ≥ h(n')", option_c="h(n) = 0 for all n", option_d="h(n) > c(n, goal)", correct_option="A", difficulty=4),
        Question(topic_id=t.id, text="Greedy Best-First Search uses which evaluation function?", option_a="f(n) = g(n)", option_b="f(n) = h(n)", option_c="f(n) = g(n) + h(n)", option_d="f(n) = 1", correct_option="B", difficulty=2),
    ])

    # CSP
    t = ai_topic_objs["Constraint Satisfaction Problems"]
    questions.extend([
        Question(topic_id=t.id, text="A CSP consists of which three components?", option_a="Variables, Domains, Constraints", option_b="States, Actions, Goals", option_c="Nodes, Edges, Weights", option_d="Inputs, Outputs, Functions", correct_option="A", difficulty=1),
        Question(topic_id=t.id, text="What does AC-3 algorithm enforce?", option_a="Path consistency", option_b="Arc consistency", option_c="Node consistency", option_d="Global consistency", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="Backtracking search improves over brute force by:", option_a="Using randomness", option_b="Pruning inconsistent assignments early", option_c="Using heuristics only", option_d="Sorting variables", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="MRV (Minimum Remaining Values) heuristic selects:", option_a="The variable with the most values left", option_b="The variable with the fewest values left", option_c="A random variable", option_d="The first variable", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="The map coloring problem is an example of:", option_a="Search problem", option_b="Optimization problem", option_c="Constraint satisfaction problem", option_d="Classification problem", correct_option="C", difficulty=1),
    ])

    # Knowledge Representation
    t = ai_topic_objs["Knowledge Representation"]
    questions.extend([
        Question(topic_id=t.id, text="In First-Order Logic, ∀x P(x) means:", option_a="There exists an x such that P(x)", option_b="For all x, P(x) is true", option_c="P(x) is false for all x", option_d="P(x) is undefined", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Forward chaining is a form of:", option_a="Backward reasoning", option_b="Data-driven reasoning", option_c="Goal-driven reasoning", option_d="Random inference", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="A knowledge base in FOL consists of:", option_a="Only facts", option_b="Only rules", option_c="Facts and rules (sentences)", option_d="Only variables", correct_option="C", difficulty=1),
        Question(topic_id=t.id, text="Modus Ponens states: if P and P → Q, then:", option_a="P is false", option_b="Q is true", option_c="Q is false", option_d="P → Q is false", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Which is NOT a valid FOL sentence?", option_a="∀x Student(x) → Studies(x)", option_b="∃x Loves(x, y)", option_c="Student(John)", option_d="∀∃ x y", correct_option="D", difficulty=3),
    ])

    # Machine Learning Basics
    t = ai_topic_objs["Machine Learning Basics"]
    questions.extend([
        Question(topic_id=t.id, text="Which type of learning uses labelled training data?", option_a="Unsupervised learning", option_b="Supervised learning", option_c="Reinforcement learning", option_d="Transfer learning", correct_option="B", difficulty=1),
        Question(topic_id=t.id, text="A decision tree splits data based on:", option_a="Random features", option_b="Feature that gives highest information gain", option_c="Alphabetical order of features", option_d="Size of the dataset", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Overfitting occurs when a model:", option_a="Is too simple", option_b="Performs well on training but poorly on test data", option_c="Has high bias", option_d="Underfits the training data", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Which metric is used for classification accuracy?", option_a="Mean Squared Error", option_b="R-squared", option_c="F1 Score", option_d="Mean Absolute Error", correct_option="C", difficulty=2),
        Question(topic_id=t.id, text="K-Means is an example of:", option_a="Supervised classification", option_b="Unsupervised clustering", option_c="Reinforcement learning", option_d="Semi-supervised learning", correct_option="B", difficulty=1),
    ])

    # Neural Networks
    t = ai_topic_objs["Neural Networks"]
    questions.extend([
        Question(topic_id=t.id, text="An artificial neuron computes:", option_a="A random output", option_b="A weighted sum passed through an activation function", option_c="The mean of inputs", option_d="The maximum input", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Backpropagation is used to:", option_a="Forward pass data", option_b="Compute gradients for weight updates", option_c="Initialize weights", option_d="Normalize inputs", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="Which activation function outputs values between 0 and 1?", option_a="ReLU", option_b="Sigmoid", option_c="Tanh", option_d="Linear", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="A Convolutional Neural Network (CNN) is primarily used for:", option_a="Text classification", option_b="Image recognition", option_c="Time series prediction", option_d="Tabular data", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="The vanishing gradient problem is most severe in:", option_a="Shallow networks", option_b="Deep networks with sigmoid activation", option_c="Networks with ReLU", option_d="Linear networks", correct_option="B", difficulty=4),
    ])

    # ── Questions: Database Management Systems ────────────────────────

    # SQL Basics
    t = dbms_topic_objs["SQL Basics"]
    questions.extend([
        Question(topic_id=t.id, text="Which SQL keyword is used to retrieve data?", option_a="INSERT", option_b="UPDATE", option_c="SELECT", option_d="DELETE", correct_option="C", difficulty=1),
        Question(topic_id=t.id, text="What does the WHERE clause do?", option_a="Sorts results", option_b="Filters rows based on conditions", option_c="Groups rows", option_d="Joins tables", correct_option="B", difficulty=1),
        Question(topic_id=t.id, text="Which JOIN returns all rows from both tables?", option_a="INNER JOIN", option_b="LEFT JOIN", option_c="FULL OUTER JOIN", option_d="CROSS JOIN", correct_option="C", difficulty=2),
        Question(topic_id=t.id, text="The GROUP BY clause is used with:", option_a="WHERE", option_b="Aggregate functions", option_c="ORDER BY only", option_d="INSERT statements", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Which constraint ensures all values in a column are unique?", option_a="PRIMARY KEY", option_b="FOREIGN KEY", option_c="UNIQUE", option_d="Both A and C", correct_option="D", difficulty=2),
    ])

    # Normalization
    t = dbms_topic_objs["Normalization"]
    questions.extend([
        Question(topic_id=t.id, text="First Normal Form (1NF) requires:", option_a="No partial dependencies", option_b="Atomic values in each cell", option_c="No transitive dependencies", option_d="All keys are composite", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Second Normal Form (2NF) eliminates:", option_a="Transitive dependencies", option_b="Partial dependencies on the primary key", option_c="Multi-valued dependencies", option_d="Repeating groups", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="Which normal form deals with transitive dependencies?", option_a="1NF", option_b="2NF", option_c="3NF", option_d="BCNF", correct_option="C", difficulty=3),
        Question(topic_id=t.id, text="Denormalization is done to:", option_a="Reduce data redundancy", option_b="Improve query performance", option_c="Enforce constraints", option_d="Increase normal form level", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="A table is in BCNF if every determinant is a:", option_a="Foreign key", option_b="Candidate key", option_c="Primary key", option_d="Non-key attribute", correct_option="B", difficulty=4),
    ])

    # Transactions
    t = dbms_topic_objs["Transactions & Concurrency"]
    questions.extend([
        Question(topic_id=t.id, text="ACID stands for:", option_a="Atomicity, Consistency, Isolation, Durability", option_b="Accuracy, Completeness, Integrity, Dependency", option_c="Atomicity, Concurrency, Isolation, Dependency", option_d="Accuracy, Consistency, Isolation, Durability", correct_option="A", difficulty=2),
        Question(topic_id=t.id, text="A dirty read occurs when a transaction reads:", option_a="Committed data", option_b="Uncommitted data from another transaction", option_c="Its own data", option_d="Indexed data", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="Two-Phase Locking (2PL) ensures:", option_a="Deadlock freedom", option_b="Serializability", option_c="Starvation freedom", option_d="Reduced lock contention", correct_option="B", difficulty=4),
        Question(topic_id=t.id, text="Which isolation level allows phantom reads?", option_a="Serializable", option_b="Repeatable Read", option_c="Read Committed", option_d="Read Uncommitted", correct_option="B", difficulty=4),
        Question(topic_id=t.id, text="A deadlock occurs when:", option_a="A transaction is too slow", option_b="Two or more transactions wait for each other's locks", option_c="A table is too large", option_d="Indexes are missing", correct_option="B", difficulty=3),
    ])

    # Indexing
    t = dbms_topic_objs["Indexing & Query Optimization"]
    questions.extend([
        Question(topic_id=t.id, text="A B-tree index provides which time complexity for search?", option_a="O(n)", option_b="O(log n)", option_c="O(1)", option_d="O(n²)", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="A clustered index determines the:", option_a="Logical order of data", option_b="Physical order of data on disk", option_c="Number of columns", option_d="Type of join used", correct_option="B", difficulty=3),
        Question(topic_id=t.id, text="How many clustered indexes can a table have?", option_a="Unlimited", option_b="One", option_c="Two", option_d="Depends on columns", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="Query optimization involves:", option_a="Writing longer queries", option_b="Choosing the most efficient execution plan", option_c="Adding more tables", option_d="Removing indexes", correct_option="B", difficulty=2),
        Question(topic_id=t.id, text="A hash index is most efficient for:", option_a="Range queries", option_b="Equality lookups", option_c="Pattern matching", option_d="Sorting", correct_option="B", difficulty=3),
    ])

    db.add_all(questions)
    db.commit()

    print(f"[+] Seeded {len(questions)} questions across 3 subjects and 16 topics")
    print("   Demo accounts: admin@example.com / admin123  |  student@example.com / student123")
