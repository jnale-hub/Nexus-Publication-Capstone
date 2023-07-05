from django.shortcuts import render
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse

def index(request):
    # Get the search query parameter
    search = request.GET.get('search')

    # List of categories
    categories = ['Business', 'Technology', 'Entertainment', 'Sports', 'Science', 'Health']

    # Set the default API URL for top headlines
    api_url = "https://newsapi.org/v2/top-headlines?country={}&apiKey={}".format("us", settings.APIKEY)

    # Override the API URL for search queries
    if search:
        api_url = "https://newsapi.org/v2/everything?q={}&sortBy={}&apiKey={}".format(search, "popularity", settings.APIKEY)

    # Send GET request to the API URL
    response = requests.get(url=api_url)

    # Check if the request was successful
    if response.status_code != 200:
        return HttpResponse("<h1>Request Failed</h1>")

    # Parse the JSON response
    data = response.json()

    # Check if the response status is ok
    if data.get("status") != "ok":
        return HttpResponse("<h1>Request Failed</h1>")

    # Extract the articles from the data
    articles = data.get("articles", [])

    # Initialize the context dictionary
    context = {
        "success": True,
        "headline": [],
        "data": [],
        "search": search,
        "categories": categories
    }

    for i, article in enumerate(articles[:3]):  # Limit to 3 items
        # Format the date
        published_date = datetime.strptime(article.get("publishedAt"), "%Y-%m-%dT%H:%M:%SZ")
        formatted_date = published_date.strftime("%B %d, %Y")

        # Get the image URL or use a default image
        image_url = article.get("urlToImage") or settings.DEFAULT_IMAGE

        # Add the news data to the 'headline' list in the context
        context["headline"].append({
            "title": article.get("title"),
            "description": article.get("description", ""),
            "url": article.get("url"),
            "image": image_url,
            "publishedat": formatted_date
        })

    for i, article in enumerate(articles[3:15]):  # Limit to 12 items
        # Format the date
        published_date = datetime.strptime(article.get("publishedAt"), "%Y-%m-%dT%H:%M:%SZ")
        formatted_date = published_date.strftime("%B %d, %Y")

        # Get the image URL or use a default image
        image_url = article.get("urlToImage") or settings.DEFAULT_IMAGE

        # Add the news data to the 'data' list in the context
        context["data"].append({
            "title": article.get("title"),
            "description": article.get("description", ""),
            "url": article.get("url"),
            "image": image_url,
            "publishedat": formatted_date
        })

    # Send the news feed to the template in the context
    return render(request, 'world_news/index.html', context=context)
