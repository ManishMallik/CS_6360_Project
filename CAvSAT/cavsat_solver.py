import csv
import time
from pysat.solvers import Glucose3
import matplotlib.pyplot as plt
import numpy as np

class CAvSAT:
    
    # Initialize the CAvSAT system with data and constraints
    def __init__(self, data, constraints):
        self.data = data
        self.constraints = constraints
        self.variables = {}
        self.clauses = []
        self.result = []
        self.performance_metrics = {}

    # Encode the data and constraints into SAT variables and clauses
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
        
        # Record the encoding time in the performance metrics
        self.performance_metrics["Encoding Time"] = end_time - start_time

    # Solve the SAT problem and extract answers
    def solve(self, query):
        
        # Encode the data and constraints
        self.encode()

        # Start the SAT solving process
        start_time = time.time()
        solver = Glucose3()
        solver.append_formula(self.clauses)
        if solver.solve():
            self.result = solver.get_model()
        else:
            self.result = None
        end_time = time.time()

        # Update the performance metrics with the SAT solving time
        self.performance_metrics["SAT Solving Time"] = end_time - start_time
        
        # Extract answers based on the query
        return self.extract_answers(query)

    # Extract answers that satisfy the query
    def extract_answers(self, query):
        if not self.result:
            return None

        start_time = time.time()
        answers = set()
        for solution in self.result:
            # Positive variable means the record is included
            if solution > 0:
                for record, index in self.variables.items():
                    if index == solution and query(record):
                        answers.add(record)
        end_time = time.time()
        
        # Update the SAT solving time with the query extraction time
        self.performance_metrics["Query Extraction Time"] = end_time - start_time
        self.performance_metrics["SAT Solving Time"] += end_time - start_time
        
        # Return the answers
        return answers

    # KW-SQL-Rewriting simulation
    def kw_sql_simulation(self, query):
        
        # Start the KW-SQL simulation
        start_time = time.time()
        result = []
        for record in self.data:
            if query(record) and all(constraint(record) for constraint in self.constraints):
                result.append(record)
        end_time = time.time()

        # Record the KW-SQL simulation time in the performance metrics
        self.performance_metrics["KW-SQL Simulation Time"] = end_time - start_time
        return result

    # ConQuer-SQL-Rewriting simulation
    def conquer_sql_simulation(self, query):
        
        # Start the ConQuer-SQL simulation
        start_time = time.time()
        result = [record for record in self.data if query(record) and all(constraint(record) for constraint in self.constraints)]
        end_time = time.time()

        # Record the ConQuer-SQL simulation time in the performance metrics
        self.performance_metrics["ConQuer-SQL Simulation Time"] = end_time - start_time
        return result
    
    # Regular SQL retrieval simulation
    def sql_simulation(self, query):
        
        # Start the SQL simulation
        start_time = time.time()
        result = [record for record in self.data if query(record)]
        end_time = time.time()

        # Record the SQL simulation time in the performance metrics
        self.performance_metrics["SQL Simulation Time"] = end_time - start_time
        return result

    # Print the performance metrics
    def print_performance_metrics(self):
        print("Performance Metrics:")
        for key, value in self.performance_metrics.items():
            print(f"{key}: {value:.4f} seconds")

    # Get the performance metrics
    def get_metrics(self):
        return self.performance_metrics

# Function to load data from a CSV file
def load_data_from_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        
        # Skip header row
        header = next(reader)
        for row in reader:
            record = tuple(row)
            data.append(record)
    return data

# Function to validate data consistency and integrity of results based on constraints and query
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

