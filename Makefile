.PHONY: build clean install help

# The name of the workflow file
WORKFLOW_FILE = Find Word.alfredworkflow

# Files to exclude from the workflow package
EXCLUDE = -x "*.git*" -x "*ICON.md" -x ".claude/*" -x "README.md" -x ".gitignore" -x "Makefile"

help:
	@echo "Available targets:"
	@echo "  make build    - Build the Alfred workflow package"
	@echo "  make clean    - Remove the workflow package"
	@echo "  make install  - Build and open the workflow for installation"
	@echo "  make help     - Show this help message"

build: clean
	@echo "Building $(WORKFLOW_FILE)..."
	@zip -r "$(WORKFLOW_FILE)" . $(EXCLUDE)
	@echo "✓ Built $(WORKFLOW_FILE)"

clean:
	@if [ -f "$(WORKFLOW_FILE)" ]; then \
		echo "Cleaning $(WORKFLOW_FILE)..."; \
		rm "$(WORKFLOW_FILE)"; \
		echo "✓ Cleaned"; \
	fi

install: build
	@echo "Opening $(WORKFLOW_FILE) for installation..."
	@open "$(WORKFLOW_FILE)"
	@echo "✓ Import the workflow in Alfred"
