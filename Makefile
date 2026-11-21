# Variables
PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt
FILES = a_maze_ing.py parser.py src/visual/visual.py src/mazegen/mazegen.py\
src/mazegen/__init__.py src/visual/__init__.py

.PHONY: install run debug clean lint lint-strict

install:
	uv sync

run:
	uv run $(PYTHON) $(SCRIPT) $(CONFIG)

build:
	uv build -o .

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	flake8 $(FILES)
	mypy $(FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports\
	 --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 $(FILES)
	mypy $(FILES) --strict
