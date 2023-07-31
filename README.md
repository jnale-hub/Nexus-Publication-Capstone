# CAPSTONE - Nexus-Publication
#### Demo video:  <>

Hi there!

This is my Final Project for the course CS50’s Web Programming with Python and JavaScript. It is built with Django, HTML, CSS, JavaScript, Python, and Bootstrap.

"Nexus Publication" is the name of my college's school paper, so I decided to create a web app that features articles, a game section, and the ability to browse world news.

The main inspiration for this project is The New York Times Games; I enjoy playing wordle, and I tried to create my own version of it. Additionally, I thought it would be great to have a web app for my school paper that also includes a games section.

## Distinctiveness and Complexity

I believe this project satisfies the distinctiveness and complexity requirements because this project contains three main apps with different functionalities and I build this web application for my local college publication. 

The "Nexus Pub" app deals with news articles, authors, categories, comments, and user profiles. 

The "Nexus Games" app offers a gaming experience with a scoring system and user rankings. 

The "Nexus World News" utilizes news API to fetch real-time news data from around the world, allowing users to search for news by category or query. 

## Main Apps:

### 1. Nexus Publication App

#### Description

In this app, an admin can post articles with its respective data from staffs and categorize it. The user can star and save articles, they can also view and read the whole article, and add and view comments on it.

#### Models

1. **User Model**:
   - Represents a user in the system, extending `AbstractUser`.
   - Fields:
     - `name`: Character field for the user's name.
     - `points`: Integer field to track the user's points in the games, default value is 0.
     - `picture`: URL field to store the user's profile picture, default is set to `settings.DEFAULT_PROFILE`.
     - `saved_articles`: Many-to-many relationship with the `Article` model, allowing users to save articles, related name is `saved_by`.
     - `starred_articles`: Many-to-many relationship with the `Article` model, allowing users to star articles, related name is `starred_by`.

2. **Staff Model**:
   - Fields:
     - `name`: Character field for the staff member's name.
     - `position`: Character field for the staff member's position (optional, can be blank).
     - `picture`: URL field to store the staff member's picture, default is set to `settings.DEFAULT_PROFILE`.
     - `description`: Text field for staff member description.
     - `email`: Email field for staff member contact.

3. **Category Model**:
   - Field:
     - `category`: Character field for the category name.

4. **Article Model**:
   - Fields:
     - `title`: Character field for the article title.
     - `description`: Character field for the article description (optional, can be blank).
     - `category`: Foreign key to the `Category` model, for article categorization, with `on_delete=models.CASCADE`.
     - `author`: Foreign key to the `Staff` model, representing the article author, with `on_delete=models.CASCADE`.
     - `date_published`: Date field for the article's publication date.
     - `content`: Text field for the article's content (optional, can be null).
     - `image`: URL field for the article's image, default is set to `settings.DEFAULT_IMAGE`.

5. **Comment Model**:
   - Fields:
     - `content`: Text field for the comment content.
     - `user`: Foreign key to the `User` model, representing the commenter, with `on_delete=models.CASCADE`.
     - `article`: Foreign key to the `Article` model, for which the comment belongs, with `on_delete=models.CASCADE`.
     - `date`: Date-time field for the comment date, auto-generated.

#### Features

This app incorporates the following features:

1. **Category Filter**: Users can filter articles by category, enabling them to view articles specific to their interests.

2. **Date Filtering**: Users can apply date filtering to find articles published within a particular timeframe.

3. **Query Search**: A search functionality that allows users to enter keywords and retrieve articles matching their search queries.

4. **Save Article**: Users have the option to save articles for later reading, making it convenient to access content of interest.

5. **Star Article**: Users can star articles to mark them as favorites, making it easy to revisit and keep track of preferred content.

6. **Pagination**: The application implements pagination, ensuring that articles are presented in manageable and navigable chunks, improving user experience.

