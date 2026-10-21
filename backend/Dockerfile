FROM python:3.12-slim
WORKDIR /service
COPY requirements.lock ./
RUN pip install --no-cache-dir --require-hashes -r requirements.lock
COPY backend ./backend
COPY culinary_engine ./culinary_engine
COPY alembic.ini ./
COPY docs/CHEF_CONSTITUTION_0_1.md ./docs/CHEF_CONSTITUTION_0_1.md
ENV PYTHONPATH=/service/backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
