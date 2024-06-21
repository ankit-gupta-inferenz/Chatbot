from operator import itemgetter
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain.schema.runnable import RunnableBranch
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage,HumanMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.chains import LLMChain
from langchain.schema.output_parser import StrOutputParser
# from . import getData
import os
import openai
from datetime import datetime
import json


os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_ENDPOINT']="https://api.smith.langchain.com"
# os.environ['LANGCHAIN_API_KEY']="ls__3298d37565d342e2a51fb193bce54dca"
os.environ['LANGCHAIN_API_KEY']="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"
os.environ['LANGCHAIN_PROJECT']="Smile-testing"
# API = "a9HS3ptfWmQAfAuPiYBKT3BlbkFJVU6otmeJp8THI2i8EzGK" #Old paid
# API = "proj-UpmqqxoEybZLlu98hhjvT3BlbkFJYFxMYgUPyF0lzm50s0xu" #New Paid Design
API = "proj-WWMWhIwiY4n5vaJtHCXaT3BlbkFJrgKBRjPPwvAV7SZdU968" #New2 Paid Design
# API = "4MWEIRg0uuBv2HevD7PtT3BlbkFJhGYnqtA2KnODK0EAtXgr"
os.environ['OPENAI_API_KEY'] = 'sk-'+API
# openai.api_key = os.environ['OPENAI_API_KEY']
llm_model = "gpt-3.5-turbo"

model = ChatOpenAI(temperature=0.04, model=llm_model)
model2 = ChatOpenAI(temperature=0.04, model=llm_model)
# memoryStorage = RedisChatMessageHistory("akki.trivedi@inferenz.ai", url="redis://localhost:6379")
memory = ConversationBufferMemory(return_messages=True,memory_key="history")
# memory = ConversationBufferWindowMemory(return_messages=True, k=10,memory_key="history")

# text = "my name is sushil mevada. my friend name is ali. i like chocolate cake and red flowers, but ali likes pineapple cake and white flowers."
# memory.chat_memory.messages.append(HumanMessage(content=text))
# # memoryStorage.add_user_message(text)

def getCurrentTime():
    return datetime.now().strftime("%H:%M:%S")

def openAiSearch(memory):
    intent_Prompt = """You are good a Text classificaiton. Classify the given question in given 9 classes.Give the Answer in single word.
    classes : ["Greeting","Shopping","ProductInfo","Trends","PairProduct","OrderDetail","HelpsFAQ","FeedBack","General"]

    Explanation
        Greeting: For any kind of greeting
                    Example: Good Morning, Hello, Hi, hyyy
        Shopping: If user want to purchase or see the  female fashion products
                    Example: Show me red shirt, I want Blue Jeans, 
        ProductInfo: If user asking about any details about female fashion proucts like, Price, any attributes, multiple Product compare
                    Example: What is Difference Between First and Second Product, What is the colour of first product?
        Trends: If user asking about fashion related trends
                    Example: What is trending in shirt?
        PairProduct: If user want to  Pair product only for female fashion product
                    Example: What I should wear with white Shirt?, I have red shirt What I should wear?
        OrderDetail: If user asking about their order progress
                    Example: Where is my order?, How much orders in my order list?
        HelpsFAQ: If user want know to Guidance or advice about product or order, Help, Support, Policies
                    Example: How to show my orders?, How to pay using credit card?, What are the return policies?
        FeedBack: When user give the feedback and Review to any product or Bot
                    Example: I'll give 8 out of 10 for this second product, Good by, By, I'll give 4.5 out of 5
        General: If user asking Irrelavante question except female fashion
                    Example: Who is SRK?, What is Molly?, What you can do?

    <question>
    {question}
    </question>
    Classification:"""

    intentPrompt = ChatPromptTemplate.from_messages(
        [
            ("system", intent_Prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )
    intentChain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | intentPrompt
        | model
        | StrOutputParser()
    )

    Greeting_Prompt = """You are Molly. You are female fashion advisor. And you are working for Styloland.
    Greet the user as per their greet. For greeting you can use user Calender event. Also greet as per Time, Date and User Events

    User Name:"Sushil"
    User Calender:
        29-05-2001: My Birthday
        30-05-2001: Friend Ali's Birthday

    Today: 29-05-2024
    Time: 12:01 PM

    <question>
    {question}
    </question>
    Classification:"""

    GreetingPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", Greeting_Prompt),
            ("human", "{question}")
        ]
    )
    GreetingChain = (
        GreetingPromptTemplate
        | model2
        | StrOutputParser()
    )

    Shopping_Prompt = """You are Molly. You are female fashion advisor. And you are working for Styloland.
    Write a SQL query for user serching product
    If the user history is included, refer to the recent conversation from the history. If the user response is affirmative in response to a previously asked question about whether the user would like to see some products, then identify the keywords from the previous question/response.

    Note: If extracting keywords, do not add any other additional text in response.
    Find only "productId","productName","brandName","category","subCategory","description","price","currency","attributes","quantity","displayImage","otherImages"
    productName: product Name
    category: ['Clothing', 'Accessories', 'Footwear']
    subCategory: ['Top Wear', 'Bottom Wear', 'Full Wear', 'Layers', 'Bags', 'Jewellery', 'Shoes', 'Sandle', 'Sleepers']
    Occasion: ['New-baby', 'Graduation', 'Fathers-day', 'Thank-you', 'Mothersday', 'Get-well', 'Congratulation', 'Anniversary', 'Wedding', 'Welcome-back', 'Housewarming', 'I-am-sorry', 'Back-to-school', 'Receptions', 'Suits-any-occasion', 'Love', 'Birthday']
    brandName: like Flower Story, Arya,Al Jarra etc,
    price: like 10KWD, 20KWD, 30 etc
       
    In database colums are : "productId","productName","brandName","category","subCategory","description","price","currency","attributes","quantity","displayImage","otherImages"
    Table name is: "chat_app_products"

    Given list of attributs and products which are currently we have.
    query should search in all related columns, Always find all products use *.

    example :
        Question: show me something special for my birthday
        Answer: Recommendation: SELECT * FROM chat_app_products WHERE productName LIKE '%birthday%' OR description LIKE '%birthday%' OR category LIKE '%birthday%' OR subCategory LIKE '%birthday%';

    <question>
    {question}
    </question>
    Classification:"""

    ShoppingPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", Shopping_Prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ]
    )
    ShoppingChain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        |ShoppingPromptTemplate
        | model2
        | StrOutputParser()
    )

    ProductInfo_Prompt = """You are Molly. You are female fashion advisor. And you are working for Styloland.
    Provide the Product information which user need. If user compare and they want to know about Product or product attributes so provide information.
    If the user history is included, refer to the recent conversation from the history. If the user response is affirmative in response to a previously asked question about whether the user would like to see some products, then identify the keywords from the previous question/response.

    Note: If extracting keywords, do not add any other additional text in response.
    Find only Name, Category, Sub Category, Occasion, Brand, Price, Colour, HeightWidth, Flower_name
    Name: product Name
    Category: ['Flower-Accesories', 'Bouquets', 'Plants']
    Sub Category: ['Giveaways', 'Crowns', 'Boxes-Baskets', 'terrarium', 'Vases', 'Stands', 'Indoor-Plants', 'Bracelets', 'Necklaces', 'Hand-Bouquets', 'Preserved-Flowers']
    Occasion: ['New-baby', 'Graduation', 'Fathers-day', 'Thank-you', 'Mothersday', 'Get-well', 'Congratulation', 'Anniversary', 'Wedding', 'Welcome-back', 'Housewarming', 'I-am-sorry', 'Back-to-school', 'Receptions', 'Suits-any-occasion', 'Love', 'Birthday']
    Brand: like Flower Story, Arya,Al Jarra etc,
    Price: like 10KWD, 20KWD, 30 etc
    Colour: ['black', 'purple', 'yellow', 'lime', 'clay', 'gold', 'orange', 'red', 'violet', 'brown', 'silver', 'green', 'blue', 'white', 'pink']
    HeightWidth: like 10X10, H:10XW:10 etc
    Flower_name: ['roses', 'peony', 'orchid', 'chrysanthemum', 'iris', 'sunflower', 'violet', 'calla lily', 'tulip', 'hyacinth', 'amaryllis', 'gerbera', 'lily', 'carnation', 'cosmos', 'daisy', 'hydrangea', 'ranunculus', 'snapdragon', 'marigold']

    Given list of attributs and products which are currently we have.

    <question>
    {question}
    </question>
    Classification:"""

    ProductInfoPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", ProductInfo_Prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ]
    )
    ProductInfoChain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | ProductInfoPromptTemplate
        | model2
        | StrOutputParser()
    )

    Trends_Prompt = """You are Molly. You are female fashion advisor. And you are working for Styloland.
    Provide the Tending information as per user query. You can use Content information.
    If the user history is included, refer to the recent conversation from the history. If the user response is affirmative in response to a previously asked question about whether the user would like to see some products, then identify the keywords from the previous question/response.

    Content: `
    Vogue’s Guide to the Best Flip-Flops:
        The Investment Buy: The Row Ginza leather and suede platform flip flops, $990
        The Easy Everyday: Tkees Foundations matte flip flops, $60
        The Office-Appropriate: Aeyede Renee snake effect leather sandals, $295
        The Kitten Heel Variation: Toteme leather flip flops, $450
        The Metallic Stunner: M.Gemi The Liliana, $228
        The Heritage Find: Ancient Greek Saionara leather flip flops, $205
        The Sleek and Simple: Madewell The Gabi thong slide sandal, $68
        The Vacation Ready: Havaianas slim flip flops, $30

    The Row really set the stage for the thong sandal’s comeback with their beautifully-crafted, minimal options, often worn by fans such as Zoë Kravitz and Kendall Jenner on the street in their everyday lives, demonstrating how cool they could be. Bella Hadid is no stranger to the shape either, having sported everything from throwback platforms to heeled flip-flops mixed into her signature looks—which always give us a bit of wardrobe envy. Even if you don’t have a super model’s closet, the great thing about flip-flops is they’re one shoe that is accessible to quite literally everyone and available at every budget.
    Advertisement

    The leather slip-ons from The Row are certainly the crème de la crème, investment buy you will treasure for years, but brands like Tkees and Ancient Greek Sandals make sleek options that won’t break the bank, as well. We recommend sticking to classic, neutral shades and simple silhouettes, to really ace this movement, but if you crave a little texture in your life, might we suggest trying a snakeskin embossed style from Aeyede or Free People, or a hit of metallic like M. Gemi’s bold silver? And if you can’t get behind a simple flat, there are platform styles aplenty from Tory Burch and Zara—as well as the chicest, kitten heel variation from Toteme. Go ahead, shop the 20 best flip-flops that all have the Vogue stamp of approval, below.
    Image may contain: Clothing, Footwear, Sandal, and Shoe
    The Row
        Ginza platform flip flops
            $990 NET-A-PORTER
            Clothing, Footwear, and Sandal
    Mango
        leather straps sandals
            $80 MANGO
            Clothing, Footwear, and Sandal
    Staud
        Dante thong sandals
            $275 NET-A-PORTER
            $275 SAKS FIFTH AVENUE
            $275 STAUD
            Clothing, Footwear, and Sandal
        Foundations flip flops
            $60 NORDSTROM
            $60 SHOPBOP
            $60 REVOLVE
            $60 BLOOMINGDALES
            Clothing, Footwear, and Sandal
        Around Town flip flops
            $54 FREE PEOPLE
            Clothing, Footwear, and Sandal
    Reformation
        Jessie thong sandals
            $128 REFORMATION
            Clothing, Footwear, and Sandal
    Aeyde
        Renee sandals
            $295 NET-A-PORTER
            Clothing, Footwear, and Sandal

    `

    Answer Should in 50 words
    <question>
    {question}
    </question>
    Classification:"""

    TrendsPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", Trends_Prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ]
    )
    TrendsChain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | TrendsPromptTemplate
        | model2
        | StrOutputParser()
    )

    PairProduct_Prompt = """You are Molly. You are female fashion advisor. And you are working for Styloland.
    Find the Paid product based on user's given product or product attritubes.
    If the user history is included, refer to the recent conversation from the history. If the user response is affirmative in response to a previously asked question about whether the user would like to see some products, then identify the keywords from the previous question/response.

    Note: If extracting keywords, do not add any other additional text in response.
    Find only Name, Category, Sub Category, Occasion, Brand, Price, Colour, HeightWidth, Flower_name
    Name: product Name
    Category: ['TopWear', 'BottomWear', 'FullWear', 'Accessories', 'FootWear','Bags','Jewellery' ]
    Sub Category: ["Shirt","T-Shirt","Shooes","Sandles","Saree","Jeans","Shorts"]
    Occasion: ["Diwali", "Navaratri","New Year", "Birthday Party","Wedding","Haldi",]
    Brand: ["Zara", "Adidas","Asopalav","Vimal"],
    Price: like 10KWD, 20KWD, 30 etc
    Colour: ['black', 'purple', 'yellow', 'lime', 'clay', 'gold', 'orange', 'red', 'violet', 'brown', 'silver', 'green', 'blue', 'white', 'pink']
    HeightWidth: like 10X10, H:10XW:10 etc
    Product: ["Denim", "Tube Top"]

    Given list of attributs and products which are currently we have.

    Output format: 'Recommendation:{{"attribute":"value","filter":"column=range(n-m)"/"column=value"}}'

    example :
        Question: I Have a White Shirt, What I should wear.
        Answer: Recommendation:{{"Product":["Jeans"],Colour:["Black","Blue"]}}
        Question: I Have a Black Denim Jeans, What I should wear.
        Answer: Recommendation:{{"Product":["Shirt","T-Shirt"],Colour:["Black","Blue","White","Red"]}}
    <question>
    {question}
    </question>
    Classification:"""

    PairProductPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", PairProduct_Prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ]
    )
    PairProductChain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | PairProductPromptTemplate
        | model2
        | StrOutputParser()
    )

    OrderDetail_Prompt = """You are Molly. You are female fashion advisor. And you are working for Styloland.
    Provide the user Order Information which they have asked. as per Content.
    If the user history is included, refer to the recent conversation from the history. If the user response is affirmative in response to a previously asked question about whether the user would like to see some products, then identify the keywords from the previous question/response.

    Content: `
    1. Blue Denim Jeans
        Delivery Time:3 Day
    2. Red Sleeveless T-Shirt
        Delivery Time:17 Hours
    `

    Answer Should in 50 words
    <question>
    {question}
    </question>
    Classification:"""

    OrderDetailPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", OrderDetail_Prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ]
    )
    OrderDetailChain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | OrderDetailPromptTemplate
        | model2
        | StrOutputParser()
    )

    HelpsFAQ_Prompt = """You are Molly. You are female fashion advisor. And you are working for Styloland.
    Provide the Help or Guidence to User. About Policies, Or Chatbot, Recommendation, Poject GUI, For Shopping From Styloland.
    If the user history is included, refer to the recent conversation from the history. If the user response is affirmative in response to a previously asked question about whether the user would like to see some products, then identify the keywords from the previous question/response.

    Company Policies: 
        1. return policy being- the recipient can return in 30 days
        2. while the refund policy would display options for credit cash ins, bank refunds, or buying another gift for the same price.

    Also provide Guidence If they want.

    Answer Should in 50 words
    <question>
    {question}
    </question>
    Classification:"""

    HelpsFAQPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", HelpsFAQ_Prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ]
    )
    HelpsFAQChain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | HelpsFAQPromptTemplate
        | model2
        | StrOutputParser()
    )

    FeedBack_Prompt = """You are Molly. You are female fashion advisor. And you are working for Styloland.
    Provide Feedback form with feedback message when user provide good bye message, if user's give ratting for product so provide Rating in format
    Feedback From : ‘<a href="/feedback" target="_blank">Feedback</a>
    If the user history is included, refer to the recent conversation from the history. If the user response is affirmative in response to a previously asked question about whether the user would like to see some products, then identify the keywords from the previous question/response.

    If user user give prodcut feedback so return given format. otherwise give simple output with feedback from URL

    Output Format: `Review={{"Product":ProductID,"Reting":Value,"ReviewMessage":ReviewMessage}}`
    Products Id:[11,22,33,44]
    Example:
        Question:Good By,
        Answer:Thank you, Have a nice day, Please share you feedback, <a href="/feedback" target="_blank">Feedback</a>
        Question:I'll Give 9 Out of 10 this second product
        Answer:Review={{"Product":22,"Reting":9/10,"ReviewMessage":""}}

    Answer Should in 50 words
    <question>
    {question}
    </question>
    Classification:"""

    FeedBackPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", FeedBack_Prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ]
    )
    FeedBackChain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | FeedBackPromptTemplate
        | model2
        | StrOutputParser()
    )

    General_Prompt = """You are Molly. You are female fashion advisor. And you are working for Styloland.
    Styloland is Virtual Shopping Mall, where user can shop ans show with friends, like multiuser game.
    this is Styloland link: <a href="https://styloland.com/">Styloland</a>

    Here user can asking about trends, shopping Product, pair Product, any helps

    this chatbot only Personal Female fashion Advisor, Don't give other Answer
    <question>
    {question}
    </question>
    Classification:"""

    GeneralPromptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", General_Prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ]
    )
    GeneralChain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | GeneralPromptTemplate
        | model2
        | StrOutputParser()
    )

    def function():
        print("This function is called")

    def verifyWord(word,x):
        print("Word : ",word," : ")
        if(word in x["topic"]):
            function()
        return word in x["topic"]

    branch = RunnableBranch(
        (lambda x: verifyWord("Greeting",x), GeneralChain),
        (lambda x: verifyWord("Shopping",x), ShoppingChain),
        (lambda x: verifyWord("ProductInfo",x), ProductInfoChain),
        (lambda x: verifyWord("Trends",x), TrendsChain),
        (lambda x: verifyWord("PairProduct",x), PairProductChain),
        (lambda x: verifyWord("OrderDetail",x), OrderDetailChain),
        (lambda x: verifyWord("HelpsFAQ",x), HelpsFAQChain),
        (lambda x: verifyWord("Feedback",x), FeedBackChain),
        GeneralChain,
    )


    full_chain = {"topic": intentChain, "question": lambda x: x["question"],"user_name": lambda x: x["user_name"]} | branch
    return full_chain
# def set_cate_list(data):
#     print("data ","*"*20,data)

# def intent(text,sender,client_ip,hist,data):
#     getData.printData()
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print("*"*20)
#     print(intentChain.invoke({"question":"good morning"}))
#     print(text,sender,client_ip,hist,data)
#     output = full_chain.invoke({"question": text,"user_name":sender})
#     print(output)
#     print(timestamp)
#     try:
#         ans = output
#         return json.dumps({"text":output}),timestamp,ans
#     except Exception as e:
#         ans = output.content
#         return json.dumps({"text":output.content}),timestamp,ans

# full_chain.invoke({"question":"tell me about my self what's i like?","user_name":"sushil mevada"})

def intent(text,sender):
    # getData.printData()
    memoryStorage = RedisChatMessageHistory(sender, url="redis://localhost:6379")


    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(text,sender)
    memory.chat_memory.messages = memoryStorage.messages
    print("Memory",memory.chat_memory.messages)
    memoryStorage.add_user_message(text)

    full_chain = openAiSearch(memory)
    output = full_chain.invoke({"question": text,"user_name":sender.split(".")[0]})
    print("LangChain Output:",output)
    print(timestamp)
    try:
        ans = output.content
        print("try message")
        memoryStorage.add_ai_message(output)
        # return json.dumps({"text":[output]}),timestamp,ans
        return output.content,timestamp,ans
        print("return messasge")
    except Exception as e:
        ans = output
        print("except message")
        memoryStorage.add_ai_message(output)
        return output,timestamp,ans


# while True:
#     query = input("Enter 0 for Exit\nEnter Your Query : ")
#     if query=="0":
#         break
#     inputs = {"question": query}
#     print(query)
#     memory.chat_memory.messages = memoryStorage.messages

#     memoryStorage.add_user_message(query)
#     output = full_chain.invoke({"question": query,"user_name":"sushil mevada"})
#     try:
#         print(output.content)
#         memoryStorage.add_ai_message(output.content)
#     except Exception as ex:
#         memoryStorage.add_ai_message(output)
#         print(output)