import nox


@nox.session(python=["3.9"])
def tests(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("pytest")


@nox.session(python=["3.9"])
def lint(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("pylint", "server")
    session.run("mypy", "server")


@nox.session(python=["3.9"])
def security(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("bandit", "-r", "server")
