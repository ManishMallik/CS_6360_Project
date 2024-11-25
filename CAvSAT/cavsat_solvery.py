import csv
import time
from pysat.solvers import Glucose3

class CAvSAT:
    def __init__(self, data, constraints):
        self.data = data
        self.constraints = constraints
        self.variables = {}
        self.clauses = []
        self.result = []
        self.performance_metrics = {}

    def encode(self):
        start_time = time.time()

        # Assign a unique SAT variable for each record
        for index, record in enumerate(self.data):
            self.variables[record] = index + 1

        # Encode the constraints
        for constraint in self.constraints:
            for record in self.data:
                if not constraint(record):
                    self.clauses.append([-self.variables[record]])
                else:
                    self.clauses.append([self.variables[record]])

        end_time = time.time()
        self.performance_metrics["Encoding Time"] = end_time - start_time

    def solve(self, query):
        self.encode()

        start_time = time.time()
        solver = Glucose3()
        solver.append_formula(self.clauses)
        if solver.solve():
            self.result = solver.get_model()
        else:
            self.result = None
        end_time = time.time()

        self.performance_metrics["SAT Solving Time"] = end_time - start_time
        return self.extract_answers(query)

    def extract_answers(self, query):
        if not self.result:
            return None

        start_time = time.time()
        answers = set()
        for solution in self.result:
            if solution > 0:  # Positive variable means the record is included
                for record, index in self.variables.items():
                    if index == solution and query(record):
                        answers.add(record)
        end_time = time.time()
        self.performance_metrics["Query Extraction Time"] = end_time - start_time

        return answers

    def sql_simulation(self, query):
        start_time = time.time()
        result = [record for record in self.data if query(record)]
        end_time = time.time()

        self.performance_metrics["SQL Simulation Time"] = end_time - start_time
        return result

    def print_performance_metrics(self):
        print("Performance Metrics:")
        for key, value in self.performance_metrics.items():
            print(f"{key}: {value:.4f} seconds")


def load_data_from_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row
        for row in reader:
            record = tuple(row)
            data.append(record)
    return data


if __name__ == "__main__":
    # Load dataset from a CSV file
    file_path = "dataset.csv"  # Replace with your dataset file path
    data = load_data_from_csv(file_path)

    # Define constraints: No two students can have the same StudentID for different courses
    constraints = [
        lambda record: not any(
            r != record and r[0] == record[0] for r in data
        )
    ]

    # Define a query: Find all students in Math courses
    query = lambda record: "Math" in record[3]

    # Initialize the CAvSAT system
    cavsat_system = CAvSAT(data, constraints)

    # Solve the SAT problem
    sat_results = cavsat_system.solve(query)
    if sat_results:
        print("SAT Query Results:")
        for r in sat_results:
            print(r)
    else:
        print("No satisfying solution found.")

    # Simulate SQL-like query
    sql_results = cavsat_system.sql_simulation(query)
    print("\nSQL Query Results:")
    for r in sql_results:
        print(r)

    # Print performance metrics
    cavsat_system.print_performance_metrics()
