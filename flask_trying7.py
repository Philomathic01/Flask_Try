from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('Index.html')

@app.route('/search', methods=['POST'])
def search():
    api_url = "https://www.federalregister.gov/api/v1/documents.json"
    params = {
        "per_page": request.form.get('per_page', 100),
        "order": "newest"
    }

    # Add parameters based on the user input
    if 'include_term' in request.form:
        params["conditions[term]"] = request.form.get('term', '')

    if 'include_section' in request.form:
        params["conditions[sections][]"] = request.form.get('section')

    if 'include_topic' in request.form:
        params["conditions[topics][]"] = request.form.get('topic')

    if 'include_cfr_title' in request.form:
        params["conditions[cfr][title]"] = request.form.get('cfr_title')

    if 'include_cfr_part' in request.form:
        params["conditions[cfr][part]"] = request.form.get('cfr_part')

    if 'include_significant' in request.form:
        params["conditions[significant]"] = request.form.get('significant')

    if 'include_dates' in request.form:
        params["conditions[publication_date][gte]"] = request.form.get('start_date')
        params["conditions[publication_date][lte]"] = request.form.get('end_date')

    if 'include_effective_year' in request.form:
        params["conditions[effective_date][year]"] = request.form.get('effective_year')
    
    if 'include_publication_year' in request.form:
        params["conditions[publication_date][year]"] = request.form.get('publication_year')

    # Fetch the API response
    response = requests.get(api_url, params=params)

    # Process the response
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
    else:
        results = []

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
