sync:
	uv sync --all-packages

download:
	uv run dataset --executor download

statis:
	uv run dataset --executor statistics --dataset all --modes "train valid test"

remake:
	uv run dataset --executor remake
