# AI-Art-News-Integration

## Description

This is a research project part of my graduation at HoGent as an enterprise & mobile developer. For more information checkout the thesis [here](https://github.com/Darjow/Bachelorproef_2022-2023/tree/main).

This project aims to explore the possibility of AI generating artworks that express the message of news articles in a recognizable manner. We utilize advanced AI models such as DALLE and GPT, in combination with news website scraping using bs4, to obtain relevant and up-to-date input.

The objective of this project is to investigate whether AI is advanced enough to generate artworks closely connected to daily news. We aim to discover if the generated artworks are capable of expressing the message of the news articles in a recognizable way.

## Repository Contents

This repository contains the following classes and directories:

- `src/scraper`: The directory that contains the abstract scraping threads aswell as 2 news website threads: HLN and DeMorgen. 
- `src/openai`: The directory that contains all interaction with the openai library. 
- `src/__main__.py`: The main file you want to execute. 

## Installation and running the application.

Follow these steps to set up the project locally:

1. Clone this repository to your local machine.
2. Install the required libraries and dependencies needed for bs4, openai and others. Refer to the documentation of each library for specific installation instructions.
3. Create an `.env` file and set an environment variable: `OPENAI_API_KEY=<YOUR-OPEN-AI-API-KEY`
4. Run `__main__.py` to gather relevant news articles, start the conversation with GPT, and prompts DALL·E to generate an artpiece.

