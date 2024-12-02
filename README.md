# CS_6360_Project
Members: Aryan Kapoor, Manish Mallik, Nikita Ramachandran, and Yusef Alimam

# About the Project
In this project, the main algorithm we implemented and tested is the CAvSAT system, which was built to test how it performs consistent query answering (CQA) over inconsistent datasets and how efficient and accurate it is when evaluating the queries. To do this, along with implementing the whole CAvSAT system, we also implemented simulations of the following methods for CAvSAT to test against:
- KW-SQL-Rewriting
- ConQuer-SQL-Rewriting
- Regular SQL retrieval from the database

For the SQL-Rewriting functions, we skipped the query rewriting part and only wrote the steps that would happen after a query is assumed to be rewritten because the CAvSAT system is the main focus of our project, and we mainly want to compare it against other methods in terms of solving time, data consistency and integrity, and accuracy. A full setup of the SQL-Rewriting functions would introduce unwanted complexities and time consumption, whereas simulating/assuming the queries are already rewritten and only including the steps that happen after rewriting a query will still help us achieve our goal and stay within the scope.

The dataset we are using is stored in dataset.csv, which consists of 10K entries. Around 10-25% of the entries will have the same primary keys as other entries, which we need to test and evaluate the performance of our CAvSAT system and compare that against the SQL-Rewriting methods and the regular SQL retrieval method.

# Tools to Install and Setup
Required Tools and Environments to Install:
1. VSCode (or any other IDE that Python scripts can run on) (https://code.visualstudio.com/download)
2. Python SDK with version >= 3.10 (https://www.python.org/downloads/)
3. Microsoft C++ Build Tools (https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   1. MSVC (Microsoft C++ Compiler)
   2. Windows 10 SDK

# Running the Program
How to Compile and Run Our Code:
1. Download our code from GitHub. To do this, click on the green code button, and click on "Download ZIP". An alternative route to take is downloading the zip folder in our submission, which will contain our code, images, and CSV files.
2. Extract the folder and files from that ZIP folder.
3. Open up that extracted folder in VSCode, where the CAvSAT folder and README file should be in. After getting our code in VSCode and opening up a terminal within VSCode, run the following commands:
   1. `cd CAvSAT` (To get in the CAvSAT directory if not in there already)
   2. `pip install python-sat matplotlib numpy pandas` 
   3. If the above command works, skip this step and go to *iv*. Otherwise, if it throws an error, run:
    
      `pip install --user python-sat matplotlib numpy pandas`

   4. `py cavsat_solver.py`

If it is successfully running, you should see "Processing Query 1..." in the terminal. It will take time to run the whole project, so be patient. Once you see a stacked bar graph, you can observe it, and close that graph in order to see the next graph. Program will successfully stop running after you close both graphs displayed to you by the program.
