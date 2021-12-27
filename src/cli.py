import os.path
import click

DB_LOADER = os.path.abspath('load_db.py')

@click.group()
def main():
	"""Entry method."""

@main.command()
@click.argument('source-dir')
def load(source_dir: str):
	"""Creates a database from source directory."""
	# TODO check database is not loaded
	os.system(f"{DB_LOADER} {source_dir}")

if __name__ == "__main__":
	main()
