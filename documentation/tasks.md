## TASKS
<hr>

### 1. Create Base Template
- [X] Move header slideshow to 'index' template
- [X] Render the base template on initial load

### 2. Authentication Flow (login/signup)
- [X] Create nav buttons for login/signup
- [X] Create 'login' & 'signup' templates and render inside base using jinja/block_content function
- [X] Create ajax query & endpoint to recieve data & authenticate/signup users (in the DB!)
- [ ] Update UI to show spinners when processing authentication data

### 3. Contact Button (navbar)
- [ ] Create modal form with: Name, Email, Subject, Message
- [ ] Create ajax query & endpoint to recieve data
- [ ] Actually send the message, implement mail functions
- [ ] Update UI to show spinners when processing message data

### 4. Studio Images Pulling From DB
- [X] Add images to 'studio_images' table in db
- [X] Dynamically load images from db and render to studio_details page

### 5. Complete Checkout Flow
- [X] Dynamically load the studio information into checkout metadata and pass to webhook
- [ ] Connect calendar APIs to automatically send invites (maybe add SMS integrations)

### 6. Create 'Booking' Template / Form
- [ ] Create form to allow arbitrary booking that you can choose yourself
- [ ] Create server side functions to carry out the form actions