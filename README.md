# TravelWorld ✈️


![Mockup](docs/mockup.png) 

A Django-based web application for searching trips, booking tickets, and managing reservations. The project includes a modern user interface, built-in authentication, and a JSON API for integrations.  

🔗 **Live site:** _[https://your-travelworld-app-3a2a4e74772e.herokuapp.com/]_  

---

## Table of Contents

- [User Experience](#user-experience)
- [Design](#design)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Bugs](#bugs)
- [Deployment](#deployment)
- [Credits & Acknowledgements](#credits--acknowledgements)

---

## User Experience

### First-Time Visitor Goals
- Easily search for available trips.
- View trip details such as price and available seats.
- Book a trip quickly without the need for an account.

### Returning Visitor Goals
- Log in to view previous bookings.
- Cancel or modify an existing booking.
- Search and book new trips.

### User Stories
1. As a user, I want to search for trips by origin, destination, and date.  
2. As a user, I want to book a trip and receive a booking reference.  
3. As a registered user, I want to view my bookings.  
4. As a user, I want to cancel a booking so that seats are released.  

---

## Design

### Wireframes
(Add screenshots here if available).

### Colour Scheme
- Primary: Blue (calm and travel-related)  
- Secondary: White/Grey for readability  
- Accent: Orange for buttons and CTAs  

### Typography
- **Roboto** for body text (modern and easy to read).  
- **Montserrat** for headings (bold and clear).  

### Imagery
Travel destination images are used to inspire users, sourced from [Unsplash](https://unsplash.com/).  

---

## Features

### Navigation
- Navbar with links to Home, Search, My Bookings, and Login.  
- Clear navigation and intuitive structure.  

### Current Features
- **Trip Search:** Search trips by location and date.  
- **Booking Form:** Reserve seats and provide contact details.  
- **My Bookings:** Logged-in users can view their bookings.  
- **Cancel Booking:** Cancel existing bookings and view history.  
- **Admin Panel:** Manage trips, bookings, and users.  
- **JSON API:** Endpoints for searching, booking, retrieving, and cancelling reservations.  

### Future Features
- Online payment integration (Stripe/PayPal).  
- Email confirmations for bookings and cancellations.  
- Advanced filtering and sorting in search results.  

---

## Technologies Used

- **Languages:** Python, HTML, CSS  
- **Frameworks:** Django 4.2  
- **Libraries:** Bootstrap, WhiteNoise, dj-database-url  
- **Database:** SQLite (dev), PostgreSQL (production)  
- **Version Control:** Git & GitHub  
- **Deployment:** Heroku  

---

## Testing

### Code Validation
- HTML and CSS validated using W3C Validators.  
- Python code checked with PEP8 standards using flake8.  

### Responsiveness
- Tested using Chrome DevTools on iPhone, iPad, and Desktop views.  
- Layout adapts correctly to different screen sizes.  

### Lighthouse Testing
- Performance, Accessibility, and SEO tested with Lighthouse in Chrome.  

### Accessibility
- Checked colour contrast.  
- All images include descriptive alt text.  

### Manual Testing
- Trip search returns correct results.  
- Booking decreases available seats.  
- Cancelling restores available seats.  
- Admin panel functions as expected.  

---

## Bugs

### Fixed Bugs
- **Issue:** Users could book even if no seats were available.  
  **Fix:** Added validation to `BookingForm`.  

### Known Bugs
- No known bugs at this time.  

---

## Deployment

### Deployment to Heroku
1. Create a new Heroku app.  
2. Set buildpack to `heroku/python`.  
3. Add `Procfile` and `runtime.txt`.  
4. Provision a Postgres database.  
5. Push code from GitHub or CLI.  
6. Run `python manage.py migrate` and `python manage.py collectstatic`.  

### Forking the Repository
1. Go to the GitHub repository.  
2. Click **Fork** in the top right.  
3. Rename the fork if desired.  
4. Click **Create fork**.  

### Cloning the Repository
```bash
git clone https://github.com/Parre87/TravelWorld.git
cd TravelWorld



