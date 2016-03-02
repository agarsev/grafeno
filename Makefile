-include local.mk

OUTDIR?=out
TARGET_LEVEL?=syn.json
FREELING?=analyze
DATA?=$(wildcard data/*)

TARGETS:=$(patsubst data/%,$(OUTDIR)/%.$(TARGET_LEVEL),$(basename $(DATA)))

all: $(TARGETS)

$(OUTDIR)/%: data/%
	@mkdir -p $(OUTDIR)
	cp $< $@

$(OUTDIR)/%.txt: $(OUTDIR)/%.html
	src/html2text.py $< >$@

$(OUTDIR)/%.syn.json: $(OUTDIR)/%.txt
	@echo -n "[" >$@
	$(FREELING) -f en.cfg --outlv dep --output json <$< | sed 's/}\s*{/}, {/g' >>$@
	@echo "]" >>$@

clean:
	rm -rf $(OUTDIR)

.SECONDARY:

.DELETE_ON_ERROR:
