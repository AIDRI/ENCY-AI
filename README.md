<img src="./assets/Ency.png">


## 💡 Introduction

Researching and creating projects is tedious. Ency is a virtual assistant developed with the concept of automating research and organizing projects and assignments. Get access ENCY [here](https://ency.live/)! (deprecated)

This is the AI repository for Ency, [Link to the Web Repository](https://github.com/milan090/ency). (private)

## 🎨 Presentation

- This is a virtual assistant project that aims to help and simplify a user's web searches.  
- The project is aimed at students, bloggers, researchers, and others.  
- Team Coffee has therefore imagined a simple API to answer this problem: E.N.C.Y.  
- By introducing an article (Wikipedia for example) to the Artificial Intelligence of E.N.C.Y., the BERT algorithm will create a summary of variable size to simplify the readings, but will also suggest interesting or similar readings to the user.

# Installation
Before starting, you must have python 3.6/7/8 64 bit installed and running on your system, else some of the
requirements will fail to install.  
Make sure you have Postman install on your computer : https://www.postman.com/downloads/

Using pip and cmd :  

1. Download Distilbert model and put it into src/AI/checkpoints/  
2. Run the following command on your computer : pip install -r requirements.txt  
3. Go to src and run global.py  
4. Wait for the API to start  
5. Open Postman and use the following configuration :  
    - Use GET method  
    - Add the URL : http://0.0.0.0:80/route  
    - Go to Body -> raw -> JSON  
    
Using docker :

1. Download Distilbert model and put it into src/AI/checkpoints/  
2. Run the following command on your computer : docker-compose up --build  
3. Wait for the dependencies to install  
4. Open Postman and use the following configuration :  
    - Use GET method  
    - Add the URL : http://0.0.0.0:80/route  
    - Go to Body -> raw -> JSON  

## Usage  

To use the API, you have differents choices : (you ll need to replace "route" by the route given here)  

1. ai-tips/ : given a word, the AI will give you some definition, articles, and keywords  
{  
&nbsp;&nbsp;"word" : "yourword"  
}  

2. chatter/ : given an expression, the AI will give you some answers. It is a simple chatbot  
{  
&nbsp;&nbsp;"text" : "yourtext"  
}  

3. summarize-text/ : given a text, the AI will give you a summary, some keywords, and some wikipedia articles.  
{  
&nbsp;&nbsp;"text" : "yourtext",  
&nbsp;&nbsp;"length" : n,  
&nbsp;&nbsp;"keywords" : true / false  
}

3. summarize-url/ : given an url, the AI will give you a summary, some keywords, and some wikipedia articles.  
{  
&nbsp;&nbsp;"url" : "yoururl",  
&nbsp;&nbsp;"length" : n,  
&nbsp;&nbsp;"keywords" : true / false  
}


## AI model

The artificial intelligence model used is based on the BERT model.  
This very powerful model using NLP technique is very useful in translation, summarization, and keyword extraction.  
It is especially these last two parts that will be useful to us.  

Since the objective of BERT is to generate a language model, only the coding mechanism is required.  
In its basic form, Transformer has two distinct mechanisms: an encoder that reads the text entered and a decoder that produces a prediction for the task.  
It is therefore considered bi-directional, although it would be more accurate to say that it is non-directional.  
BERT uses the Transformer, an attention mechanism that learns contextual relationships between words (or sub-words) in a text.

## References

1 - [{"BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova"}](https://arxiv.org/pdf/1810.04805.pdf)   
2 - [Generating text summaries using GPT-2](https://blog.paperspace.com/generating-text-summaries-gpt-2/) (not used in this first version)  
3 - [{"Attention is all you need", "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin"}](https://arxiv.org/abs/1706.03762)  
3 - [Huggins Face Github](https://github.com/huggingface/transformers)  
4 - [CNN-DailyMail dataset](https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail)  

## Use our API  

If you use our API in your project, please cite us as :  
{  
&nbsp;&nbsp;title : "ENCY"  
&nbsp;&nbsp;author : "Adrien I"  
&nbsp;&nbsp;date : "1/25/2021"  
&nbsp;&nbsp;adress : "online"  
&nbsp;&nbsp;url : "https://github.com/AIDRI/ENCY-AI/"  
}
