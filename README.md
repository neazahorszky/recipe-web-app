# recipe-web-app
Tsoha project

In the app, there are recipes that one can search through and review.

App features:  
- Users can sign in and out and create a new user account  
- Users can click on a recipe to see its details (ingredients needed and the instructions for preparing the food)  
- Users can rate recipes (stars and comment) and read others' reviews  
  <br>
How to test the web-app:  
- Clone this repository to your computer and go to its root folder  
- Create .env file with the following content:  
    ```
    DATABASE_URL=<local-database-address>  
    SECRET_KEY=<secret-key>  
    ```
- Activate virtual environment and install requirements as follows:  
    ```
    $ python3 -m venv venv     
    $ source venv/bin/activate  
    $ pip install -r ./requirements.txt  
    ```  
- Define the database schema:
    ```
    $ psql < schema.sql
    ``` 
- Now you can start the app with the command
    ```
    $ flask run
    ```
