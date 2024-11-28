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
        result = [record for record in self.data if query(record)]
        end_time = time.time()

        self.performance_metrics["KW-SQL Simulation Time"] = end_time - start_time
        return result

    def conquer_sql_simulation(self, query):
        start_time = time.time()
        result = [record for record in self.data if query(record)]
        end_time = time.time()

        self.performance_metrics["SQL Simulation Time"] = end_time - start_time
        return result
    
    def sql_simulation(self, query):
        start_time = time.time()
        result = [record for record in self.data if query(record)]
        end_time = time.time()

        self.performance_metrics["ConQuer-SQL Simulation Time"] = end_time - start_time
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

    # YUSEF HERE. ADDED MORE QUERIES: (I COMMENTED 1 and 2 but didn't go over your old code :) )
    # Find all students in Math courses
    query1 = lambda record: "Math" in record[3]

    # Find all students in CS courses taught by Prof. Brown
    query2 = lambda record: "CS" in record[3] and "Prof. Brown" in record[4]

    # Find students whose CourseID is even (creative use of numeric fields)
    query3 = lambda record: int(record[2]) % 2 == 0

    # Find students whose names start with the letter 'K' (e.g., Kimberly Reyes)
    query4 = lambda record: record[1].startswith("K")

    # Find courses taught by multiple instructors (hypothetical scenario)
    query5 = lambda record: record[4] in ["Prof. Jones", "Prof. Wilson"]

    # Find students enrolled in courses with IDs greater than 2000
    query6 = lambda record: int(record[2]) > 2000

    # Find all students whose names contain "Taylor" (supports flexible searches)
    query7 = lambda record: "Taylor" in record[1]

    # YUSEF HERE. ADDED MORE QUERIES:

    # YUSEF HERE. ADDED CODE TO GENERATE EXPECTED RESULTS
    def generate_expected_results(data, query, output_file, primary_key_index=0):
        """
        Generate and save expected results for a given query, resolving primary key conflicts.
        I decided to go with just keeping the first instance o0f a key that has a conflict.

        ie. 
        StudentID,StudentName,CourseID,CourseName,Instructor
        1461,Kimberly Reyes,1480,CS138,Prof. Jones
        1461,Kimberly R.,     1480,CS138,Prof. Jones <=============== SHOULD BE IGNORED!!!
        3556,Isla Wilson,     2967,Physics156,Prof. Jones

        output: (Doesn't have the primary key violation)
        StudentID,StudentName,CourseID,CourseName,Instructor
        1461,Kimberly Reyes,1480,CS138,Prof. Jones
        3556,Isla Wilson,    2967,Physics156,Prof. Jones

        """
        seen_primary_keys = set()  # To track unique primary keys
        filtered_results = []

        for record in data:
            primary_key = record[primary_key_index]  # Extract the primary key
            if query(record) and primary_key not in seen_primary_keys:
                filtered_results.append(record)
                seen_primary_keys.add(primary_key)  # Mark this primary key as seen

        # Write the filtered results to a CSV file
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])  # Header
            writer.writerows(filtered_results)

        print(f"Expected results written to {output_file}")


    # Apply for all queries
    generate_expected_results(data, query1, "query1_expected_results.csv")
    generate_expected_results(data, query2, "query2_expected_results.csv")
    generate_expected_results(data, query3, "query3_expected_results.csv")
    generate_expected_results(data, query4, "query4_expected_results.csv")
    generate_expected_results(data, query5, "query5_expected_results.csv")
    generate_expected_results(data, query6, "query6_expected_results.csv")
    generate_expected_results(data, query7, "query7_expected_results.csv")
    # YUSEF HERE. ADDED CODE TO GENERATE EXPECTED RESULTS



    #YUSEF HERE. Instead of writing all the code 7 times to make a query I looped on all Queries

    queries = [query1, query2, query3, query4, query5, query6, query7]

    # Initialize the CAvSAT system
    cavsat_system = CAvSAT(data, constraints)

    # Initialize arrays for performance metrics
    encoding_times = []
    solving_times = []
    query_labels = []

    # Process all queries
    for i, query in enumerate(queries, start=1):
        print(f"\nProcessing Query {i}...")

        # Solve the SAT problem
        sat_results = cavsat_system.solve(query)
        if sat_results:
            # Uncomment if u want the print logs, WAAAAAY To many lol 
            # print("SAT Query Results:")
            # for r in sat_results:
            #     print(r)

            # Save SAT results to a CSV file
            with open(f"query{i}_sat_results.csv", mode='w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])
                writer.writerows(sat_results)
        else:
            print("No satisfying solution found.")

        # Simulate KW-SQL query
        kw_sql_results = cavsat_system.kw_sql_simulation(query)

        # Simulate ConQuer-SQL query
        conquer_sql_results = cavsat_system.conquer_sql_simulation(query)

        # Simulate SQL-like query
        sql_results = cavsat_system.sql_simulation(query)
        # Uncomment if u want the print logs, WAAAAAY To many lol 
        # print("\nSQL Query Results:")        
        # for r in sql_results:
        #     print(r)

        # Validate results
        print("\nData Integrity Validation:")
        print("SAT Query Results:", data_integrity_validation(sat_results, constraints, query))
        print("KW-SQL Query Results:", data_integrity_validation(kw_sql_results, constraints, query))
        print("ConQuer-SQL Query Results:", data_integrity_validation(conquer_sql_results, constraints, query))
        print("SQL Query Results:", data_integrity_validation(sql_results, constraints, query))

        # Generate expected results for this query
        output_file = f"query{i}_expected_results.csv"
        generate_expected_results(data, query, output_file)

        # Collect performance metrics
        metrics = cavsat_system.get_metrics()
        encoding_times.append(metrics.get("Encoding Time", 0))
        solving_times.append(metrics.get("SAT Solving Time", 0))
        query_labels.append(f"Q{i}")

    # Plot performance metrics
    x = np.arange(len(query_labels))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, encoding_times, bar_width, label='Encoding Time')
    ax.bar(x, solving_times, bar_width, bottom=encoding_times, label='SAT Solving Time')

    ax.set_xlabel('Queries')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Performance Metrics by Query')
    ax.set_xticks(x)
    ax.set_xticklabels(query_labels)
    ax.legend()

    plt.tight_layout()
    plt.show()
