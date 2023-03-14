# Twitter Watch

## A Twitter Watcher (Tweet Scraper without API and limitations)

### Setup and deploy
How to install requirments:

```bash
pip3 install -r requirments.txt
```

How to run api server:

```bash
cd ./src/
hypercorn main:app --bind 0.0.0.0:80
```

The service will be on 0.0.0.0:80 and Swagger on 0.0.0.0:80/docs

### Docker Setup 

```bash
docker build -t watch .
```

```bash
docker run -d --name twitterwatch -p 80:80 watch
```

### To-Do list
#### Data Mining

- [x] Get all tweets of a twitter user.
- [x] Get all mentions/replies from a specific tweet URL.
- [x] Get info about the audience.

#### Data Analyzing

- [x] Subjectivity and polarity of each mention/reply.
- [x] Sentiment each mention/reply.
- [ ] Translate each Persian/Farsi mention/reply for sentiment.
- [x] Sentiment each Persian/Farsi mention/reply.

#### Tools

- [x] Swagger.
- [ ] Better data cleaning for csv files.
- [ ] Use AI to make a summery of an account.
- [ ] UI/UX

#### Deployment

- [ ] Designing a good arch for project.
- [x] Dockerize.
- [ ] Docker Stack.


### Images
![My animated logo](assets/1.png)
![My animated logo](assets/2.png)
![My animated logo](assets/3.png)
