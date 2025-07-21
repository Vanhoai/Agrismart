sync:
	uv sync --all-packages

agrismart:
	uv run agrismart

benchmark:
	uv run benchmark

training:
	uv run training

# Download the dataset
# uv run dataset --executor download

# Statistics of the dataset
# uv run dataset --executor statistics --dataset original --mode train

# Remake dataset
# uv run dataset --executor remake