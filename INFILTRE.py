import requests
import concurrent.futures
import argparse
import time
from urllib.parse import urljoin
from datetime import datetime
import logging
from termcolor import colored
import random
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_sensitive_file(content):
    
    sensitive_keywords = [
        "APP_KEY", "DB_HOST", "DB_USERNAME", "DB_PASSWORD", "API_KEY", "SECRET",
        "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "DATABASE_URL", "MYSQL_ROOT_PASSWORD",
        "MONGO_URI", "REDIS_PASSWORD", "SESSION_SECRET", "JWT_SECRET", "SMTP_PASSWORD",
        "CLIENT_SECRET", "ACCESS_TOKEN", "AUTH_TOKEN", "DATABASE_PASSWORD", "FTP_PASSWORD"
    ]
    return any(keyword in content for keyword in sensitive_keywords)

def test_file_access(base_url, file_path, proxies=None, timeout=5):
    full_url = urljoin(base_url, file_path)
    try:
        response = requests.get(full_url, proxies=proxies, timeout=timeout, allow_redirects=False)
        if response.status_code == 200:
            if is_sensitive_file(response.text):
                logging.info(colored(f"[+] Accessible and sensitive file: {full_url}", "green"))
                logging.info(f"[*] Content (first 500 characters):\n{response.text[:500]}...\n")
                return full_url, response.text[:500]
            else:
                logging.warning(colored(f"[!] Accessible file but not sensitive: {full_url}", "yellow"))
                return full_url, "Not sensitive"
        elif response.status_code == 403:
            logging.debug(colored(f"[-] Access denied (403): {full_url}", "red"))
        elif response.status_code == 404:
            logging.debug(colored(f"[-] File not found (404): {full_url}", "red"))
        else:
            logging.debug(colored(f"[-] HTTP Status {response.status_code}: {full_url}", "red"))
    except requests.exceptions.RequestException as e:
        logging.error(colored(f"[!] Error connecting to {full_url}: {e}", "red"))
    return None, None

def load_wordlist(wordlist_file):
    try:
        with open(wordlist_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error(colored(f"[!] Wordlist file not found: {wordlist_file}", "red"))
        return []

def handle_rate_limiting(response):
    if response.status_code == 429:
        logging.warning(colored(f"[-] Rate limiting detected, sleeping...", "yellow"))
        time.sleep(random.uniform(5, 10))

def validate_proxy(proxies):
    try:
        test_url = "http://www.google.com"
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            logging.info(colored(f"[*] Proxy validated successfully: {proxies['http']}", "blue"))
        else:
            logging.error(colored(f"[!] Proxy validation failed with status: {response.status_code}", "red"))
            return None
    except requests.RequestException as e:
        logging.error(colored(f"[!] Error validating proxy: {e}", "red"))
        return None
    return proxies

def main():
    parser = argparse.ArgumentParser(description="Advanced script to test access to sensitive files.")
    parser.add_argument("-u", "--url", required=True, help="Base URL of the site (e.g. https://example.com)")
    parser.add_argument("-w", "--wordlist", default=None, help="Wordlist file with file paths to test (e.g. wordlist.txt)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads for requests (default: 10)")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Delay between requests in seconds (default: 0)")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file for saving results (default: results.txt)")
    parser.add_argument("-p", "--proxy", default=None, help="Proxy to use (e.g. http://127.0.0.1:8080)")
    parser.add_argument("--timeout", type=int, default=5, help="Timeout for requests in seconds (default: 5)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    base_url = args.url
    wordlist_file = args.wordlist
    num_threads = args.threads
    delay = args.delay
    output_file = args.output
    timeout = args.timeout
    verbose = args.verbose

    proxies = None
    if args.proxy:
        proxies = {"http": args.proxy, "https": args.proxy}
        logging.info(colored(f"[*] Using proxy: {args.proxy}", "blue"))
        proxies = validate_proxy(proxies)
        if not proxies:
            return

    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        logging.error(colored("[!] The URL must start with http:// or https://", "red"))
        return

    if wordlist_file:
        files_to_test = load_wordlist(wordlist_file)
    else:
        logging.info(colored("No wordlist specified. Use manual input.", "blue"))
        files_to_test = []
        while True:
            file_path = input("File (e.g., .env, config.php, etc.): ").strip()
            if file_path == "":
                if len(files_to_test) == 0:
                    print(colored("[!] Please enter at least one file to test.", "red"))
                    continue
                break
            files_to_test.append(file_path)

    if ".env" not in files_to_test:
        files_to_test.append(".env")
        logging.info(colored("[*] Added .env to the default list.", "blue"))

    logging.info(colored(f"[*] Files to test: {len(files_to_test)}", "blue"))
    logging.info(colored(f"[*] Base URL: {base_url}", "blue"))
    logging.info(colored(f"[*] Threads: {num_threads}, Delay: {delay}s, Timeout: {timeout}s", "blue"))

    results = []

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_file = {executor.submit(test_file_access, base_url, file_path, proxies, timeout): file_path
                          for file_path in files_to_test}

        for future in concurrent.futures.as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                result_url, result_content = future.result()
                if result_url and result_content:
                    results.append((result_url, result_content))
                if verbose:
                    logging.debug(f"Tested {file_path} with result {result_url}")
            except Exception as e:
                logging.error(colored(f"[!] Error testing {file_path}: {e}", "red"))

            if delay > 0:
                time.sleep(delay)

    end_time = time.time()
    logging.info(colored(f"[*] Scan completed in {end_time - start_time:.2f} seconds.", "blue"))

    if results:
        output_filename = f"{os.path.splitext(output_file)[0]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(output_filename, 'a') as f:
            f.write(f"\n=== Scan from {datetime.now()} ===\n")
            f.write(f"Base URL: {base_url}\n")
            f.write(f"Files found: {len(results)}\n\n")
            for url, content in results:
                f.write(f"File: {url}\nContent:\n{content}\n{'='*50}\n")
        logging.info(colored(f"[*] Results saved in {output_filename}", "green"))
    else:
        logging.info(colored("[*] No sensitive files found.", "yellow"))
        logging.info(colored("[*] Files tested:", "blue"))
        for file in files_to_test:
            logging.info(f"  - {file}")

if __name__ == "__main__":
    main()