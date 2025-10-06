# Film Chat Website
A social platform for film lovers to chat publicly and privately about movies, curate personal top-5 lists, and discover titles from a seeded database of 1,000+ IMDb films.

## Overview
FilmChat was built during the COVID era to recreate the feeling of movie-night discussions even when physically apart, combining persistent private threads with a public homepage feed to keep conversations going across sessions. Authenticated users can add friends, chat in real time via WebSockets, and showcase favorite movies on their profile with a curated top-5 drawn from an IMDb-derived list (and can add missing films to the catalog).

## Key Features
- Real-time chat
- Public feed for sitewide conversations about any film.
- Private, persistent friend-to-friend threads that live beyond page refreshes or navigation.
- Social graph and profiles
- Friend system to connect with known contacts.
- User profiles display a curated top-5 films with quick links to discussions.
- Film catalog
- Seeded database of 1,000+ IMDb top titles for quick selection, with the ability to add missing films.
- Authenticated experience
- Account creation and login to enable private messaging, profile editing, and personalization.

## Architecture
- Backend: Python with Django, using WebSockets for real-time messaging and persistence of conversations in the database.
- Frontend: HTML/CSS with Bootstrap and vanilla JavaScript for chat UI and interactive components.
- Database: MySQL (external to this repository) to store users, friendships, messages, and films.
- Deployment: Previously hosted on an AWS EC2 instance; archived as a portfolio reference today.
