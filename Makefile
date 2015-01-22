#!/usr/bin/env make

# External commands
CTAGS ?= ctags
FIND ?= find
MARKDOWN ?= markdown
NOSE ?= nosetests
PYTHON ?= python
RM_R ?= rm -fr
SH ?= sh

# Options
flags ?=
TESTCMD ?= $(NOSE) --with-doctest $(flags)

PYTHON_DIRS := skeletor
PYTHON_DIRS += tests

# The default target of this makefile is....
all:: help

help:
	@echo "================"
	@echo "Makefile Targets"
	@echo "================"
	@echo "make help - print this message"
	@echo "make test - run unit tests"
	@echo "make README.html - preview markdown"
	@echo "make clean - remove cruft"
.PHONY: help

# Preview the markdown using "make README.html"
%.html: %.md
	$(MARKDOWN) $< >$@

test:
	$(NOSE) $(NOSEARGS) $(PYTHON_DIRS)
.PHONY: test

clean:
	$(FIND) $(PYTHON_DIRS) -name '*.py[cod]' -print0 | xargs -0 rm -f
	$(RM_R) build dist tags
.PHONY: clean

tags:
	$(FIND) $(PYTHON_DIRS) -name '*.py' -print0 | xargs -0 $(CTAGS) -f tags
