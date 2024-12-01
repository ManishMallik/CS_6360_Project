# CS_6360_Project

Required Tools and Environments to Install:
1. VSCode (or any other IDE that Python can run on)
2. Python SDK with version >= 3.10 (https://www.python.org/downloads/)
3. Microsoft C++ Build Tools (https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   1. MSVC (Microsoft C++ Compiler)
   2. Windows 10 SDK

How to Compile and Run Our Code:
1. Download our code from GitHub. To do this, click on the green code button, and click on "Download ZIP".
2. Extract the folder and files from that ZIP folder.
3. Open up the directory in VSCode where the CAvSAT folder is in. After getting our code in VSCode, make sure to run the following commands:
   1. cd CAvSAT
   2. pip install python-sat matplotlib numpy pandas 
   3. If the above command throws an error, run:
    
      pip install --user python-sat matplotlib numpy pandas

   4. py cavsat_solver.py