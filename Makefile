sync:
	uv sync --all-packages

agrismart:
	uv run agrismart

benchmark:
	uv run benchmark

training:
	uv run training

# Dataset commands
# 1. Download the dataset
# uv run dataset download
# 2. Remake the dataset
# uv run dataset remake
# 3. Statistics of the dataset
# uv run dataset statistics --set train