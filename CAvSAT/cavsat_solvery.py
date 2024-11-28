import csv
import time
from pysat.solvers import Glucose3
import matplotlib.pyplot as plt
import numpy as np

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
            conflicting_records = []
            for record in self.data:
                if not constraint(record):
                    self.clauses.append([-self.variables[record]])
                    # conflicting_records.append(self.variables[record])
                else:
                    self.clauses.append([self.variables[record]])
            # if conflicting_records:
            #     self.clauses.append([-r for r in conflicting_records])

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
        self.performance_metrics["SAT Solving Time"] += end_time - start_time

        return answers

    def kw_sql_simulation(self, query):
        start_time = time.time()
        result = []
        for record in self.data:
            if query(record) and all(constraint(record) for constraint in self.constraints):
                result.append(record)
        end_time = time.time()

        self.performance_metrics["KW-SQL Simulation Time"] = end_time - start_time
        return result

    def conquer_sql_simulation(self, query):
        start_time = time.time()
        result = [record for record in self.data if query(record) and all(constraint(record) for constraint in self.constraints)]
        end_time = time.time()

        self.performance_metrics["ConQuer-SQL Simulation Time"] = end_time - start_time
        return result
    
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

    def get_metrics(self):
        return self.performance_metrics


def load_data_from_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row
        for row in reader:
            record = tuple(row)
            data.append(record)
    return data

# I tested this function with the following constraints and query, it works fine.
def data_integrity_validation(results, constraints, query):
    for record in results:
        for constraint in constraints:
            if not constraint(record):
                return False
        if not query(record):
            return False
    return True

# Function to calculate the accuracy of the results
def accuracy(method_results, correct_results):
    true_positives = len(set(method_results).intersection(set(correct_results)))
    false_positives = len(set(method_results) - set(correct_results))
    false_negatives = len(set(correct_results) - set(method_results))
    
    # Not sure if we need to include true negatives when trying to calculate accuracy
    # This could also be inaccurate
    # true_negatives = len(correct_results) - (false_positives + false_negatives)

    # Did not include true_negatives here since we want to check if method results
    # are the same as the correct results and only penalize if there are false positives
    # and false negatives
    accuracy = true_positives / (true_positives + false_positives + false_negatives)
    return accuracy

# Function to compare the results of two methods and display the differences
def compare_method_results(method1results, method2results, method1Name, method2Name):
    same_results = set(method1results).intersection(set(method2results))
    different_results = {
        method1Name: set(method1results) - set(method2results),
        method2Name: set(method2results) - set(method1results)
    }
    return same_results, different_results

if __name__ == "__main__":
    # Load dataset from a CSV file
    file_path = "expanded_dataset.csv"
    data = load_data_from_csv(file_path)

    # Define constraints: No two students can have the same StudentID for different courses
    constraints = [
        lambda record: not any(
            r != record and r[0] == record[0] and r[3] == record[3] for r in data
        )
    ]

    # Define a query: Find all students in Math courses
    query1 = lambda record: "Math" in record[3]
    query2 = lambda record: "CS" in record[3] and "Prof. Brown" in record[4]

    # Initialize the CAvSAT system
    cavsat_system = CAvSAT(data, constraints)

    # Solve the SAT problem
    sat_results1 = cavsat_system.solve(query1)
    
    # Simulate KW-SQL query
    kw_sql_results = cavsat_system.kw_sql_simulation(query1)

    # Simulate ConQuer-SQL query
    conquer_sql_results = cavsat_system.conquer_sql_simulation(query1)
    
    if sat_results1:
        print("SAT Query Results:")
        for r in sat_results1:
            print(r)
            # Save the results to a CSV file
            with open("sat_results.csv", mode='w') as file:
                writer = csv.writer(file)
                # writer.writerow(header)
                for record in sat_results1:
                    writer.writerow(record)
    else:
        print("No satisfying solution found.")

    # Simulate SQL-like query
    sql_results = cavsat_system.sql_simulation(query1)
    print("\nSQL Query Results:")
    for r in sql_results:
        print(r)

    # Validate the integrity of the results
    print("\nData Integrity Validation:")
    print("SAT Query Results:", data_integrity_validation(sat_results1, constraints, query1))
    print("KW-SQL Query Results:", data_integrity_validation(kw_sql_results, constraints, query1))
    print("ConQuer-SQL Query Results:", data_integrity_validation(conquer_sql_results, constraints, query1))
    print("SQL Query Results:", data_integrity_validation(sql_results, constraints, query1))

    # Print performance metrics
    cavsat_system.print_performance_metrics()
    # print("\nPerformance Metrics:")
    # for method, time_taken in metrics.items():
    #     print(f"{method}: {time_taken:.4f} seconds")

    # Plot performance metrics
    metrics1 = cavsat_system.get_metrics()
    sat_results2 = cavsat_system.solve(query2)
    cavsat_system.print_performance_metrics()
    metrics2 = cavsat_system.get_metrics()
    query_labels = ["Q1", "Q2"]
    encoding_Times = [metrics1.get("Encoding Time", 0), metrics2.get("Encoding Time", 0)]
    SAT_Solving_Times = [metrics1.get("SAT Solving Time", 0), metrics2.get("SAT Solving Time", 0)]

    x = np.arange(len(query_labels))

    fig, ax = plt.subplots()
    bar_width = 0.35

    ax.bar(x, encoding_Times, bar_width, label='Encoding Time')
    ax.bar(x, SAT_Solving_Times, bar_width, label='SAT Solving Time', bottom=encoding_Times)

    ax.set_xlabel('Queries')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Performance Metrics')
    ax.set_xticks(x)
    ax.set_xticklabels(query_labels)
    ax.legend()

    plt.show()

    methods = ["SAT Solving", "KW-SQL Simulation", "ConQuer-SQL Simulation"]
    times = [
        metrics1.get("SAT Solving Time", 0),
        metrics1.get("KW-SQL Simulation Time", 0),
        metrics1.get("ConQuer-SQL Simulation Time", 0),
    ]

    plt.figure(figsize=(8, 6))
    plt.bar(methods, times, color='skyblue')
    plt.xlabel('Methods')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Metrics')
    plt.show()

