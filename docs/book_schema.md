### The book Schema

At the moment,  the company is manually updating the books to their database. The database has the folloowing
schema about the books that is stored in the Mongo database:

1. Title
2. Author
3. Description
4. Language
5. Publisher
6. Publisher Date
7. ISBN
8. Price
9. Status (PENDING, ACTIVE, INACTIVE)
10. Created Date
11. Updated Date
12. Inactive Date
13. Ratings By Stars (Array of Objects with keys as stars and values as number of ratings, e.g., (1:10, 2:20, 3:30, 4:40, 5:50))
14. Number of Reviews