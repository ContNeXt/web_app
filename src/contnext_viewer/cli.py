import click
from pathlib import Path
import os
from urllib.request import urlretrieve
from zipfile import ZipFile

from contnext_viewer.load import load_database, is_ready
from contnext_viewer.web.app import create_app
from contnext_viewer.constants import HIDDEN_FOLDER, DATA_FOLDER, ZENODO_URL

@click.group()
def main():
	"""Entry method."""

@main.command()
@click.option('-s', '--source', help="A source directory with network data.")
def load(source: str=None):
	"""Creates a database from source directory."""
	print("Loading database....")
	# Load with data files if path is given
	if source:
		files = load_database(data_source=source)
		print(f"Files uploaded to database: {str(files)}")

	else:
		# Create data folder in home
		datafolder = os.path.join(Path.home(), HIDDEN_FOLDER)
		Path(datafolder).mkdir(parents=True, exist_ok=True)
		filepath = os.path.join(datafolder, 'contnext.zip')

		if not Path(filepath).is_file():
			# Load from Zenodo
			print(f"Downloading data ...")
			urlretrieve(ZENODO_URL, filename=filepath)
			print(f"ContNeXt data successfully downloaded: {filepath}")

		# Unzip downloaded data
		with ZipFile(filepath, 'r') as zip:
			zip.extractall(datafolder)
			print(f"ContNeXt data successfully uncompressed to: {datafolder}")
			# Load with data files if path is given
			load_database(data_source=datafolder)



@main.command()
@click.option('--host', default='0.0.0.0', help='Flask host. Defaults to 0.0.0.0')
@click.option('--port', type=int, default=5000, help='Flask port. Defaults to 5000')
@click.option('--template', help='Defaults to "./templates"')
@click.option('--static', help='Defaults to "./static"')
def web(host, port, template, static):
	"""Runs web application."""
	if not is_ready():
		print("Loading database....")
		# Create data folder in home
		datafolder = os.path.join(Path.home(), HIDDEN_FOLDER)
		Path(datafolder).mkdir(parents=True, exist_ok=True)
		filepath = os.path.join(datafolder, 'contnext.zip')

		if not Path(filepath).is_file():
			# Load from Zenodo
			print(f"Downloading data ...")
			urlretrieve(ZENODO_URL, filename=filepath)
			print(f"ContNeXt data successfully downloaded: {filepath}")

		# Unzip downloaded data
		with ZipFile(filepath, 'r') as zip:
			print("Extracting downloaded dataa...")
			zip.extractall(datafolder)
			print(f"ContNeXt data successfully uncompressed to: {datafolder}")
			# Load with data files if path is given
			load_database(data_source=datafolder)

	app = create_app(template_folder=template, static_folder=static)
	app.run(debug=True, host=host, port=port)


if __name__ == "__main__":
	main()
