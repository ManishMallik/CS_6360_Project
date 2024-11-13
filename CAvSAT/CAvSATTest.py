# import pycosat

# class CAvSAT:
#     def __init__(self, data, integrity_constraints):
#         """
#         Initialize the CAvSAT system.
        
#         Parameters:
#         - data: A list of tuples representing the database records.
#         - integrity_constraints: A list of constraints as lambda functions that must hold.
#         """
#         self.data = data
#         self.integrity_constraints = integrity_constraints
#         self.encoding = []
    
#     def encode_data(self):
#         """
#         Encode data and integrity constraints into SAT clauses.
#         Each tuple in data is represented as a unique variable.
#         """
#         self.variable_map = {record: idx + 1 for idx, record in enumerate(self.data)}
#         # Encode each integrity constraint as a SAT clause
#         for constraint in self.integrity_constraints:
#             clause = self.encode_constraint(constraint)
#             if clause:
#                 self.encoding.append(clause)
    
#     def encode_constraint(self, constraint):
#         """
#         Encode a single integrity constraint.
        
#         Parameters:
#         - constraint: A lambda function representing the integrity constraint.
        
#         Returns:
#         - A clause that represents the constraint in SAT format.
#         """
#         clause = []
#         for record in self.data:
#             if constraint(record):
#                 clause.append(self.variable_map[record])
#             else:
#                 clause.append(-self.variable_map[record])
#         return clause
    
#     def solve_consistent_query(self, query):
#         """
#         Solve the SAT problem to find consistent answers for a given query.
        
#         Parameters:
#         - query: A lambda function that specifies the query condition.
        
#         Returns:
#         - A list of consistent answers that satisfy the query.
#         """
#         self.encode_data()
        
#         # Encode the query as a SAT clause and add it temporarily
#         query_clause = self.encode_constraint(query)
#         self.encoding.append(query_clause)
        
#         # Find all solutions satisfying the constraints and the query
#         solutions = list(pycosat.itersolve(self.encoding))
#         consistent_answers = []
        
#         for solution in solutions:
#             answer_set = set()
#             for var in solution:
#                 if var > 0:  # Positive variables indicate included records
#                     answer_set.add(self.data[var - 1])
#             if answer_set not in consistent_answers:
#                 consistent_answers.append(answer_set)
        
#         # Remove the temporary query clause after solving
#         self.encoding.pop()
        
#         return consistent_answers

# # Example Usage
# # Define a sample dataset
# data = [
#     ('Alice', 'Sales', 5000),
#     ('Bob', 'Engineering', 7000),
#     ('Carol', 'Sales', 6000),
# ]

# # Define integrity constraints (e.g., no two people in Sales can have the same salary)
# constraints = [
#     lambda record: not (record[1] == 'Sales' and record[2] == 5000),  # Alice's salary is unique in Sales
# ]

# # Define a query (e.g., find all employees in Sales)
# query = lambda record: record[1] == 'Sales'

# # Initialize the CAvSAT system
# cavsat_system = CAvSAT(data, constraints)

# # Get consistent answers
# consistent_answers = cavsat_system.solve_consistent_query(query)
# print("Consistent Answers:")
# for answer_set in consistent_answers:
#     print(answer_set)

# Section 2

# import pycosat

# class CAvSAT:
#     def __init__(self, data, integrity_constraints):
#         """
#         Initialize the CAvSAT system.
        
#         Parameters:
#         - data: A list of tuples representing the database records.
#         - integrity_constraints: A list of constraints as lambda functions that must hold.
#         """
#         self.data = data
#         self.integrity_constraints = integrity_constraints
#         self.encoding = []
#         self.variable_map = {}  # Maps records to unique SAT variables

#     def encode_data(self):
#         """
#         Encode data and integrity constraints into SAT clauses.
#         Each tuple in data is represented as a unique variable.
#         """
#         # Map each record to a unique SAT variable
#         self.variable_map = {record: idx + 1 for idx, record in enumerate(self.data)}

#         # Encode each integrity constraint into SAT clauses
#         for constraint in self.integrity_constraints:
#             clause = self.encode_constraint(constraint)
#             if clause:
#                 self.encoding.extend(clause)  # Collecting multiple clauses for each constraint

#     def encode_constraint(self, constraint):
#         """
#         Encode a single integrity constraint.
        
#         Parameters:
#         - constraint: A lambda function representing the integrity constraint.
        
#         Returns:
#         - A list of clauses that represent the constraint in SAT format.
#         """
#         clauses = []
#         for record in self.data:
#             if constraint(record):
#                 # Encode this as a positive literal if the constraint holds
#                 clauses.append([self.variable_map[record]])
#             else:
#                 # Encode as a negative literal if the constraint does not hold
#                 clauses.append([-self.variable_map[record]])
#         return clauses
    
#     def encode_query(self, query):
#         """
#         Encode the query condition into a SAT clause.
        
#         Parameters:
#         - query: A lambda function that specifies the query condition.
        
#         Returns:
#         - A clause that represents the query in SAT format.
#         """
#         return [self.variable_map[record] if query(record) else -self.variable_map[record] for record in self.data]

#     def solve_consistent_query(self, query):
#         """
#         Solve the SAT problem to find consistent answers for a given query.
        
#         Parameters:
#         - query: A lambda function that specifies the query condition.
        
#         Returns:
#         - A list of consistent answers that satisfy the query.
#         """
#         self.encode_data()  # Encode data and constraints first
        
#         # Encode the query as an additional temporary clause
#         query_clause = self.encode_query(query)
#         self.encoding.append(query_clause)
        
