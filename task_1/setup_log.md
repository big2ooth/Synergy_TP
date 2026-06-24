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
# creating required .md and .txt files
touch task_1/readme.md task_1/requirements.txt task_1/linux_commands.md task_1/setup_logs.md
touch src/hello.py data/sample.txt
# installing packages 
pip install numpy
# generating requirements.txt
pip freeze > task_1/requirements.txt
# version control 
git add .
git commit -m "task_1 commit"
git push origin main 