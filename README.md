## Pizza

This is a web application for handling a pizza restaurant’s online orders. Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. Meanwhile, the restaurant owners will be able to add and update menu items and view orders that have been placed.

## Installation
After cloning or downloading the repository, the required packages can be installed via the following commands.

For `pipenv`, run:
`pipenv install`

For `venv`:
`pip install -r requirements.txt`

To apply migrations:
`python manage.py migrate`

## Deployment
There are a few ways to deploy this application on both local and remote servers.

    python manage.py runserver

> Run this command to deploy in the local server.

To deploy in Heroku, create a `Procfile` and put the following command inside it.

    release: python manage.py migrate
    web: gunicorn pizza.wsgi --log-file -

## Usage
Visit [the site](https://pizza-subs-online.herokuapp.com/), and find many delicious food items. When you click into a food item, you'll be taken to a customization page. The price will be updated in real-time while customizing. You need to be logged in to add foods to the cart. Add as many as you can eat. Then go to the `Cart` page to see what have you added so far and how much these are going to cost. You may remove items from the cart. Confirm your order by pressing the `Confirm order` button. After you have confirmed orders, these orders can be visible in `

## Privacy
* Your name, email, username, password, & order details are stored in the database.
* Order details can be deleted only before order confirmation.
* All of your data is protected with Django's state of the art security features.

## Built With

* [Django](https://www.djangoproject.com/)- The web framework.
* [SQLite](https://www.sqlite.org/) - The SQL database engine used in development.
* [PostgreSQL](https://www.postgresql.org/) - Open source object-relational database system used in production.
* [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/) - Front-end framework.
* [Vanilla JS](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Regular Javascript.
