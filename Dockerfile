FROM python:3.10.4
WORKDIR /pdfqa-app

# Copy the requirements file first and install dependencies
# This way, Docker will cache this step if requirements.txt hasn't changed
COPY requirements.txt /pdfqa-app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /pdfqa-app

EXPOSE 9001

CMD ["streamlit", "run", "app.py", "--server.port=9001"]
