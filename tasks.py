from invoke import task
import shutil

@task
def clean(c):
    shutil.rmtree("./dist")
    shutil.rmtree("./build")

@task
def test(c):
    with c.cd('tests'):
        c.run('python -m unittest')

@task
def build(c, docs=False):
    c.run("python -m build")

@task(test, build)
def all(c):
    pass

@task
def install(c):
    c.run("pip install coreali --find-links file:./dist")

@task
def uninstall(c):
    c.run("pip uninstall coreali")
