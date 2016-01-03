# branchtodo
A python script helping keeping track of TODOs added to code on current branch.

### Installation
```bash
cd branchtodo
mkvirtualenv branchtodo
pip install -r requirements.txt
```
Then add this to your `bashrc` file:
```bash
branchtodo() {
    $WORKON_HOME/branchtodo/bin/python <PATH_TO_REPO>/branchtodo.py
}
```

### Usage
<img src="https://cloud.githubusercontent.com/assets/31284/12078871/3e85c566-b22b-11e5-9b63-4149e3dd8302.png" width="400">
