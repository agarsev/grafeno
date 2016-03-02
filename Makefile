-include local.mk

OUTDIR?=out
TARGET_LEVEL?=syn.json
FREELING?=analyze
DATA?=$(wildcard data/*)

TARGETS:=$(patsubst data/%,$(OUTDIR)/%.$(TARGET_LEVEL),$(basename $(DATA)))

all: $(TARGETS)

$(OUTDIR)/%: data/%
	mkdir -p $(OUTDIR)
	cp $< $@

$(OUTDIR)/%.txt: $(OUTDIR)/%.html
	src/extract_text.py $< >$@

$(OUTDIR)/%.syn.json: $(OUTDIR)/%.txt
	$(FREELING) -f en.cfg --outlv dep --output json <$< >$@

clean:
	rm -rf $(OUTDIR)

.SECONDARY:

.DELETE_ON_ERROR:
