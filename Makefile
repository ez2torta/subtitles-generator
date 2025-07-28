cvs2:
# Makefile para automatizar generación de subtítulos

.PHONY: subtitles clean_subtitles

subtitles:
	@if [ -z "$(PROJECT)" ]; then \
	  echo "Uso: make subtitles PROJECT=nombre_proyecto"; \
	  exit 1; \
	fi
	python3 clean_output.py $(PROJECT) || true
	python3 cli.py subtitle --project $(PROJECT) --textfile $(PROJECT)_subtitulos.txt --input_dir input --output_dir output --font_size 48 --line_separation 1.5

clean_subtitles:
	@if [ -z "$(PROJECT)" ]; then \
	  echo "Uso: make clean_subtitles PROJECT=nombre_proyecto"; \
	  exit 1; \
	fi
	python3 clean_output.py $(PROJECT)
