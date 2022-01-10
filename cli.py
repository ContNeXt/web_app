import click
from pathlib import Path
import os
from urllib.request import urlretrieve
from zipfile import ZipFile

from src.load import load_database, is_ready
from src.app import create_app
from src.constants import HIDDEN_FOLDER, DATA_FOLDER, ZENODO_URL

@click.group()
def main():
	"""Entry method."""

@main.command()
@click.option('-s', '--source', help="A source directory with network data.")
def load(source: str=None):
	"""Creates a database from source directory."""
	# Load with data files if path is given
	if source:
		files = load_database(data_source=source)
		print(f"Files uploaded to database: {str(files)}")

	else:
		# Load from Zenodo
		hidden_folder = os.path.join(Path.home(), HIDDEN_FOLDER)
		filepath = os.path.join(hidden_folder, DATA_FOLDER)
		urlretrieve(ZENODO_URL, filepath)
		print(f"ContNeXt data successfully downloaded: {filepath}")
		# Unzip downloaded data
		with ZipFile(filepath, 'r') as zip:
			zip.extractall(DATA_FOLDER)
			print(f"ContNeXt data successfully uncompressed: {DATA_FOLDER}")


@main.command()
@click.option('--host', default='0.0.0.0', help='Flask host. Defaults to 0.0.0.0')
@click.option('--port', type=int, default=5000, help='Flask port. Defaults to 5000')
@click.option('--template', help='Defaults to "./templates"')
@click.option('--static', help='Defaults to "./static"')
@click.option('-v', '--verbose', is_flag=True)
def web(host, port, template, static, verbose):
	"""Runs web application."""
	if not is_ready:
		load()
	app = create_app(template_folder=template, static_folder=static)
	app.run(host=host, port=port)


if __name__ == "__main__":
	main()
