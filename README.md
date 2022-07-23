# Library Management System
A Library management system implementation in Python using OOP and Layered Architecture.

It has 5 types of repository:
- InMemory Repository
- TextFiles Repository
- JsonFiles Repository
- PickleFiles Repository
- SqlDatabase Repository

The way the program handles the data (which Repo to use) can be set in settings.properties file.

Advanced Undo - Redo feature using inverse functions.

Tests coverage > 80%. With only the InMemory Repository type, it had 98%.

For representation, I used a DynamicArray with ShellSort.
