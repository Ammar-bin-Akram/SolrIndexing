from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

SOLR_URL = 'http://localhost:8983/solr/jcgArticles/select'

# Solr search view
def solr_search(request):
    query = request.GET.get('q', '')  # Search query
    category = request.GET.get('category', '')  # Filter by category
    author = request.GET.get('author', '')  # Filter by author

    # Construct Solr query string
    solr_query = f"title:{query}*" if query else "*:*"  # Wildcard for title matching

    params = {
        'q': solr_query,
        'wt': 'json',  # JSON response format
        'rows': 20  # Limit results
    }

    # Add filters (category and author) if present
    fq = []
    if category:
        fq.append(f"category:{category}")
    if author:
        fq.append(f"author:{author}")
    
    if fq:
        params['fq'] = fq  # Add filter queries to params

    try:
        # Make request to Solr
        response = requests.get(SOLR_URL, params=params)
        data = response.json()  # Parse response
        return JsonResponse(data['response']['docs'], safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Failed to fetch data from Solr', 'details': str(e)})


def home(request):
    return render(request, 'search.html')


def autocomplete(request):
    query = request.GET.get('q', '')
    category = request.GET.get('filter', '')

    solr_url = 'http://localhost:8983/solr/jcgArticles/select'  # Update with your Solr core name

    params = {
        'q': f'text:{query}*',        # Wildcard for autocomplete
        'wt': 'json',
        'rows': 5,
        'fl': 'title',
                            # Only fetch title (or your suggestion field)
    }

    # If a category filter is provided, add it to the query
    if category:
        params['fq'] = f'category:{category}'

    try:
        response = requests.get(solr_url, params=params)
        data = response.json()
        suggestions = [doc['title'] for doc in data['response']['docs']]
        return JsonResponse({'suggestions': suggestions})
    except Exception as e:
        print("Autocomplete error:", e)
        return JsonResponse({'suggestions': []})