# Function to generate expected results for each query (Method 1)
def generate_expected_results(data, query, output_file, primary_key_index=(0, 3)):
        
    # Generate and save expected results for a given query, resolving primary key conflicts.
    # Keep the first instance of a key that has a conflict.

    # i.e. 
    # StudentID,StudentName,CourseID,CourseName,Instructor <==== Header, not a record
    # 1461,Kimberly Reyes,1480,CS138,Prof. Jones <==== SHOULD BE KEPT!!!
    # 1461,Kimberly R.,   1480,CS138,Prof. Jones <==== SHOULD BE IGNORED because of previous record!!!
    # 3556,Isla Wilson,   2967,Physics156,Prof. Jones

    # output: (Doesn't have the primary key violation)
    # StudentID,StudentName,CourseID,CourseName,Instructor <==== Header, not a record
    # 1461,Kimberly Reyes,1480,CS138,Prof. Jones
    # 3556,Isla Wilson,    2967,Physics156,Prof. Jones

    # Initialize set to track primary keys
    seen_primary_keys = set()
        
    # Initialize list to store filtered results
    filtered_results = []

    for record in data:
        primary_key = tuple(record[i] for i in primary_key_index)
            
        # If the record satisfies the query and the primary key has not been seen before,
        # add it to the filtered results and mark the primary key as seen
        if query(record) and primary_key not in seen_primary_keys:
            filtered_results.append(record)
            seen_primary_keys.add(primary_key) 

    # Write the filtered results to a CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])  # Header
        writer.writerows(filtered_results)

    print(f"Expected results written to {output_file}")

# Function to generate expected results for each query (Method 2)
# Unlike the previous function (Method 1), this function filters out all of the records that violate primary key constraints
def generate_expected_results_2(data, query, output_file, primary_key_index=(0, 3)):
    
    # Initialize set to track primary keys
    seen_primary_keys = set()
    
    # Initialize list to store filtered results
    filtered_results = []

    # Identify and track records that violate primary key constraints
    primary_key_violations = set()
    for record in data:
        primary_key = tuple(record[i] for i in primary_key_index)
        if primary_key in seen_primary_keys:
            primary_key_violations.add(primary_key)
        else:
            seen_primary_keys.add(primary_key)
        
    # Filter out records that violate primary key constraints
    for record in data:
        primary_key = tuple(record[i] for i in primary_key_index)
        if query(record) and primary_key not in primary_key_violations:
            filtered_results.append(record)
        
    # Write the filtered results to a CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])
        writer.writerows(filtered_results)
    
    print(f"Expected results written to {output_file}")

