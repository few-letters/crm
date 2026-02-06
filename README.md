# CRM Django pet-project

### A comprehensive Customer Relationship Management system designed to manage customers, orders, and product inventory. Features full CRUD, DB optimization
<br>
<img width="1919" height="859" alt="image" src="https://github.com/user-attachments/assets/dc1c6e70-a7a1-4bb3-ab9d-01a3b48adebb" />

## 🛠 Tech Stack

* **Core:** Python 3.11, Django 5.2
* **Database:** PostgreSQL
* **Caching:** Redis via Docker (configured for Select2 widget caching)
* **DevOps:** Docker, Docker Compose (deployment in process)
* **Frontend:** Bootstrap 5, JS, Select2, CSS, Django Templates

## 🔥 Key Features

### 1. Advanced Form Handling (Master Form)
Implemented a complex "Master Form" that allows creating a **Customer**, an **Order**, and multiple **Order Items** in a single submission.
* Uses `inlineformset_factory`.
* **Atomic Transactions:** Used `transaction.atomic()` to ensure that either all records are saved, or none, preventing database inconsistencies.

### 2. Database Optimization (ORM)
Focus on solving the N+1 query problem to ensure high performance.
* Used `select_related` for ForeignKeys (e.g., fetching Customer with Order).
* Used `prefetch_related` for Reverse relationships (e.g., fetching OrderItems for Orders).
* Result: No N+1 problems were found. Average amount of queries is around 4-5 instructions (inspected with DDT).

### 3. Secure & Fast Autocomplete
Implemented server-side searching for products and customers using **Django-Select2** backed by **Redis**.
* **Security:** Prevents IDOR attacks by storing widget configuration in Redis (signed state), not in the URL.
* **Performance:** Loads results via AJAX, reducing initial page size and rendering time.

### 4. Other Features
* **Pagination:** Efficiently handles large lists of data.
* Dynamic Filtering: Custom search functionality by multiple fields (Customer Name, Email, Order ID) preserving query parameters across pages.
* Authentication: implemented register, login, logout functionality for user (CRM manager) with django.contrib.auth

## Screenshots (UI)

### Master form
<img width="1590" height="806" alt="image" src="https://github.com/user-attachments/assets/b1b75be2-7bab-4b8d-bbac-e795260ca0df" />

<br>

### Order List
<img width="1919" height="826" alt="image" src="https://github.com/user-attachments/assets/1cfbd6da-8ce6-4fa9-8c74-d9041feb5d3d" />

<br>

### Add Product form
<img width="1913" height="721" alt="image" src="https://github.com/user-attachments/assets/8366c06a-2f2c-4bdc-8c05-d4a6ac9c65f4" />

<br>

### Add Order form (for existing customer)
<img width="1911" height="796" alt="image" src="https://github.com/user-attachments/assets/770cda13-b470-4576-afa9-a883ccc325ee" />
