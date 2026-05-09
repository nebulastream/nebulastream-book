.PHONY: help html pdf preview drift-check clean

help:
	@echo "Targets:"
	@echo "  html         Render the book to HTML (fast)"
	@echo "  pdf          Render the book to PDF (requires LuaLaTeX)"
	@echo "  preview      Live-preview while editing"
	@echo "  drift-check  Verify cited file paths/line ranges resolve"
	@echo "  clean        Remove rendered output"

html:
	quarto render --to html

pdf:
	quarto render --to pdf

preview:
	quarto preview

drift-check:
	@python3 scripts/drift-check.py

clean:
	rm -rf _book .quarto
