import os.path
import click
from load import load_database
from model import DB_PATH
from pathlib import Path

@click.group()
def main():
	"""Entry method."""

@main.command()
@click.option('-s', '--source', help="A source directory with network data.")
def load(source: str):
	"""Creates a database from source directory."""
	try:
		files = load_database(data_source=source)
		print(f"Files uploaded to database: {str(files)}")
	except:
		print(f"ContNext database already exists at: {Path(DB_PATH).resolve()}",
			"\nDatabase must be deleted in order to reload it.")

if __name__ == "__main__":
	main()
