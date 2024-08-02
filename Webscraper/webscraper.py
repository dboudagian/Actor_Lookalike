from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import pyautogui
import time


actors = [
    "Meryl Streep", "Viola Davis", "Jennifer Lawrence", "Natalie Portman", 
    "Scarlett Johansson", "Cate Blanchett", "Emma Stone", "Sandra Bullock", 
    "Julia Roberts", "Anne Hathaway", "Charlize Theron", "Angelina Jolie", 
    "Reese Witherspoon", "Nicole Kidman", "Amy Adams", "Halle Berry", 
    "Rachel McAdams", "Jessica Chastain", "Margot Robbie", "Emily Blunt", 
    "Gal Gadot", "Saoirse Ronan", "Lupita Nyong'o", "Keira Knightley", 
    "Julianne Moore", "Tilda Swinton", "Olivia Colman", "Kristen Stewart", 
    "Zendaya", "Emma Watson", "Brie Larson", "Michelle Williams", 
    "Rosamund Pike", "Elisabeth Moss", "Laura Dern", "Regina King", 
    "Carey Mulligan", "Jennifer Aniston", "Kate Winslet", "Salma Hayek", 
    "Thandiwe Newton", "Helena Bonham Carter", "Robin Wright", 
    "Anna Kendrick", "Jodie Foster", "Helen Mirren", "Penélope Cruz", 
    "Allison Janney", "Emily Mortimer", "Sarah Paulson", "Octavia Spencer", 
    "Taraji P. Henson", "Felicity Jones", "Alicia Vikander", "Eva Green", 
    "Kristen Bell", "Mila Kunis", "Sofia Vergara", "Priyanka Chopra", 
    "Blake Lively", "Lucy Liu", "Kristen Wiig", "Isla Fisher", 
    "Lily Collins", "Zoe Saldana", "Dakota Johnson", "Margot Robbie", 
    "Gal Gadot", "Scarlett Johansson", "Emma Stone", "Jennifer Lawrence", 
    "Brie Larson", "Charlize Theron", "Natalie Portman", "Anne Hathaway", 
    "Emily Blunt", "Saoirse Ronan", "Keira Knightley", "Jessica Chastain", 
    "Amy Adams", "Rachel McAdams", "Reese Witherspoon", "Nicole Kidman", 
    "Sandra Bullock", "Angelina Jolie", "Julia Roberts", "Emma Watson", 
    "Michelle Williams", "Kate Winslet", "Julianne Moore", "Tilda Swinton", 
    "Olivia Colman", "Kristen Stewart", "Zendaya", "Jennifer Aniston", 
    "Salma Hayek", "Thandiwe Newton", "Helena Bonham Carter", "Robin Wright", 
    "Anna Kendrick", "Jodie Foster", "Helen Mirren", "Penélope Cruz", 
    "Allison Janney", "Emily Mortimer", "Sarah Paulson", "Octavia Spencer", 
    "Taraji P. Henson", "Felicity Jones", "Alicia Vikander", "Eva Green", 
    "Kristen Bell", "Mila Kunis", "Sofia Vergara", "Priyanka Chopra", 
    "Blake Lively", "Lucy Liu", "Kristen Wiig", "Isla Fisher", "Lily Collins", 
    "Zoe Saldana", "Dakota Johnson", "Leonardo DiCaprio", "Brad Pitt", 
    "Johnny Depp", "Robert Downey Jr.", "Tom Hanks", "Denzel Washington", 
    "Matt Damon", "George Clooney", "Will Smith", "Christian Bale", 
    "Hugh Jackman", "Chris Hemsworth", "Chris Evans", "Ryan Reynolds", 
    "Ryan Gosling", "Jake Gyllenhaal", "Tom Cruise", "Harrison Ford", 
    "Daniel Craig", "Joaquin Phoenix", "Edward Norton", "Mark Ruffalo", 
    "Ben Affleck", "Robert Pattinson", "Timothée Chalamet", "Adam Driver", 
    "Michael B. Jordan", "Chadwick Boseman", "Matthew McConaughey", 
    "Bradley Cooper", "Steve Carell", "Steve Buscemi", "Jeff Bridges", 
    "Jeff Goldblum", "Bill Murray", "Tom Hardy", "Javier Bardem", 
    "Jared Leto", "Oscar Isaac", "Jason Momoa", "Idris Elba", 
    "Keanu Reeves", "Chris Pratt", "Vin Diesel", "Paul Rudd", 
    "Mahershala Ali", "Willem Dafoe", "Viggo Mortensen", "Ralph Fiennes", 
    "Ethan Hawke", "John Goodman", "Colin Firth", "Gary Oldman", 
    "Clint Eastwood", "Morgan Freeman", "Samuel L. Jackson", 
    "Liam Neeson", "Daniel Day-Lewis", "Sean Penn", "Robin Williams", 
    "Robert De Niro", "Al Pacino", "Jack Nicholson", "Anthony Hopkins", 
    "Tommy Lee Jones", "Kevin Spacey", "Kevin Bacon", "William H. Macy", 
    "Ben Kingsley", "Kenneth Branagh", "Jeremy Irons", "Ian McKellen", 
    "Patrick Stewart", "Hugh Grant", "Hugh Laurie", "Ewan McGregor", 
    "Sam Rockwell", "J.K. Simmons", "Forest Whitaker", "Terrence Howard", 
    "Don Cheadle", "Jamie Foxx", "Jon Hamm", "John C. Reilly", "Zach Galifianakis"
]