#         # Use the SAT solver to find all solutions that satisfy the constraints and the query
#         solutions = list(pycosat.itersolve(self.encoding))
#         consistent_answers = self.extract_consistent_answers(solutions)
        
#         # Remove the temporary query clause after solving
#         self.encoding.pop()
        
#         return consistent_answers

#     def extract_consistent_answers(self, solutions):
#         """
#         Extracts consistent answers from the list of solutions.
        
#         Parameters:
#         - solutions: A list of satisfying solutions from the SAT solver.
        
#         Returns:
#         - A list of sets, each representing a consistent answer set.
#         """
#         consistent_answers = []
#         for solution in solutions:
#             answer_set = set()
#             for var in solution:
#                 if var > 0:  # Positive variables indicate included records
#                     answer_set.add(self.data[var - 1])
#             if answer_set not in consistent_answers:
#                 consistent_answers.append(answer_set)
#         return consistent_answers

# # Example Usage
# # Define a sample dataset
# data = [
#     ('Alice', 'Sales', 5000),
#     ('Bob', 'Engineering', 7000),
#     ('Carol', 'Sales', 6000),
# ]

# # Define integrity constraints (e.g., no two people in Sales can have the same salary)
# constraints = [
#     lambda record: not (record[1] == 'Sales' and record[2] == 5000),  # Unique salary constraint for Alice in Sales
# ]

# # Define a query (e.g., find all employees in Sales)
# query = lambda record: record[1] == 'Sales'

# # Initialize the CAvSAT system
# cavsat_system = CAvSAT(data, constraints)

# # Get consistent answers
# consistent_answers = cavsat_system.solve_consistent_query(query)
# print("Consistent Answers:")
# for answer_set in consistent_answers:
#     print(answer_set)

import pycosat

class CAvSATTest:
    def __init__(self, data, integrity_constraints):
        """
        Initialize the CAvSAT system.
        
        Parameters:
        - data: A list of tuples representing the database records.
        - integrity_constraints: A list of constraints as lambda functions that must hold.
        """
        self.data = data
        self.integrity_constraints = integrity_constraints
        self.encoding = []
        self.variable_map = {}  # Maps records to unique SAT variables

    def encode_data(self):
        """
        Encode data and integrity constraints into SAT clauses.
        Each tuple in data is represented as a unique variable.
        """
        # Map each record to a unique SAT variable
        self.variable_map = {record: idx + 1 for idx, record in enumerate(self.data)}

        # Encode each integrity constraint into SAT clauses
        for constraint in self.integrity_constraints:
            clause = self.encode_constraint(constraint)
            if clause:
                self.encoding.extend(clause)  # Collect multiple clauses for each constraint

    def encode_constraint(self, constraint):
        """
        Encode a single integrity constraint.
        
        Parameters:
        - constraint: A lambda function representing the integrity constraint.
        
        Returns:
        - A list of clauses that represent the constraint in SAT format.
        """
        clauses = []
        for record in self.data:
            if constraint(record):
                # Encode this as a positive literal if the constraint holds
                clauses.append([self.variable_map[record]])
            else:
                # Encode as a negative literal if the constraint does not hold
                clauses.append([-self.variable_map[record]])
        return clauses
    
    def solve_consistent_query(self, query):
        """
        Solve the SAT problem to find consistent answers for a given query.
        
        Parameters:
        - query: A lambda function that specifies the query condition.
        
        Returns:
        - A list of consistent answers that satisfy the query.
        """
        self.encode_data()  # Encode data and constraints first
        
        # Use the SAT solver to find all solutions that satisfy only the constraints
        solutions = list(pycosat.itersolve(self.encoding))
        
        # Filter solutions based on the query after solving
        consistent_answers = self.extract_consistent_answers(solutions, query)
        
        return consistent_answers

    def extract_consistent_answers(self, solutions, query):
        """
        Extracts consistent answers from the list of solutions that satisfy the query condition.
        
        Parameters:
        - solutions: A list of satisfying solutions from the SAT solver.
        - query: A lambda function to filter the solutions based on the query.
        
        Returns:
        - A list of sets, each representing a consistent answer set.
        """
        consistent_answers = []
        for solution in solutions:
            answer_set = set()
            for var in solution:
                if var > 0 and query(self.data[var - 1]):  # Apply query filter here
                    answer_set.add(self.data[var - 1])
            if answer_set and answer_set not in consistent_answers:
                consistent_answers.append(answer_set)
        return consistent_answers

# Example Usage
# Define a sample dataset
data = [
    ('Alice', 'Sales', 5000),
    ('Bob', 'Engineering', 7000),
    ('Carol', 'Sales', 6000),
    ('Dave', 'Marketing', 4000),
]

# Define integrity constraints (e.g., no two people in Sales can have the same salary)
constraints = [
    lambda record: not (record[1] == 'Sales' and record[2] <= 5000),
]

# Define a query (e.g., find all employees in Sales)
query = lambda record: record[1] == 'Sales'

# Initialize the CAvSAT system
cavsat_system = CAvSATTest(data, constraints)

# Get consistent answers
consistent_answers = cavsat_system.solve_consistent_query(query)
print("Consistent Answers (Sales Department):")
for answer_set in consistent_answers:
    print(answer_set)

# Testing the query for the "Engineering" department
query_engineering = lambda record: record[1] == 'Marketing'
consistent_answers_engineering = cavsat_system.solve_consistent_query(query_engineering)
print("\nConsistent Answers (Engineering Department):")
for answer_set in consistent_answers_engineering:
    print(answer_set)
