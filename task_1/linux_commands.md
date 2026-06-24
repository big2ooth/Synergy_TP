## list of commands used 
# 1. pwd
    function: pwd prints the current working directory.
    command used: 
        $ pwd
    output:
        /c/Users/UNNABH BARUAH/Synergy_TP

# 2. ls
    function: lists the files and folders in the current directory
    command used: 
        $ ls
    output:
        task_1/  venv/

# 3. ls -la
    function: lists ALL the files and folders including hidden files(-a).
    command used: 
        $ ls -la
    output:
        total 37
        drwxr-xr-x 1 UNNABH BARUAH 197121  0 Jun 24 15:45 ./
        drwxr-xr-x 1 UNNABH BARUAH 197121  0 Jun 24 14:26 ../
        drwxr-xr-x 1 UNNABH BARUAH 197121  0 Jun 24 15:53 .git/
        -rw-r--r-- 1 UNNABH BARUAH 197121 64 Jun 24 14:37 .gitignore
        drwxr-xr-x 1 UNNABH BARUAH 197121  0 Jun 24 15:19 task_1/
        drwxr-xr-x 1 UNNABH BARUAH 197121  0 Jun 24 14:40 venv/

# 4. cd
    function: Changes current directory.
    command used:
        $ cd Synergy_TP
    output:
        directory is changed to ~/Synergy_TP 

# 5. mkdir
    function: creates new directories
    command used: 
        $ mkdir -p task_1/data task_1/src
    output:
        task_1/data and task_1/src created

# 6. touch
    function: creates an empty file.
    comman used: 
        $ touch task_1/readme.md task_1/requirements.txt task_1/linux_commands.md task_1/setup_logs.md
    output: 
        empty readme,requirements,linux_commands and setup_logs files are created

# 7. cat 
    function: used to display the contents of a file.
    command used:
        $ cat task_1/requirements.txt
    output:
        certifi==2026.6.17
        charset-normalizer==3.4.7
        idna==3.18
        numpy==2.4.6
        urllib3==2.7.0

# 8. echo
    function: prints text in the terminal and can also create content in a file.
    command used:
        $ echo "hello"
        $ echo "hello" > task_1/data/sample_1
    output:
        hello
        when the 2nd command is executed "task_1/data/sample_1" is overwritten by "hello". (reverted using git restore)

# 9. cp 
    function: copies a file
    command used:
        $ cp task_1/data/sample.txt task_1/copy.txt
    output:
        a new file "copy.txt" is created at Synergy_TP/task_1/copy.txt

# 10. mv 
    function: moves or renames files
    command used:
        $ mv task_1/src/hello.py bye.py
    output:
        hello.py is renamed to bye.py and moved from Synergy_TP/task_1/src/hello.py to Synergy_TP.

# 11. rm 
    function: used to delete files.
    command used:
        $ rm random.txt
    output: 
        removes random.txt from Synergy_TP

# 12. grep 
    function: Searches for a pattern in a file.
    command used:
        $ grep "print" task_1/src/hello.py
    output:
        print("Hello, World!")

# 13. find 
    function: searches for files and directories.
    command used:
        $ find . -name "sample.txt"
    output:
        ./task_1/data/sample.txt

# 14. head 
    function: displays the first 10 lines of a file.
    command used: 
        $ head task_1/setup_log.md
    output:
        SETUP LOG 
        =============
        # cloning repo & chanding directory
        git clone https://github.com/big2ooth/Synergy_TP.git
        cd Synergy_TP
        # making folder structure 
        mkdir -p task_1/data task_1/src
        # creating & activating virtual environment 
        python -m venv venv 
        source venv/Scripts/activate

# 15. tail 
    function: displays the last 10 lines of a file.
    command used:
        $ tail task_1/setup_log.md
    output:
        # generating requirements.txt
        pip freeze > task_1/requirements.txt
        # version control 
        git add .
        git commit -m "task_1 commit"

# 16. wc
    function: counts the number of lines, words and characters and displays them respectively.
    command used:
        $ wc task_1/requirements.txt
    output:
        5  5 89 task_1/requirements.txt
    
# 17. chmod
    function: changes file permissions.
    command used:
        $ chmod -x task_1/src/hello.py
    output:
        removes execute permission from a file
        no output - success 
        