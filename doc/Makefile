all: out/readme.pdf

out/%.pdf: %.md
	pandoc $< -o $@
