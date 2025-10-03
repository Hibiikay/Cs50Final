.PHONY: start stop

start:
	FLASK_APP=app.py FLASK_ENV=development flask run

stop:
	@pid=$$(lsof -ti:5000); \
	if [ -n "$$pid" ]; then \
		kill -9 $$pid && echo "Flask stopped (PID: $$pid)"; \
	else \
		echo "No Flask process found on port 5000"; \
	fi
