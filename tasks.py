from invoke import task
import shutil
import os

if shutil.which("python") is None:
    PYTHON = "python3"
else:
    PYTHON = "python"

@task
def clean(c):
    for clean_dir in ["./build","./site"]:
        if os.path.isdir(clean_dir):
            shutil.rmtree(clean_dir)

@task
def test(c):
    with c.cd('tests'):
        c.run(PYTHON + " -m unittest")

@task
def docs(c):
    c.run("mkdocs build")

@task
def build(c, docs=False):
    c.run(PYTHON + " -m build")

@task(test, docs, build)
def all(c):
    pass

@task
def install(c):
    c.run("pip install coreali --find-links file:./dist")

@task
def uninstall(c):
    c.run("pip uninstall coreali")
