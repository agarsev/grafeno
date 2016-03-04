-include local.mk

OUTDIR?=out
TARGET_LEVEL?=sem.json
FREELING?=analyze
DATA?=$(wildcard data/*)
PENV?=PYTHONPATH=modules:$$PYTHONPATH

TARGETS:=$(patsubst data/%,$(OUTDIR)/%.$(TARGET_LEVEL),$(basename $(DATA)))

all: $(TARGETS)

$(OUTDIR)/%: data/%
	@mkdir -p $(OUTDIR)
	cp $< $@

$(OUTDIR)/%.txt: $(OUTDIR)/%.html
	$(PENV) src/html2text.py $< >$@

$(OUTDIR)/%.syn.json: $(OUTDIR)/%.txt
	@echo -n "[" >$@
	$(FREELING) -f en.cfg --outlv dep --output json <$< | sed 's/}\s*{/}, {/g' >>$@
	@echo "]" >>$@

$(OUTDIR)/%.sem.json: $(OUTDIR)/%.syn.json
	$(PENV) src/extract_concepts.py -p $< >$@

clean:
	rm -rf $(OUTDIR)

.SECONDARY:

.DELETE_ON_ERROR:
