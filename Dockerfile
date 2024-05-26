FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN chmod +x /app/bin/install_requirements_docker.sh

RUN /app/bin/install_requirements_docker.sh

ENTRYPOINT ["streamlit", "run", "lib/viz/main_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]