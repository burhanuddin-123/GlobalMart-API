## refer:- BasicAuth:- https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
# https://betterprogramming.pub/a-beginner-friendly-introduction-to-fastapi-security-d8f69a259804
# https://itsjoshcampos.codes/fast-api-api-key-authorization
## Metadata:- https://fastapi.tiangolo.com/tutorial/metadata/
# pagination:- https://nordicapis.com/everything-you-need-to-know-about-api-pagination/

## Fast API:- https://fastapi.tiangolo.com/tutorial/dependencies/


from typing import Union
from fastapi import Depends, FastAPI #, HTTPException, status
from paginate import paginate
# New Imports for app.py
from fastapi.security.api_key import APIKey
from fastapi.responses import HTMLResponse
import auth
# from fastapi.middleware.cors import CORSMiddleware

description = """
## Industry Background:
ECommerce is one of the most successful businesses of modern times. The likes of **Amazon**, **Flipkart**, **Myntra**, etc. have made 
multi-billion-dollar businesses by making the whole process of searching, buying, and returning products extremely simple for 
the end user. These companies heavily rely on technology and specifically data to personalize the shopping experience of their 
customers. Retail over the years has become one of the most mature industries and has seen many applications of data-driven 
decision-making to squeeze in as much margin as possible and at the same time engage the customers so well E-commerce has taken this 
to the next level but virtualizing the whole shopping experience through apps. As an industry heavily driven by data, there are a lot 
of interesting problem statements that ECommerce companies work on

<h1>Problem Statement:</h1>
Global Mart is one of the leading e-Commerce giants with a presence in North America and Europe region. It has a presence across 120 
markets and primarily deals with 3 lines of business: 

<ul>
    <li>Technology,</li>
    <li>Office Supplies,</li> 
    <li>and Furniture.</li>
</ul>

With an increase in customers and expansion in geography, GlobalMart has developed tie-ups with several local vendors to help them 
deliver their products to the end customers. 

<ul>
    <li>There has been a rapid increase in customers. Because of this the amount of data being generated has been rapidly increasing
    <li>Because of this, the overhead of maintaining servers, Difficulty in creating and capture of reports, management of data and manually cleaning them, etc. data teams have got overwhelming issues
    <li>The Management is pushing for a full-length application to capture all relevant data points easily and efficiently. This would mean there will be a front-end web and mobile application. This would only add further load on databases which will be the backend. Hence there is a high need for autoscaling the backend as and when required.
    <li>The company is also planning to expand its product offerings. With a variety of product types, it is no longer feasible for them to have a fixed schema
    <li>The data structure to store product-related information needs to be more flexible to be able to accommodate changing insurance types and their rules & regulations
    <li>The company does not have a clean and processed store of data. There is no single source of truth. With the growing dependency on data, GlobalMart wishes to have a single source of truth developed and deployed so that they can leverage all the data and enhance the business.
</ul>


The Customer Sales Team at GlobalMart is tasked with the responsibility of ensuring that the sales experience of the customers is fast
and hassle-free. Any factor leading to a bad experience for a customer is taken very seriously and steps are taken to fix the same. 
The Sales Team prepares several reports to be shared with the VP, of Sales Operations on a week-on-week basis. Some of the metrics to 
be covered would be:

<ul>
    <li>No of orders by customer
    <li>Sales Value
    <li>On-time delivery
</ul>


<h1>Your Responsibilities:</h1>
Fetch the GlobalMart data from the given API, and fetch useful insights out of that.
<br>
"""

tags_metadata = [
    {
        "name": "Sales",
        "description": 
                "<font size=3px>Returns the GlobalMart data containing the transactions, products, orders, customers and vendors data.\
                Carefully go through the data element in the response, and fetch the data out of that. Whole globalmart data is divided\
                into different pages, each page has metadata in response\
                such as **count**, **limit, next_page**, **previous_page**. There are 2 parameters called <b>offset</b> and <b>limit</b>. By default\
                offset is set to **1** and limit is set to **30**. And max limit can be set to **100**. Records more than 100 won't be return\
                by API. If we pass the limit more then 100 then also API will return the 100 records.</font>",

        "externalDocs": {
            "description": "Go through this link to understand the Pagination",
            "url": "https://nordicapis.com/everything-you-need-to-know-about-api-pagination/",
        },
    },
]

app = FastAPI(
    title="GlobalMart",
    description=description,
    version="0.0.1",
    contact={
        "name": "Mentorskool",
        "url": "https://www.mentorskool.com/",
        "email": "learn@mentorskool.com",
    },
    openapi_tags=tags_metadata
)

# origins=["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     alow_methods=["*"],
#     allow_headers=["*"]
# )

html_response = """
        <h1> Endpoints: </h1>
        <font size=5px>
        <ol>
            <li> Document Endpoint: <b><u><a href="/docs">/docs</a></u></b>
            <li> API Endpoint: <b><u><a href="/mentorskool/v1/sales">/mentorskool/v1/sales<a></u></b>
            <li> Readable Document: <b><u><a href="/redoc">/redoc</a></u></b>
        </ol>
        </font>
    """

@app.get('/')
async def index():
    return HTMLResponse(content=html_response, status_code=200)


# Lockedown Route
@app.get("/mentorskool/v1/sales", tags=["Sales"], dependencies=[Depends(auth.get_api_key)])
## Union:- https://www.reddit.com/r/Python/comments/vcvyok/unionstr_none_vs_optionalstr/
async def read_current_user(offset: Union[int, None] = None, limit: Union[int, None] = None):
    if not offset:
        offset = 1
    
    if limit is None:
        limit=30
    elif limit>100:
        limit=100
    
    if offset < 0 or limit < 0:
        return {"message": "Pass the valid values for parameters"}
    final_data = paginate(offset, limit)

    # return {"message": "Fetch successfully!!"}
    if final_data.get("message"):
        return final_data
    else:
        return final_data


### Runs the file using following command:- uvicorn <file_name>:app --reload, Ex:- uvicorn main:app --reload