# Configure WebDriver options
options = ChromeOptions()
user_data_dir = '/Users/danielboudagian/Library/Application Support/Google/Chrome'  # Ensure the path is correct
profile_dir = 'DB'  # Replace with your profile directory if different

options.add_argument(f'--user-data-dir={user_data_dir}')
options.add_argument(f'--profile-directory={profile_dir}')

# Launch Browser
driver = webdriver.Chrome(options=options)
driver.maximize_window()  # Maximize window to ensure all elements are visible

# Give some time for the browser to open and get focus
time.sleep(5)

# actors = ["margot", "bird"]

for index, actor in enumerate(actors):

    # Navigate to Google
    driver.get('https://www.google.com')

    # Give some time for the page to load
    time.sleep(2)

    # Find the search box element by its name attribute
    search_box = driver.find_element(By.NAME, 'q')

    # Type the search query into the search box
    search_query = actor
    search_box.send_keys(search_query)

    # Submit the search query
    search_box.send_keys(Keys.RETURN)

    # Give some time for the search results to load
    time.sleep(5)

    # Move the mouse cursor to a specific position (e.g., the middle of the screen)
    # Note: Adjust the coordinates as needed
    screen_width, screen_height = pyautogui.size()
    target_position = (screen_width // 2, screen_height // 2)
    pyautogui.moveTo(256, 260, duration=1)

    # Optionally, click at the new position
    pyautogui.click()

    time.sleep(3)
    pyautogui.moveTo(1300, 75, duration=1)
    
    pyautogui.click()

    time.sleep(3)

    pyautogui.moveTo(1200, 258, duration=1)

    pyautogui.click()

    time.sleep(3)

    pyautogui.moveTo(1200, 130, duration=1)

    time.sleep(1)

    pyautogui.click()

    time.sleep(1)
    
    # select all again

    pyautogui.moveTo(180, 360, duration=1)

    pyautogui.click()
    
    
    # moves to download selected
    time.sleep(4)

    pyautogui.moveTo(480, 360, duration=1)

    pyautogui.click()
    
    time.sleep(1)
    
    pyautogui.moveTo(635, 360, duration=1)
    
    pyautogui.click()
    
    time.sleep(3)
    
    
    # pyautogui.press('delete')
    
    for _ in range(60):
        pyautogui.press('backspace')
    
    pyautogui.typewrite("Imager/"+ actor)
    
    pyautogui.moveTo(1200, 450, duration=1)

    time.sleep(1)

    pyautogui.click()
    
    
    
    

    time.sleep(30)
