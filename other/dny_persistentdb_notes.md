#Tasks for db persistance

1. file hierarchy (DNY: File creation taken care of)
- use the FILES_DIR (set in persistantdb.py) as the root directory
    - have each db take a db_name, which determines the paths from there
        - each directory should have a:
            - header file
            - index file (one for each index)
            - metaheap file
            - tsheap file


2. header file (DNY: TODO)
- in general, the schema does not have to be the same as in dictDB. Instead, I can redefine things;
    - Let's let 'convert' -> 'type', which will be a string that matches to a dictionary that I define, such as
    persistantTypes = {
        'int': int,
        'float': float
    }
    - let the index indicate what type of index (bitmask, binary tree, etc.) will be kept on that data field.

4. index files (DNY: TODO)
- look into how to use binary trees in memory

3. heap file (DNY: Both TSheap and metaheap are taken care of)
