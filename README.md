# PetHaven - Pet Adoption System

PetHaven is a Django REST Framework (DRF) project for managing pet adoptions. It provides user authentication, pet management, wallet integration, reviews, and role-based access control. The project is built with a modern stack and deployed on Vercel, using Supabase as the database and Cloudinary for media storage.

---

## Features

### User Authentication & Verification
- Users are verified via **email and token**.
- JWT-based authentication (DRF).

### Pet Management, Adoption, Wallet, Reviews, and Access Control
- Users can post pets but **cannot edit or delete** them.
- Admins can **edit, delete**, and change `is_adopted` and `availability`.
- When a user adopts a pet:
  - `is_adopted` is automatically set to `True`.
  - The user's wallet is reduced by the pet's price.
- Users can view their profile, including wallet balance and list of adopted pets.
- Users can add money to their wallet.
- Users can review **only pets they have adopted**; others cannot review pets they did not adopt.
- Non-authenticated users can see **only public pets**.
- Users cannot see other users' wallets.

---

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: Supabase (PostgreSQL)
- **Media Storage**: Cloudinary
- **Deployment**: Vercel
- **Authentication**: Email & token verification

---

## Models Overview
- **User**: Custom user with email-based authentication, wallet.
- **Pet**: Stores pet details including `is_adopted` and `availability`.
- **Adopt**: Records each adoption per user.
- **AdoptPet**: Tracks which pets are adopted in each adoption.
- **Review**: User reviews for adopted pets.
- **Wallet**: Tracks user balance and updates automatically on adoption.

---

## Endpoints Overview

### Users
- `POST /auth/register/` - Register a user (email verification)
- `POST /auth/login/` - Login and obtain token
- `GET /profile/` - Get user profile with wallet and adoption history
- `POST /wallet/add/` - Add money to wallet

### Pets
- `GET /pets/` - List all pets (public or all for authenticated users)
- `POST /pets/` - Add a pet (user)
- `PUT/PATCH /pets/<id>/` - Edit pet (admin only)
- `DELETE /pets/<id>/` - Delete pet (admin only)
- `POST /pets/<id>/adopt/` - Adopt a pet (user)

### Reviews
- `POST /pets/<id>/review/` - Add review (only if adopted)
- `GET /pets/<id>/reviews/` - List all reviews for a pet

---

## How it Works
1. Users register and verify via email token.
2. Users can post pets but cannot edit or delete them.
3. Admins can edit, delete, and change `is_adopted` and `availability`.
4. When a pet is adopted:
   - `is_adopted` is automatically set to `True`.
   - User wallet is reduced by pet price.
5. Users can review **only their adopted pets**.
6. Non-authenticated users see only public pets.
7. Users can view their own wallet and adoption history; other users’ wallets are hidden.

---

## Setup
1. Clone the repository:

```bash
git clone <repo-url>
cd PetHaven
```

2. Install dependencies:
``` bash
pip install -r requirements.txt
```

3. Set environment variables (Vercel or local .env):

``` env 
DATABASE_URL=<supabase-postgres-url>
CLOUDINARY_CLOUD_NAME=<cloud_name>
CLOUDINARY_API_KEY=<api_key>
CLOUDINARY_API_SECRET=<api_secret>
SECRET_KEY=<django-secret-key>
DEBUG=False
ALLOWED_HOSTS=<vercel-domain>
``` 
4. Apply migrations:
``` bash
python manage.py migrate
```

5. Run the development server:
``` bash
python manage.py runserver
```# Pet_Haven
