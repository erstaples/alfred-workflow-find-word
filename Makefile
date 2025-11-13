.PHONY: build build-dev clean install install-dev help

# The name of the workflow files
WORKFLOW_FILE = Find Word.alfredworkflow
WORKFLOW_FILE_DEV = Find Word-dev.alfredworkflow

# Files to exclude from the workflow package
EXCLUDE = -x "*.git*" -x "*ICON.md" -x ".claude/*" -x "README.md" -x ".gitignore" -x "Makefile" -x ".env*" -x "inject_env.py" -x "*.backup" -x "assets/*" -x "*.alfredworkflow"

help:
	@echo "Available targets:"
	@echo "  make build        - Build the production workflow package"
	@echo "  make build-dev    - Build dev version with API key from .env (gitignored)"
	@echo "  make clean        - Remove all workflow packages"
	@echo "  make install      - Build production version and open for installation"
	@echo "  make install-dev  - Build dev version with .env and install"
	@echo "  make help         - Show this help message"

build:
	@if [ -f "$(WORKFLOW_FILE)" ]; then \
		echo "Cleaning $(WORKFLOW_FILE)..."; \
		rm "$(WORKFLOW_FILE)"; \
	fi
	@echo "Building $(WORKFLOW_FILE)..."
	@zip -r "$(WORKFLOW_FILE)" . $(EXCLUDE)
	@echo "✓ Built $(WORKFLOW_FILE)"

build-dev:
	@if [ -f "$(WORKFLOW_FILE_DEV)" ]; then \
		echo "Cleaning $(WORKFLOW_FILE_DEV)..."; \
		rm "$(WORKFLOW_FILE_DEV)"; \
	fi
	@echo "Building $(WORKFLOW_FILE_DEV) with development environment..."
	@if [ ! -f .env ]; then \
		echo "⚠️  No .env file found. Create one from .env.example:"; \
		echo "  cp .env.example .env"; \
		echo "  # Then edit .env with your API key"; \
		exit 1; \
	fi
	@cp info.plist info.plist.backup
	@python3 inject_env.py
	@zip -r "$(WORKFLOW_FILE_DEV)" . $(EXCLUDE)
	@mv info.plist.backup info.plist
	@echo "✓ Built $(WORKFLOW_FILE_DEV) with development environment"
	@echo "⚠️  This file contains your API key and is gitignored"

clean:
	@if [ -f "$(WORKFLOW_FILE)" ]; then \
		echo "Cleaning $(WORKFLOW_FILE)..."; \
		rm "$(WORKFLOW_FILE)"; \
	fi
	@if [ -f "$(WORKFLOW_FILE_DEV)" ]; then \
		echo "Cleaning $(WORKFLOW_FILE_DEV)..."; \
		rm "$(WORKFLOW_FILE_DEV)"; \
	fi
	@if [ -f "info.plist.backup" ]; then \
		rm "info.plist.backup"; \
	fi
	@if [ -f "$(WORKFLOW_FILE)" ] || [ -f "$(WORKFLOW_FILE_DEV)" ]; then \
		:; \
	else \
		echo "✓ Cleaned"; \
	fi

install: build
	@echo "Opening $(WORKFLOW_FILE) for installation..."
	@open "$(WORKFLOW_FILE)"
	@echo "✓ Import the workflow in Alfred"

install-dev: build-dev
	@echo "Opening $(WORKFLOW_FILE_DEV) for installation..."
	@open "$(WORKFLOW_FILE_DEV)"
	@echo "✓ Import the workflow in Alfred with development environment"
