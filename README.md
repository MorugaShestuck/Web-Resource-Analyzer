# WRA - Web Resource Analyzer

![Python Version](https://img.shields.io/badge/Python-3.9-blue)

[//]: # (![License]&#40;https://img.shields.io/badge/license-MIT-green&#41;)

WRA (Web Resource Analyzer) is a tool for analyzing web resources, checking URLs for categories and themes, and more.

## Navigation

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
  - [Ping](#ping)
  - [Get Pages](#get-pages)
  - [Check URL](#check-url)
  - [Check URLs](#check-urls)
  - [Check Domain](#check-domain)
- [Docker Compose](#docker-compose)
- [Contributing](#contributing)
- [License](#license)

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://git.codenrock.com/kokoc-2023/cnrprod-team-58908/theme-web-resources-kokoc
cd theme-web-resources-kokoc
pip install -r requirements.txt
```

## Run

To run project locally, simple run `main.py` file:
```bash
python3 main.py
```

## Usage

To use WRA, you can run it locally or deploy it in a Docker container.

### Running Locally

```bash
python main.py
```

### Running with Docker Compose

You can also run WRA in a Docker container. Make sure you have Docker and Docker Compose installed. Then, run the following command:

```bash
docker-compose up
```

## Endpoints

### Ping

- **Endpoint:** `/ping`
- **Description:** Ping the server to check if it's running.
- **Method:** GET

### Get Pages

- **Endpoint:** `/get_pages`
- **Description:** Retrieve web pages starting from a given URL and a specified depth.
- **Method:** GET
- **Parameters:**
  - `url` (str): The starting URL.
  - `depth` (int, optional): The depth to crawl (default is 1).
- **Returns:** JSON containing the links retrieved.

### Check URL

- **Endpoint:** `/check_url`
- **Description:** Check a single URL for categories and themes.
- **Method:** GET
- **Parameters:**
  - `url` (str): The URL to check.
  - `depth` (int, optional): The depth for analysis (default is 1).
- **Returns:** JSON containing the categories and themes found.

### Check URLs

- **Endpoint:** `/check_urls`
- **Description:** Check multiple URLs for categories and themes.
- **Method:** POST
- **Parameters:**
  - `request_data` (Dict[str, List[str]]): JSON data with a list of URLs.
  - `depth` (int, optional): The depth for analysis (default is 1).
- **Returns:** JSON containing the results for each URL.

### Check Domain

- **Endpoint:** `/check_domain`
- **Description:** Check a domain for categories and themes based on its linked pages.
- **Method:** GET
- **Parameters:**
  - `url` (str): The URL of the domain.
  - `depth` (int, optional): The depth for analysis (default is 1).
- **Returns:** JSON containing the categories and themes found in the domain.

## Docker Compose

You can run WRA in a Docker container using Docker Compose. The Docker Compose configuration is provided in the `docker-compose.yml` file. To start the container, use the following commands:

```bash
docker-compose build
```

```bash
docker-compose up
```

[//]: # (## Contributing)

[//]: # ()
[//]: # (Contributions are welcome! Please feel free to submit issues or pull requests.)

[//]: # ()
[//]: # (## License)

[//]: # ()
[//]: # (This project is licensed under the MIT License. See the [LICENSE]&#40;LICENSE&#41; file for details.)

[//]: # (```)
