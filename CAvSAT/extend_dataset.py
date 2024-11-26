import csv
import random

# Define the base structure
students = [
    "Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack",
    "Karen", "Liam", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Rachel", "Steve", "Tracy",
    "Uma", "Vera", "Will", "Xander", "Yara", "Zane", "Alex", "Ben", "Chloe", "Diana",
    "Ethan", "Fiona", "Gary", "Haley", "Ian", "Jane", "Kyle", "Lila", "Mike", "Nina",
    "Omar", "Penny", "Ray", "Sara", "Tina", "Ulysses", "Violet", "Wyatt", "Xenia", "Zoe",
    "Aaron", "Bella"
]
courses = [
    (101, "Math101", "Prof. Smith"), (102, "CS101", "Prof. Brown"), (103, "Physics101", "Prof. White"),
    (104, "History101", "Prof. Johnson"), (105, "Math102", "Prof. Taylor"), (106, "CS102", "Prof. Green"),
    (107, "Math103", "Prof. Taylor"), (108, "Biology101", "Prof. Gray"), (109, "Math104", "Prof. Smith"),
    (110, "History102", "Prof. Johnson"), (111, "Physics102", "Prof. White"), (112, "Biology102", "Prof. Gray"),
    (113, "CS103", "Prof. Green"), (114, "History103", "Prof. Johnson"), (115, "Math105", "Prof. Taylor"),
    (116, "Physics103", "Prof. White"), (117, "CS104", "Prof. Green"), (118, "Math106", "Prof. Taylor"),
    (119, "History104", "Prof. Johnson"), (120, "Physics104", "Prof. White"), (121, "CS105", "Prof. Green"),
    (122, "Biology103", "Prof. Gray"), (123, "History105", "Prof. Johnson"), (124, "Math107", "Prof. Taylor"),
    (125, "Physics105", "Prof. White"), (126, "CS106", "Prof. Green"), (127, "Biology104", "Prof. Gray"),
    (128, "History106", "Prof. Johnson"), (129, "Math108", "Prof. Taylor"), (130, "Physics106", "Prof. White"),
    (131, "CS107", "Prof. Green"), (132, "Biology105", "Prof. Gray"), (133, "History107", "Prof. Johnson"),
    (134, "Math109", "Prof. Taylor"), (135, "Physics107", "Prof. White"), (136, "CS108", "Prof. Green"),
    (137, "Biology106", "Prof. Gray"), (138, "History108", "Prof. Johnson"), (139, "Math110", "Prof. Taylor")
]

# Generate 10,000 unique entries
def generate_dataset(file_name, num_entries):
    used_ids = set()  # Track unique (StudentID, CourseID) pairs
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"])
        
        student_count = len(students)
        course_count = len(courses)
        
        for _ in range(num_entries):
            # Randomly assign StudentID and CourseID
            while True:
                student_id = random.randint(1, student_count)
                course = random.choice(courses)
                course_id = course[0]
                # Ensure unique (StudentID, CourseID) pair
                if (student_id, course_id) not in used_ids:
                    used_ids.add((student_id, course_id))
                    break
            
            student_name = students[student_id - 1]
            course_name, instructor = course[1], course[2]
            
            # Write the entry to the file
            writer.writerow([student_id, student_name, course_id, course_name, instructor])

# Generate a dataset with 10,000 entries
generate_dataset("large_dataset.csv", 10000)
