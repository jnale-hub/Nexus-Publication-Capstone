from django.shortcuts import render
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse
import requests
from django.core.paginator import Paginator

def index(request):
    # Get the search query parameter
    search = request.GET.get('search')

    # List of categories
    categories = ['Business', 'Technology', 'Entertainment', 'Sports', 'Science', 'Health']

    # Set the default API URL for top headlines
    api_url = "https://newsapi.org/v2/top-headlines?language={}&apiKey={}".format("en", settings.APIKEY)

    # Override the API URL for search queries
    if search:
        api_url = "https://newsapi.org/v2/everything?q={}&sortBy={}&apiKey={}".format(search, "popularity", settings.APIKEY)

    try:
        # Send GET request to the API URL
        response = requests.get(url=api_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse the JSON response
        data = response.json()

        # Check if the response status is ok
        if data.get("status") != "ok":
            return HttpResponse("<h1>Request Failed</h1>")

        # Extract the articles from the data
        articles = data.get("articles", [])

        # Define a function to format the date and get the image URL
        def format_article_data(article):
            # Format the date
            published_date = datetime.strptime(article.get("publishedAt"), "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = published_date.strftime("%B %d, %Y")

            # Get the image URL or use a default image
            image_url = article.get("urlToImage") or settings.DEFAULT_IMAGE

            return {
                "title": article.get("title"),
                "description": article.get("description", ""),
                "url": article.get("url"),
                "image": image_url,
                "publishedat": formatted_date
            }

        # Process articles for both 'headline' and 'data' lists
        context = {
            "success": True,
            "headline": [format_article_data(article) for article in articles[:3]],
            "search": search,
            "categories": categories
        }

        # Add pagination for 'data' list
        paginator = Paginator([format_article_data(article) for article in articles[3:]], per_page=12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj

        # Send the news feed to the template in the context
        return render(request, 'world_news/index.html', context=context)

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"<h1>Request Failed: {e}</h1>")
    except ValueError as e:
        return HttpResponse(f"<h1>Failed to parse JSON response: {e}</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>An unexpected error occurred: {e}</h1>")
