# Buy And Sell Website
Built an Olx like website an e-commerce portal dealing with buying and selling of products.
 It's main functionalities include:
- Login/Register user.
- User can view existing products and their specific details.
- Logged in users can post their products ads which they want to sell.
- Also the specific logged in user can update their products ads which was posted earlier by referring to their my listings.
- Specific logged in user can also delete the particular product ad which was posted earlier by referring to their my listings.
- Also one cannot buy/sell a product unless logged in.
- Logged in user can buy some other user's posted product by just going to that selected product details page and clicking the checkout button, it'll get redirected to payments page where user has to fill his/her card credentials and proceed for the payment. If the user backouts during the transaction, the payment get's failed else it get's successful.
- Newly registered user can update his/her profile in the update profile page. This page will ask him/her to upload a profile picture and enter their contact number and their data get's saved in the Profiles model.
- Also there is an admin dashboard, where entire control of the website is done by the admin. Accessible only by the admin and no other registered user.
- Also user can search products of his/her choice on the view products page. 
- After successful payment by a user to a seller's product, seller/admin will be able to delete the product from the main listings if the product is out of stock in that specific seller's inventory.
- Made use of Pagination.
- Logout option.
-Tech Stack Used :
 * Frontend : HTML-5, Tailwind CSS v2.2.16, Javascript ES-6.
 * Backend : Django 4.0, DBSqlite3, Node.js. 
 * Payment Gateway: Stripe API.

Implementation video : https://drive.google.com/file/d/1NVy3SqYCdxozVUEhAmY1osrOYCa5Y_Jh/view?usp=sharing
