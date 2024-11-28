import random
import pandas as pd

# Define lists of possible first and last names
first_names = [
    "Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack", "Karen", "Liam", "Mia", "Noah",
    "Olivia", "Paul", "Quinn", "Rachel", "Steve", "Tracy", "Uma", "Vera", "Will", "Xander", "Yara", "Zane", "Aaron",
    "Bella", "Caleb", "Diana", "Ethan", "Fiona", "George", "Hazel", "Ian", "Julia", "Kyle", "Laura", "Mark", "Nina",
    "Oscar", "Penny", "Quincy", "Rose", "Sam", "Tina", "Ulysses", "Victor", "Wendy", "Xavier", "Yvonne", "Zoe",
    "Bryan", "Cindy", "Dennis", "Elena", "Freddie", "Gina", "Harold", "Irene", "Justin", "Kimberly", "Leon", "Monica",
    "Nathan", "Omar", "Peter", "Ruby", "Sebastian", "Tara", "Uriel", "Vanessa", "Wesley", "Ximena", "Yosef", "Zelda",
    "Clara", "Derek", "Emma", "Felix", "Gloria", "Harry", "Isla", "Jasper", "Katie", "Lukas", "Maddie", "Nate", "Olga",
    "Patrick", "Rita", "Sophia", "Theo", "Ursula", "Vince", "Wyatt", "Xena", "Yasmine", "Zack", "Adrian", "Bianca",
    "Charlie", "Dana", "Elliot", "Frances", "Gareth", "Helen", "Isaac", "Jackie", "Kieran", "Lena", "Milo", "Nancy",
    "Ophelia", "Philip", "Renee", "Simone", "Tim", "Uriah", "Valerie", "Winston", "Yvette", "Zoey"
]

last_names = [
    "Smith", "Johnson", "Brown", "Taylor", "White", "Green", "Gray", "Williams", "Jones", "Davis", "Miller", "Wilson",
    "Moore", "Anderson", "Thomas", "Jackson", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", 
    "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "King", "Wright", "Scott", "Adams",
    "Carter", "Evans", "Turner", "Torres", "Nelson", "Baker", "Perez", "Campbell", "Mitchell", "Roberts", "Gonzalez",
    "Foster", "Howard", "Morris", "Bell", "Reed", "Cook", "Rogers", "Morgan", "Cooper", "Peterson", "Flores", "Kelly",
    "Parker", "Ward", "Cruz", "Bailey", "Reyes", "Hughes", "Price", "Myers", "Long", "Fisher", "Sanders", "Barnes",
    "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Russell", "Sullivan", "Ortiz", "Jenkins", "Griffin"
]

prof_last_names = [
    "Smith", "Johnson", "Brown", "Taylor", "White", "Green", "Gray", "Williams", "Jones", "Davis", "Miller", "Wilson",
]

subjects = ["Math", "CS", "Physics", "History", "Biology", "English"]
instructors = [f"Prof. {ln}" for ln in prof_last_names]

print(f"First names: {len(first_names)}")
print(f"Last names: {len(last_names)}")
print(len(first_names) * len(last_names))

# Generate unique CourseID based on CourseName and Instructor
course_mapping = {}
course_id_counter = 101

def get_course_id(course_name, instructor):
    global course_id_counter
    key = (course_name, instructor)
    if key not in course_mapping:
        course_mapping[key] = course_id_counter
        course_id_counter += 1
    return course_mapping[key]

# Pre-generate unique StudentName pool
student_name_pool = [f"{fn} {ln}" for fn in first_names for ln in last_names]
random.shuffle(student_name_pool)

# Map to ensure unique StudentID to StudentName relationship
student_id_to_name = {i: f"{random.choice(first_names)} {random.choice(last_names)}" for i in range(1, 7001)}

def get_unique_student_name(student_id):
    if student_id not in student_id_to_name:
        if not student_name_pool:
            raise ValueError("Ran out of unique names!")
        name = student_name_pool.pop()
        student_id_to_name[student_id] = name
    return student_id_to_name[student_id]

# Generate unique dataset with primary key violations
total_entries = 10000
violation_percentage = random.uniform(0.1, 0.25)
violation_count = int(total_entries * violation_percentage)
unique_count = total_entries - violation_count

unique_entries = set()
while len(unique_entries) < unique_count:
    student_id = random.randint(1, 7000)  # Keep StudentID within a realistic range
    student_name = get_unique_student_name(student_id)
    course_name = f"{random.choice(subjects)}{random.randint(101, 199)}"
    instructor = random.choice(instructors)
    course_id = get_course_id(course_name, instructor)
    if (student_id, course_name) not in {(s[0], s[3]) for s in unique_entries}:
        unique_entries.add((student_id, student_name, course_id, course_name, instructor))

# Generate primary key violation entries
unique_entries = list(unique_entries)
violation_entries = []
for _ in range(violation_count):
    entry = random.choice(unique_entries)
    student_id, student_name, course_id, course_name, instructor = entry
    # Keep StudentID and CourseName the same to ensure primary key violation
    violation_instructor = random.choice([i for i in instructors if i != instructor])
    violation_course_id = get_course_id(course_name, violation_instructor)
    violation_entries.append((student_id, student_name, violation_course_id, course_name, violation_instructor))

# Combine all entries
all_entries = unique_entries + violation_entries

# Convert to DataFrame
columns = ["StudentID", "StudentName", "CourseID", "CourseName", "Instructor"]
df = pd.DataFrame(all_entries, columns=columns)

# Save to CSV
df.to_csv("expanded_dataset.csv", index=False)
print("Dataset generated and saved as 'expanded_dataset.csv'")
