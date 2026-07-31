# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = DynamicsControl
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

distclean:
	-rm dist/*

dist:
	uv build

upload:
	uv publish

# Notebook handling. .gitattributes is committed, but the drivers it names live
# in .git/config, so this has to be run once per checkout or the attributes
# silently do nothing.
setup-git:
	git config filter.nbclean.clean "python3 tools/nbclean.py"
	git config filter.nbclean.smudge cat
	git config filter.nbclean.required true
	uv run nbdime config-git --enable
# nbdime registers its drivers by bare name, which only resolves when .venv/bin
# is on PATH. Git invokes them itself, including from editors and GUI clients
# that never see the direnv environment, so point at the venv directly.
	git config diff.jupyternotebook.command "$(CURDIR)/.venv/bin/git-nbdiffdriver diff"
	git config merge.jupyternotebook.driver "$(CURDIR)/.venv/bin/git-nbmergedriver merge %O %A %B %L %P"
	git config difftool.nbdime.cmd '$(CURDIR)/.venv/bin/git-nbdifftool diff "$$LOCAL" "$$REMOTE" "$$BASE"'
	git config mergetool.nbdime.cmd '$(CURDIR)/.venv/bin/git-nbmergetool merge "$$BASE" "$$LOCAL" "$$REMOTE" "$$MERGED"'

.PHONY: help Makefile distclean dist upload setup-git

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
