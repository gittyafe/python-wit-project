from wit import status_def, add_def, init_def, commit_def, checkout_def
import click

@click.group()
def cli():
    """Version Control System, Resembling Git."""
    pass

@click.command()
def init():
    result = init_def()
    click.echo(result)

@click.command()
@click.argument('name')
def add(name):
    result = add_def(name)
    click.echo(result)

@click.command()
@click.option('-m', prompt='Commit message')
def commit(m):
    result = commit_def(m)
    click.echo(result)

@click.command()
@click.argument('commit_id')
def checkout(commit_id):
    result = checkout_def(commit_id)
    click.echo(result)

@click.command()
def status():
    result = status_def()
    click.echo(result)

cli.add_command(init)
cli.add_command(add)
cli.add_command(commit)
cli.add_command(checkout)
cli.add_command(status)