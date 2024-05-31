import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Configuration
username = 'your_username'
password = 'your_passowrd'
login_url = 'https://leetcode.com/accounts/login/'
submissions_url = 'https://leetcode.com/submissions/#/1' #here you can scroll different pages by change #/i  for all i that exists

# Function to log in to LeetCode
def login(driver, username, password):
    driver.get(login_url)

    time.sleep(3)  # Wait for the page to load completely

    # Find and fill the username field
    username_field = driver.find_element(By.ID, 'id_login')
    username_field.send_keys(username)

    # Find and fill the password field
    password_field = driver.find_element(By.ID, 'id_password')
    password_field.send_keys(password)

    # Submit the login form
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)  # Wait for the login to complete

# Function to get solved problems
def get_solved_problems(driver):
    driver.get(submissions_url)
    time.sleep(3)  # Wait for the page to load completely

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'class': 'table table-striped table-bordered table-hover'})
    hrefs = []
    problems = []
    for row in table.find_all('tr'):
        anchor = row.find('a',class_='text-success' ,href=True)
        problem =row.find('a', href=True)
        if (anchor and problem):
            hrefs.append(anchor['href'])
            problems.append(problem.text)
            

    for href,problem in zip(hrefs,problems):
        print(href)
        print(problem)
        code =get_solution_code(driver,href)
        filename = os.path.join("leetcode_solutions", f"{problem.replace(' ', '_')}.java")
        with open(filename, 'w') as file:
            # Find the index of the class name in the Java code string
            class_index = code.find("Solution")
            # Replace the class name with the actual problem name
            modified_java_code = code[:class_index] + f"{problem.replace(' ', '_')}" + code[class_index + len("Solution"):]
            file.write(modified_java_code)
        print(f"Saved {filename}")
# Function to get solution code
def get_solution_code(driver, title_slug):
    problem_url = f'https://leetcode.com{title_slug}'
    driver.get(problem_url)
    time.sleep(3)  # Wait for the page to load completely
    code=extract_code(driver.page_source)
    return code
def extract_code(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the text from the HTML
    code_lines = soup.find_all('div', class_='ace_line')
    java_code = '\n'.join([line.get_text() for line in code_lines])
    print(java_code)
    return java_code
def save_solutions(directory='leetcode_solutions'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()
    login(driver, username, password)
    get_solved_problems(driver)
    driver.quit()


save_solutions()
