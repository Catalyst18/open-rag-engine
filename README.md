# introductoryRag
![img.png](ideas/img.png)

## To run locally
1. Install docker desktop and docker-compose
2. clone the repository
3. move to the root directory pdf_trainer
4. run `docker-compose up`This will spin up three containers
   1. chroma - vector database
   2. ollama-phi3 - as the model
   3. fast-api - the application
5. If all is successful then you should be able to visit the below url http://localhost:80/docs you should be able to see the swager ui