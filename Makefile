.PHONY: install dev test build release-patch release-minor release-major clean

# ── Development ───────────────────────────────────────────────────────────────

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	python -m pytest

validate:
	python scripts/validate_agent_structure.py
	python scripts/validate_yaml.py

# ── Build ─────────────────────────────────────────────────────────────────────

build: clean
	pip install --quiet build
	python -m build
	@echo ""
	@echo "Built packages:"
	@ls -lh dist/

clean:
	rm -rf dist/ build/ *.egg-info

# ── Release (bump + tag + push → triggers GitHub Actions) ────────────────────

release-patch: test
	python scripts/bump_version.py patch
	@NEW=$$(python -c "from agent_forge._version import __version__; print(__version__)"); \
	git add agent_forge/_version.py pyproject.toml && \
	git commit -m "release: v$$NEW" && \
	git tag v$$NEW && \
	git push origin main --tags && \
	echo "" && \
	echo "Released v$$NEW — GitHub Actions will build and publish."

release-minor: test
	python scripts/bump_version.py minor
	@NEW=$$(python -c "from agent_forge._version import __version__; print(__version__)"); \
	git add agent_forge/_version.py pyproject.toml && \
	git commit -m "release: v$$NEW" && \
	git tag v$$NEW && \
	git push origin main --tags && \
	echo "Released v$$NEW"

release-major: test
	python scripts/bump_version.py major
	@NEW=$$(python -c "from agent_forge._version import __version__; print(__version__)"); \
	git add agent_forge/_version.py pyproject.toml && \
	git commit -m "release: v$$NEW" && \
	git tag v$$NEW && \
	git push origin main --tags && \
	echo "Released v$$NEW"

# ── Status ────────────────────────────────────────────────────────────────────

version:
	@python -c "from agent_forge._version import __version__; print('agent-forge', __version__)"
