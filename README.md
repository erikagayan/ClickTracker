# ClickTracker

Click Tracker is a Django application for tracking user clicks on links. It allows creating shortened URLs, redirecting users to original URLs, and configuring "Thank You" pages.

## Installation
1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
   
2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
   
3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```
   
5. Start the development server:

    ```bash
    python manage.py runserver
    ```


## Usage

### Creating a Shortened URL
#### To create a shortened URL, send a POST request to http://127.0.0.1:8000/api/shorturls/ with the request body:
```json
{
  "original_url": "https://www.google.com"
}
```

### Updating the "Thank You" Page
#### To update the "Thank You" page URL, send a PATCH request to http://127.0.0.1:8000/api/shorturls/{id}/update_thank_you_page/ with the request body:
```json
{
  "thank_you_page": "https://www.example.com/thank-you"
}
```

### Redirecting with a Shortened URL
#### Navigate to the URL http://127.0.0.1:8000/s/{short_code}/, where {short_code} is the code generated for the shortened URL. The user will be redirected to the original URL or to the "Thank You" page if it is specified.


## API
### Create a Shortened URL
- **URL**: `http://127.0.0.1:8000/api/shorturls/`
- **Method**: `POST`
- **Request Body**:
```json
{
  "original_url": "https://www.google.com"
}
```
- **Response**:
```json
{
  "id": 1,
  "original_url": "https://www.google.com",
  "short_code": "abc123",
  "thank_you_page": null
}
```

### Update the "Thank You" Page
- **URL**: `http://127.0.0.1:8000/api/shorturls/{id}/update_thank_you_page/`
- **Method**: `PATCH`
- **Request Body**:
```json
{
  "thank_you_page": "https://www.example.com/thank-you"
}
```
- **Response**:
```json
{
  "status": "thank you page updated"
}
```

### Redirect with a Shortened URL
- **URL**: `http://127.0.0.1:8000/s/{short_code}/`
- **Method**: `GET`
- **Response**: Redirect to the original URL or the "Thank You" page.