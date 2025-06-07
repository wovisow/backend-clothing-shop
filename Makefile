MODULE=src.main:app
HOST=127.0.0.1
PORT=8000


run:
	uvicorn $(MODULE) --reload --host $(HOST) --port $(PORT)