# Main function
if __name__ == "__main__":
    # Load dataset from a CSV file
    file_path = "dataset.csv"
    data = load_data_from_csv(file_path)

    # Define constraints: No two records should have the same StudentID and CourseName
    # In the real world, a student cannot take the same course twice during the same semester
    constraints = [
        lambda record: not any(
            r != record and r[0] == record[0] and r[3] == record[3] for r in data
        )
    ]

    # Example queries
    # Find all records consisting of students enrolled in Math courses
    # Represents following SQL statement: SELECT * FROM data WHERE CourseName LIKE 'Math%'
    query1 = lambda record: "Math" in record[3]

    # Find all records consisting of students enrolled in CS courses taught by Prof. Brown
    # Represents following SQL statement: SELECT * FROM data WHERE CourseName LIKE 'CS%' AND Instructor = 'Prof. Brown'
    query2 = lambda record: "CS" in record[3] and "Prof. Brown" in record[4]

    # Find all records whose CourseID is even (creative use of numeric fields)
    # Represents following SQL statement: SELECT * FROM data WHERE CourseID % 2 = 0
    query3 = lambda record: int(record[2]) % 2 == 0

    # Find all records consisting of students whose names start with the letter 'K' (e.g., Kimberly Reyes)
    # Represents following SQL statement: SELECT * FROM data WHERE StudentName LIKE 'K%'
    query4 = lambda record: record[1].startswith("K")

    # Find all records consisting of courses taught by one of the following professor names
    # Represents following SQL statement: SELECT * FROM data WHERE Instructor = "Prof. Jones" OR Instructor = "Prof. Wilson"
    query5 = lambda record: record[4] in ["Prof. Jones", "Prof. Wilson"]

    # Find all records consisting of CourseIDs that are greater than 2000
    # Represents following SQL statement: SELECT * FROM data WHERE CourseID > 2000
    query6 = lambda record: int(record[2]) > 2000

    # Find all records consisting of students whose names contain "Taylor" (supports flexible searches, can be first or last name)
    # Represents following SQL statement: SELECT * FROM data WHERE StudentName LIKE %Taylor%
    query7 = lambda record: "Taylor" in record[1]

    # Function to generate expected results for each query (Method 1)
    # def generate_expected_results(data, query, output_file, primary_key_index=(0, 3)):
        
    #     # Generate and save expected results for a given query, resolving primary key conflicts.
    #     # Keep the first instance of a key that has a conflict.

    #     # i.e. 
    #     # StudentID,StudentName,CourseID,CourseName,Instructor <==== Header, not a record
    #     # 1461,Kimberly Reyes,1480,CS138,Prof. Jones <==== SHOULD BE KEPT!!!
    #     # 1461,Kimberly R.,   1480,CS138,Prof. Jones <==== SHOULD BE IGNORED because of previous record!!!
    #     # 3556,Isla Wilson,   2967,Physics156,Prof. Jones

    #     # output: (Doesn't have the primary key violation)
    #     # StudentID,StudentName,CourseID,CourseName,Instructor <==== Header, not a record
    #     # 1461,Kimberly Reyes,1480,CS138,Prof. Jones
    #     # 3556,Isla Wilson,    2967,Physics156,Prof. Jones

    #     # Initialize set to track primary keys
    #     seen_primary_keys = set()
        
    #     # Initialize list to store filtered results
    #     filtered_results = []

    #     for record in data:
    #         primary_key = tuple(record[i] for i in primary_key_index)
            
    #         # If the record satisfies the query and the primary key has not been seen before,
    #         # add it to the filtered results and mark the primary key as seen
    #         if query(record) and primary_key not in seen_primary_keys:
    #             filtered_results.append(record)
    #             seen_primary_keys.add(primary_key) 

    #     # Write the filtered results to a CSV file
    #     with open(output_file, mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])  # Header
    #         writer.writerows(filtered_results)

    #     print(f"Expected results written to {output_file}")

    # # Function to generate expected results for each query (Method 2)
    # # Unlike the previous function (Method 1), this function filters out all of the records that violate primary key constraints
    # def generate_expected_results_2(data, query, output_file, primary_key_index=(0, 3)):
    #     seen_primary_keys = set()
    #     filtered_results = []

    #     # Identify and track records that violate primary key constraints
    #     primary_key_violations = set()
    #     for record in data:
    #         primary_key = tuple(record[i] for i in primary_key_index)
    #         if primary_key in seen_primary_keys:
    #             primary_key_violations.add(primary_key)
    #         else:
    #             seen_primary_keys.add(primary_key)
        
    #     # Filter out records that violate primary key constraints
    #     for record in data:
    #         primary_key = tuple(record[i] for i in primary_key_index)
    #         if query(record) and primary_key not in primary_key_violations:
    #             filtered_results.append(record)
        
    #     # Write the filtered results to a CSV file
    #     with open(output_file, mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])
    #         writer.writerows(filtered_results)

    #     print(f"Expected results written to {output_file}")

    # Apply for all queries
    generate_expected_results(data, query1, "query1_expected_results.csv")
    generate_expected_results(data, query2, "query2_expected_results.csv")
    generate_expected_results(data, query3, "query3_expected_results.csv")
    generate_expected_results(data, query4, "query4_expected_results.csv")
    generate_expected_results(data, query5, "query5_expected_results.csv")
    generate_expected_results(data, query6, "query6_expected_results.csv")
    generate_expected_results(data, query7, "query7_expected_results.csv")

    generate_expected_results_2(data, query1, "query1_expected_results_2.csv")
    generate_expected_results_2(data, query2, "query2_expected_results_2.csv")
    generate_expected_results_2(data, query3, "query3_expected_results_2.csv")
    generate_expected_results_2(data, query4, "query4_expected_results_2.csv")
    generate_expected_results_2(data, query5, "query5_expected_results_2.csv")
    generate_expected_results_2(data, query6, "query6_expected_results_2.csv")
    generate_expected_results_2(data, query7, "query7_expected_results_2.csv")

    # Store all queries in a list
    queries = [query1, query2, query3, query4, query5, query6, query7]

    # Initialize the CAvSAT system
    cavsat_system = CAvSAT(data, constraints)

    # Initialize arrays for performance metrics
    encoding_times = []
    solving_times = []
    kw_sql_rewriting_times = []
    conquer_sql_rewriting_times = []
    sql_times = []
    query_labels = []

    # Process all queries
    for i, query in enumerate(queries, start=1):
        print(f"\nProcessing Query {i}...")

        # Solve the SAT problem
        sat_results = cavsat_system.solve(query)
        if sat_results:
            
            # Save SAT results to a CSV file
            with open(f"query{i}_sat_results.csv", mode='w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])
                writer.writerows(sat_results)
        else:
            print("No satisfying solution found.")

        # Simulate KW-SQL query
        kw_sql_results = cavsat_system.kw_sql_simulation(query)
        if kw_sql_results:

            # Save KW-SQL results to a CSV file
            with open(f"query{i}_kw_sql_rewriting_results.csv", mode='w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])
                writer.writerows(kw_sql_results)

        # Simulate ConQuer-SQL query
        conquer_sql_results = cavsat_system.conquer_sql_simulation(query)
        if conquer_sql_results:
            # Save ConQuer-SQL results to a CSV file
            with open(f"query{i}_conquer_sql_rewriting_results.csv", mode='w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])
                writer.writerows(conquer_sql_results)

        # Simulate SQL-like query
        sql_results = cavsat_system.sql_simulation(query)
        if sql_results:
            # Save SQL results to a CSV file
            with open(f"query{i}_regular_sql_retrieval_results.csv", mode='w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])
                writer.writerows(sql_results)

        # Validate results
        print("\nData Integrity Validation (are the consistency and integrity of the results maintained?):")
        print("SAT-Solver Query Results:", data_integrity_validation(sat_results, constraints, query))
        print("KW-SQL-Rewriting Results:", data_integrity_validation(kw_sql_results, constraints, query))
        print("ConQuer-SQL-Rewriting Results:", data_integrity_validation(conquer_sql_results, constraints, query))
        print("Regular SQL Query Results:", data_integrity_validation(sql_results, constraints, query))

        # Write the data integrity validation results to a CSV file
        with open(f"query{i}_data_integrity_validation_results.csv", mode='w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Method", "Consistency and Integrity of Data Results Maintained?"])
            writer.writerow(["SAT-Solver", data_integrity_validation(sat_results, constraints, query)])
            writer.writerow(["KW-SQL-Rewriting", data_integrity_validation(kw_sql_results, constraints, query)])
            writer.writerow(["ConQuer-SQL-Rewriting", data_integrity_validation(conquer_sql_results, constraints, query)])
            writer.writerow(["Regular SQL Query", data_integrity_validation(sql_results, constraints, query)])
            
        # Load the expected results from the CSV file
        output_file = f"query{i}_expected_results.csv"
        output_file_2 = f"query{i}_expected_results_2.csv"
        expected_results = load_data_from_csv(output_file)
        expected_results_2 = load_data_from_csv(output_file_2)

        # Calculate accuracy against each set of expected results
        # 1st set of expected results: For multiple records with the same primary key, keep the first instance and disregard the rest of the records
        sat_accuracy = accuracy(sat_results, expected_results)
        kw_sql_accuracy = accuracy(kw_sql_results, expected_results)
        conquer_sql_accuracy = accuracy(conquer_sql_results, expected_results)
        sql_accuracy = accuracy(sql_results, expected_results)

        # 2nd set of expected results: For any multiple records with the same primary key, disregard all of those records
        sat_accuracy_2 = accuracy(sat_results, expected_results_2)
        kw_sql_accuracy_2 = accuracy(kw_sql_results, expected_results_2)
        conquer_sql_accuracy_2 = accuracy(conquer_sql_results, expected_results_2)
        sql_accuracy_2 = accuracy(sql_results, expected_results_2)

        # Compare the accuracies of each of the methods
        print("\nAccuracy Comparison Method 1:")
        print(f"SAT Accuracy: {sat_accuracy:.4f}")
        print(f"KW-SQL Accuracy: {kw_sql_accuracy:.4f}")
        print(f"ConQuer-SQL Accuracy: {conquer_sql_accuracy:.4f}")
        print(f"SQL Accuracy: {sql_accuracy:.4f}")

        print("\nAccuracy Comparison Method 2:")
        print(f"SAT Accuracy: {sat_accuracy_2:.4f}")
        print(f"KW-SQL Accuracy: {kw_sql_accuracy_2:.4f}")
        print(f"ConQuer-SQL Accuracy: {conquer_sql_accuracy_2:.4f}")
        print(f"SQL Accuracy: {sql_accuracy_2:.4f}")

        # Save the accuracy results to a CSV file
        # Accuracy results against the first set of expected results
        with open(f"query{i}_accuracy_results.csv", mode='w', newline="") as file:
            writer = csv.writer(file)
            # writer.writerow(["Accuracy Results against 1st set of Expected Results (where for multiple records with the same primary key, keep the first instance and disregard the rest of the records)"])
            writer.writerow(["Method", "Accuracy"])
            writer.writerow(["SAT-Solver", sat_accuracy])
            writer.writerow(["KW-SQL-Rewriting", kw_sql_accuracy])
            writer.writerow(["ConQuer-SQL-Rewriting", conquer_sql_accuracy])
            writer.writerow(["Regular SQL Query", sql_accuracy])
        
        # Accuracy results against the second set of expected results
        with open(f"query{i}_accuracy_results_2.csv", mode='w', newline="") as file:
            writer = csv.writer(file)
            # writer.writerow(["Accuracy Results against 2nd set of Expected Results (where for any multiple records with the same primary key, disregard all of those records)"])
            writer.writerow(["Method", "Accuracy"])
            writer.writerow(["SAT-Solver", sat_accuracy_2])
            writer.writerow(["KW-SQL-Rewriting", kw_sql_accuracy_2])
            writer.writerow(["ConQuer-SQL-Rewriting", conquer_sql_accuracy_2])
            writer.writerow(["Regular SQL Query", sql_accuracy_2])

        # Collect performance metrics
        metrics = cavsat_system.get_metrics()
        encoding_times.append(metrics.get("Encoding Time", 0))
        solving_times.append(metrics.get("SAT Solving Time", 0))
        kw_sql_rewriting_times.append(metrics.get("KW-SQL Simulation Time", 0))
        conquer_sql_rewriting_times.append(metrics.get("ConQuer-SQL Simulation Time", 0))
        sql_times.append(metrics.get("SQL Simulation Time", 0))
        query_labels.append(f"Q{i}")

    # Plot performance metrics of encoding time and SAT solving time for each query
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

    # Plot performance metrics for SAT Solving vs KW-SQL-Rewriting vs ConQuer-SQL-Rewriting vs Regular SQL Retrieval
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(query_labels))
    ax.plot(x, solving_times, label='SAT Solving Time', marker='o', linestyle='-', color='b')
    ax.plot(x, kw_sql_rewriting_times, label='KW-SQL Simulation Time', marker='s', linestyle='--', color='r')
    ax.plot(x, conquer_sql_rewriting_times, label='ConQuer-SQL Simulation Time', marker='x', linestyle='-.', color='g')
    ax.plot(x, sql_times, label='SQL Simulation Time', marker='d', linestyle=':', color='m')
    ax.set_xlabel('Queries')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Performance Metrics by Query')
    ax.set_xticks(x)
    ax.set_xticklabels(query_labels)
    ax.set_yscale('log')
    ax.legend()

    plt.tight_layout()
    plt.show()