7. **Edit Profile**: Users can edit their profile information, allowing them to update details like name, profile picture, and email for better personalization.

#### Pages

1. **Index Page**:
   - This page displays all news articles sorted by the date of publication.
   - It features a Bootstrap carousel showcasing the headline of the newest article from each category.
   
2. **Article Page**:
   - When a user clicks on an article, they are directed to this page to view the complete story.
   - The page includes a comment section that allows users to toggle the visibility of comments.
   - Comments are paginated for easier navigation.

3. **Staff Page**:
   - This page provides information about staff members.
   - It displays details such as name, position, picture, description, and email.

4. **Saved / Starred Article Page**:
   - This page presents a collection of articles that the user has saved or starred for future reference.
   - Users can access their saved and starred articles conveniently in one place.

#### File Structure

The application's file structure is organized as follows:

1. **nexus_pub/**:
   - `__init__.py`: A Python package file indicating that the directory is a Python package.
   - `admin.py`: Contains Django admin site configurations for managing application models.
   - `apps.py`: Configurations related to the Django app, such as the app name and settings.
   - `models.py`: Defines the application's database models, including the `User`, `Staff`, `Category`, `Article`, and `Comment` models.
   - `tests.py`: Contains unit tests for the application.
   - `urls.py`: Defines URL patterns and their corresponding view functions.
   - `views.py`: Contains view functions that handle HTTP requests and generate responses.

2. **nexus_pub/templates/**:
   - Templates include:
     - `nexus_pub/layout.html`: Base template that defines the overall structure of other pages.
     - `nexus_pub/minimal.html`: A minimal template to use in a minimal view of articles, I use `{% include %}` function to be more flexible. Used in star and saved articles page.
     - `nexus_pub/modals.html`: Template for displaying modals such as the `log in`, `register`, `user profile`, `edit profile`, and `filter date` modal.
     - `nexus_pub/profile-dropdown.html`: Template for the user profile dropdown.
     - `nexus_pub/search-form.html`: Template for the search form.
     - `nexus_pub/staff.html`: Template for displaying staff information.
     - `nexus_pub/article-grid.html`: Template for presenting articles in a grid layout.
     - `nexus_pub/article.html`: Template for displaying the details of a single article, and where the comments are.
     - `nexus_pub/index.html`: Template for the index page, showing all news articles.

3. **nexus_pub/static/nexus_pub/**:
   - Static files include:
     - `nexus_pub/main.js`: JavaScript file for client-side functionalities and interactions, includes toggle comments, pagination of the comments using the see more button.
     - `nexus_pub/styles.css`: CSS file for defining the application's visual styles and layout.

#### View Functions

1. `index(request)`: Handles the rendering of the index page, displaying news articles sorted by date of publication. It includes a carousel showcasing the newest article headlines from each category.

2. `view_article(request, id)`: Renders the article page for a specific article, displaying the complete story and its associated comments.

3. `view_category(request, category)`: Displays articles filtered by a specific category, showing news related to that category.

4. `view_staff(request, name)`: Shows information about a specific staff member, along with their authored articles.

5. `search(request)`: Allows users to search for articles based on their queries, date range, and authors.

6. `add_comment(request, id)`: Handles the addition of comments to an article by an authenticated user.

7. `star_article(request, id)`: Allows authenticated users to star/unstar articles to indicate their favorites.

8. `save_article(request, id)`: Allows authenticated users to save/unsave articles for later reading.

9. `starred_articles(request)`: Shows the list of articles that the authenticated user has starred.

10. `saved_articles(request)`: Displays the list of articles that the authenticated user has saved.

11. `edit_profile(request)`: Allows an authenticated user to edit their profile information (name, username, email).

12. `login_view(request)`: Handles user login and redirects them to the desired page after login.

13. `logout_view(request)`: Logs out the user and redirects them to the index page.

14. `register(request)`: Handles user registration and redirects them to the desired page after successful registration.

### Nexus Games App

#### Description

The "Nexus Games" app is focused on offering a collection of games to users. Currently, the app includes one game, which is the "Wordle" game. However, I really want add more games in it in the future.

#### Models

1. **GameResult Model**
   - Represents the game results of a user in the "Nexus Games" app.
   - Fields:
      - `user`: Foreign key to the `User` model from the "Nexus Pub" app, representing the user who played the game.
      - `wordle_played`: Integer field to track the number of times the user has played the "Wordle" game, with a default value of 0.
      - `wordle_won`: Integer field to track the number of times the user has won the "Wordle" game, with a default value of 0.

#### Features

1. **Wordle User Ranking**:
   - Provides a ranking system that tracks and displays the performance of users in the "Wordle" game.
   - Users can view their rankings compared to other players, it shoows the Top 5 user based on the number of games won or points scored.
   - It also involves a reload button to get the latest ranking among the users.

2. **Statistics Menu and Points System**:
   - Includes a statistics menu where users can access the amount they played the game and the number won, plus their winning percentage.
   - The app implements a points system to reward users for their achievements and progress in the games.

3. **Settings Menu**:
   - Offers a settings menu that allows users to customize game-related preferences and configurations according to their preferences. (To be done)

4. **Help Menu**:
   - Provides game instructions, rules, and tips to assist users in understanding and playing the games effectively.

5. **Surrender Button**:
   - Users can choose to surrender or give up during a game.

6. **Restart Button**:
   - Allows users to restart or reset a game if they wish to begin again from the beginning or retry a challenge.

7. **Message**:
   - The user is promted of a message if they input word not on the list or shorter than the word length to be guessed.

8. **Win or Lose Modal**:
   - If the user lose or won, they are promted by a modal and have the button to restart or to view stats.

9. **Confetti Effect**:
   - When the user wins, an animation of confetti shows.

#### Pages

1. **Games Page**:
   - This page serves as the landing page for the Nexus Games app.
   - It provides an overview of the available games and allows users to access the different game options.

2. **Wordle Page**:
   - This page represents the Wordle game within the Nexus Games app.
   - Users can play the Wordle game on this page and engage with its specific functionalities and features.

The app's structure may include additional pages in the future as more games are introduced and integrated into the Nexus Games app. 

#### File Structure

The file structure of the "Nexus Games" app is organized as follows:

1. **nexus_games/**
   - `static/`: Directory for static files used in the app.
   - `static/games/`: Subdirectory for game-specific static files.
     - `game.js`: JavaScript file for game-related logic and functionalities. Functions includes: initBoard, abortGame, rightGuessString, and updateStats.
     - `main.js`: Main JavaScript file for the games app, includes the event listeners.
     - `ui.js`: JavaScript file for user interface interactions in the games. Functions includes: showFinalMessage, showLoseModal, showWinModal, showSection, showMessage, howFinalMessage, showWinModal, triggerConfetti, shadeKeyBoard, and animateCSS.
     - `wordle.css`: CSS file for styling the Wordle game.
     - `words.js`: JavaScript file containing word data for the games.
   - `templates/`: Directory for HTML templates used in the app.
   - `templates/games/`: Subdirectory for game-specific templates.
     - `dashboard.html`: Template for the dashboard page displaying user rankings and statistics.
     - `games.html`: Template for the games page listing the available games.
     - `layout.html`: Base template defining the overall structure for other game-specific templates.
     - `wordle.html`: Template for the Wordle game page.
   - `templatetags/`: Directory for custom template tags (used to extend template functionalities).
     - `custom_filters.py`: Python file containing custom template filter which is `ordinalize` for the user ranking.
   - `admin.py`: Django admin site configurations for managing app models.
   - `apps.py`: Django app configurations, such as the app name and settings.
   - `models.py`: App-specific database models, including the `GameResult` model.
   - `tests.py`: Unit tests for the app.
   - `urls.py`: URL patterns and corresponding view functions for the app.
   - `views.py`: Contains view functions handling HTTP requests and generating responses for the app.

#### View Funtions

1. **`games(request)`**:
   - This function handles the rendering of the games page, which serves as the landing page for the Nexus Games app.
   - If the user is not authenticated (logged in), a warning message is displayed, asking the user to log in first to gain access.

2. **`wordle(request)`**:
   - This function handles the rendering of the Wordle game page within the Nexus Games app.
   - If the user is authenticated (logged in), game-related statistics and rankings are calculated and displayed on the page.
   - The user's GameResult object is retrieved or created, and relevant data such as the number of games played, games won, and percentage of wins is calculated.
   - The top 5 users with the highest number of games won are also fetched, and the current user's ranking in the list is determined.

3. **`update_points(request)`**:
   - This function handles the update of points for the authenticated user.
   - When a POST request is received, the user's points are incremented by 1 using the F() expression, and the updated points value is returned in the response as JSON data.

4. **`update_stats(request, isWin)`**:
   - This function handles the update of game statistics for the Wordle game based on whether the user won the game or not.
   - When a POST request is received, the statistics for games played and games won are updated using F() expressions.
   - The updated statistics, including games played, games won, and percentage of wins, are returned in the response as JSON data.

5. **`logout_games(request)`**:
   - This function handles the user logout from the Nexus Games app.
   - After the user is logged out, they are redirected to the games page.

#### Planned Expansion
-The Nexus Games app has future plans by adding more games to provide users with a diverse selection of options. As new games are developed and integrated into the app, additional models and views specific to each game will be implemented. This expansion aims to enhance the overall gaming experience for the users.

### Nexus World News App

#### Description

Nexus World News is an app that utilizes the news API to fetch the latest and most popular news worldwide. Users can search for news based on categories and specific queries.

#### Pages

- **Index Page**: This is the main page of the Nexus World News app where the latest news articles and headlines are displayed. Users can also search for news by entering a search query or selecting a category.

#### File Structure

- **world_news/**
  - `templates/`: Directory for HTML templates used in the app.
  - `templates/world_news/`: Subdirectory for app-specific templates.
    - `index.html`: Template for the Index page displaying the latest news articles and headlines.
  - `admin.py`: Django admin site configurations for managing app models.
  - `apps.py`: Django app configurations, such as the app name and settings.
  - `tests.py`: Unit tests for the app.
  - `urls.py`: URL patterns and corresponding view functions for the app.
  - `views.py`: Contains view functions handling HTTP requests and generating responses for the app.

#### View Functions

- **`index(request)`**:
  - This function handles the rendering of the Index page, which displays the latest news articles and headlines.
  - The function utilizes the news API to fetch the data and display it on the page.
  - Users can search for news by entering a search query, and the API URL is adjusted accordingly to fetch relevant results.
  - The API response is parsed and relevant data, such as article titles, descriptions, URLs, and published dates, is extracted.
  - The extracted data is organized and sent to the template to be displayed as headlines and news articles.
  - The context also includes a list of categories to enable users to explore news by different topics.
  
## Installation & How to Run the Project

To run the project, follow the steps below:

1. Install the dependencies:
   ```bash
   $ pip install -r requirements.txt
   ```

2. Make migrations for the database:
   ```bash
   $ python manage.py makemigrations
   ```

3. Apply the migrations:
   ```bash
   $ python manage.py migrate
   ```

4. Finally, run the Django project:
   ```bash
   $ python manage.py runserver
   ```

## Comments

A huge huge thanks to the whole team of CS50 for providing courses with such a high quality 👏👏👏

## Stay in touch

- LinkedIn: [John Mark Delima](https://www.linkedin.com/in/delimajohnmark)
- Email: [delimajohnmark14@gmail.com](mailto:delimajohnmark14@gmail.com)
- [Personal Portfolio](https://jnale-hub.github.io/John-Mark-Delima/)
