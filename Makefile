# Makefile for executing stats.py using Poetry

stats:
	poetry run python stats.py

run:
	poetry run streamlit run Matches.py
