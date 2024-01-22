# LittleLemonAPI Project

This repository contains the source code for the LittleLemonAPI project, a fully functioning API developed for the Little Lemon restaurant. The project enables client application developers to build web and mobile applications, allowing users with different roles to perform various tasks such as browsing, adding and editing menu items, placing orders, and managing deliveries.

**PS1.** This is my inaugural project, and it's possible that you might encounter some errors :)

**PS2.** Project requirements on the course were a little bit confusing and even the solution code provided after we submitted the task doesn't meet the requirements but it was clean and DRY. Anyway valuable experience

Project Overview
----------------

### Scope

The project encompasses the creation of a Django app named LittleLemonAPI, where all API endpoints are implemented. Dependencies are managed using pipenv within a virtual environment. The use of class-based views is encouraged, adhering to proper API naming conventions.

### User Groups

Two user groups, "Manager" and "Delivery Crew," are created using Django admin. Users not assigned to any group are considered customers.

### Error Handling and Status Codes

Error messages with appropriate HTTP status codes are implemented for specific scenarios, including non-existing resources, unauthorized API requests, and invalid data in POST, PUT, or PATCH requests.

### API Functionality

#### User Registration and Token Generation Endpoints using Djoser

*   `/api/users`: POST - Creates a new user with name, email, and password.
*   `/api/users/me/`: GET - Displays only the current user.
*   `/token/login/`: POST - Generates access tokens for other API calls.

### Menu-Items Endpoints

*   `/api/menu-items`: GET - Lists all menu items (Customers, delivery crew).
*   `/api/menu-items`: POST, PUT, PATCH, DELETE - Denies access and returns 403 – Unauthorized.
*   `/api/menu-items/{menuItem}`: GET - Lists a single menu item.
*   `/api/menu-items/{menuItem}`: POST, PUT, PATCH, DELETE - Returns 403 - Unauthorized.
*   `/api/menu-items`: Manager - GET - Lists all menu items.
*   `/api/menu-items`: Manager - POST - Creates a new menu item.
*   `/api/menu-items/{menuItem}`: Manager - GET - Lists a single menu item.
*   `/api/menu-items/{menuItem}`: Manager - PUT, PATCH - Updates a single menu item.
*   `/api/menu-items/{menuItem}`: Manager - DELETE - Deletes a menu item.

### User Group Management Endpoints

*   `/api/groups/manager/users`: Manager - GET - Returns all managers.
*   `/api/groups/manager/users`: Manager - POST - Assigns the user to the manager group.
*   `/api/groups/manager/users/{userId}`: Manager - DELETE - Removes a user from the manager group.
*   `/api/groups/delivery-crew/users`: Manager - GET - Returns all delivery crew.
*   `/api/groups/delivery-crew/users`: Manager - POST - Assigns the user to the delivery crew group.
*   `/api/groups/delivery-crew/users/{userId}`: Manager - DELETE - Removes a user from the delivery crew group.

### Cart Management Endpoints

*   `/api/cart/menu-items`: Customer - GET - Returns current items in the cart.
*   `/api/cart/menu-items`: Customer - POST - Adds a menu item to the cart.
*   `/api/cart/menu-items`: Customer - DELETE - Deletes all menu items created by the current user token.

### Order Management Endpoints

*   `/api/orders`: Customer - GET - Returns all orders with order items created by the user.
*   `/api/orders`: Customer - POST - Creates a new order item for the user.
*   `/api/orders/{orderId}`: Customer - GET - Returns all items for the specified order id.
*   `/api/orders`: Manager - GET - Returns all orders with order items by all users.
*   `/api/orders/{orderId}`: Customer - PUT, PATCH - Updates the order.
*   `/api/orders/{orderId}`: Manager - DELETE - Deletes an order.
*   `/api/orders`: Delivery crew - GET - Returns all orders with order items assigned to the delivery crew.
*   `/api/orders/{orderId}`: Delivery crew - PATCH - Updates the order status to 0 or 1.

### Additional Steps

*   Proper filtering, pagination, and sorting capabilities are implemented for `/api/menu-items` endpoint.

### Throttling

Throttling is applied for authenticated users and anonymous/unauthenticated users.

Requirements
------------

*   Python 3.x
*   Django
*   Djoser
*   Pipenv

Getting Started
---------------

1.  Clone the repository.
2.  Navigate to the project directory.
3.  Create and activate a virtual environment using pipenv.
4.  Install dependencies using `pipenv install`.
5.  Apply migrations using `python manage.py makemigrations` and `python manage.py migrate`.
6.  Run the development server using `python manage.py runserver`.
7.  Access the API at `http://localhost:8000/`.

Functionality Evaluation Criteria
---------------------------------

This project provides functionality to perform various tasks, and the following criteria will be used to evaluate its effectiveness:

1.  Admin can assign users to the manager group.
2.  Manager group can be accessed with an admin token.
3.  Admin can add menu items.
4.  Admin can add categories.
5.  Managers can log in.
6.  Managers can update the item of the day.
7.  Managers can assign users to the delivery crew.
8.  Managers can assign orders to the delivery crew.
9.  Delivery crew can access orders assigned to them.
10.  Delivery crew can update an order as delivered.
11.  Customers can register.
12.  Customers can log in using their username and password and get access tokens.
13.  Customers can browse all categories.
14.  Customers can browse all menu items at once.
15.  Customers can browse menu items by category.
16.  Customers can paginate menu items.
17.  Customers can sort menu items by price.
18.  Customers can add menu items to the cart.
19.  Customers can access previously added items in the cart.
20.  Customers can place orders.
21.  Customers can browse their own orders.


Good luck with your reviews!
