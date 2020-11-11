# Inventory API and Webapp

## Description
Hobbyist communities for roleplaying often have difficulty managing user inventories as they can get expansive over time because of an individual creating multiple characters and the natural progression of obtaining items.

This web app is designed to help users manage their inventories for all of their characters with a single account and have it be accessible on any device. This web app has advantages over Google Docs or Google Sheets which can become quite messy over some time, especially dependent on the players' own tracking system. The web app will maintain all of the relevant inventories by the user and display them in a clutter-free way to improve an individual's inventory management.

The Postgres database and web-app is managed by a Django server using the Django Rest Framework and SimpleJWT as the back-end and web-packed React for the front-end.

## Disclaimer
This project is a planned continuous WIP and will continue to be supported and maintained. At this point in time, a front-end webapp has yet to be started and there are some crucial endpoints missing (but with their DB logic created) such as:
- User registration.
- Character registration and deletion/inactive marking.
- Item creation/deletion/editing.

### (Planned) Front-end technologies:
- React

### Back-end technologies:
- Django
- Django Rest Framework
- Django Rest Framework SimpleJWT
- Postgres