# pdfQA

deployed the code to azure -- first deploy the pdf folder which contains all the files

run the azure app service with below cmd :

 -- to check the streamlit is installed properly --> python -m streamlit hello --server.port 8000 --server.address 0.0.0.0

 -- to run my app where my code is inside app.py  --> python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0

                                pdfQA --> main folder which is deployed
                                └───app.py
                                └───requirements.txt
                                └─── .... --> other files

## Docker CMDs

- docker build -t anilaren/pdfqa .

    Explanation - Builing the docker image with a tag name as provided and last . indicate that the docker file is present in same level 

-  docker run --name pdfQA -p 8501:9001 anilaren/pdfqa

    This doesnt work because we need .env values as well right?

    Explanation - Creating contaniner from the image created above so that we can just run it, in the above cmd we are saying that the name of the container will be "pdfQA" and exposing the port 8501 to the external world not the 9001 and at last we give container name or id 

- docker run --name pdfQA -p 8501:9001 --env-file .env anilaren/pdfqa

    we are mentioning the env file that contains valid data

    AZURE_OPENAI_API_KEY=<key>
    AZURE_OPENAI_ENDPOINT=<value>
    AZURE_OPENAI_API_VERSION=<value>
    AZURE_OPENAI_API_TYPE=<value>

    For example:
        AZURE_OPENAI_API_KEY=1ca1
        AZURE_OPENAI_ENDPOINT=https://open-ai.openai.azure.com/
        AZURE_OPENAI_API_VERSION=2023-07-01-preview
        AZURE_OPENAI_API_TYPE=azure

