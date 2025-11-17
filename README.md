Github: jndunhamcpp

CPP Email: jndunham@cpp.edu

Abhishek Sarepaka

Github: asarepaka

CPP Email: asarepaka@cpp.edu
- Worked on Part 1, which focused on recognizing Python decimal integer literals
- Designed the complete NFA for decintegers, ensuring it handled unlimited digits correctly and followed Python’s lexical rules
- Tested the NFA using JFLAP, generated the required .jff and .jpg files, and implemented the initial Python code that validates decimal integer inputs based on the NFA’s behavior

Abhishek Sarepaka

Github: asarepaka

CPP Email: asarepaka@cpp.edu

- Completed Part 2, expanding the project to support Python octinteger and hexinteger literals 
- Created the NFAs for both bases and combined them with the decinteger NFA into a single unified machine capable of recognizing all three integer types in one run
- Produced the associated JFLAP files, handled batch testing, and updated the code so the program can process integer literals across all supported bases

Nikhitha Vasiraju

Github: nikhithavasiraju

CPP Email: nvasiraju@cpp.edu

- Worked on Part 3, which included the extra credit floating-point literal recognition
- Designed the standalone NFA for Python floating-point numbers and then merged it with the integer NFAs to create the final combined NFA capable of recognizing decinteger, octinteger,
hexinteger, and floatnumber inputs
- Added the full testing support for this combined machine, updated the Python implementation to match the final NFA logic, and ensured all final JFLAP files, code, and test outputs were
complete for submission


This project includes a full set of NFAs (and images) for Python decintegers, octintegers, hexintegers, and floating-point literals, along with a final combined NFA that recognizes all literal 
types at once. The repository contains all .jff automata files, exported .jpg visualization files, and Python code that mirrors the NFA behavior. The program supports interactive input and batch 
testing using in.txt, in_ans.txt, and automated output generation in out.txt that displays expected vs. actual results with pass/fail analysis. All NFAs were tested in JFLAP using multiple-run batch 
mode, and the code was updated to match the same acceptance logic. 
