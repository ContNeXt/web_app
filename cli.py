import os.path
import click

DATABASE_LOADER = os.path.abspath('load_db.py')

@click.group()
def main():
	"""Entry method."""

@main.command()
@click.argument('source-dir')
def compile(source_dir: str):
	"""Creates a database from source directory."""
	os.system(f"DATABASE_LOADER {source_dir}")
