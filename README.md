# Inventory Management System

A product inventory management application built with a Flask REST API backend and an interactive Python CLI client. The app integrates with the [Open Food Facts API](https://world.openfoodfacts.org) to automatically enrich products with real-world data like brand name, barcode, and ingredients.

---

## Features

- **Add products** by name — automatically fetches barcode, brand, and ingredients from Open Food Facts
- **View full inventory** with formatted product details
- **Look up a product** by barcode
- **Edit** a product's price or stock level
- **Delete** products from inventory
- Full **unit test suite** covering both API routes and CLI commands

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| CLI Client | Python 3, `requests` |
| External API | [Open Food Facts](https://world.openfoodfacts.org) |
| Testing | `unittest`, `unittest.mock` |
| Storage | In-memory (no database) |

---

## Project Structure

```
inventory-manage/
├── app.py          # Flask REST API — all CRUD endpoints
├── cli.py          # Interactive CLI client
├── services.py     # Open Food Facts API integration
└── testing.py      # Unit tests for routes and CLI
```

---

## Getting Started

### Prerequisites

- Python 3.7+
- `pip`

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd inventory-manage

# Install dependencies
pip install flask requests
```

### Running the App

The backend and CLI must be run in **separate terminals**.

**Terminal 1 — Start the Flask backend:**
```bash
python3 app.py
```
The API will be available at `http://127.0.0.1:5000`.

**Terminal 2 — Start the CLI client:**
```bash
python3 cli.py
```

You will see an interactive menu:
```
--- Inventory Menu ---
1. Add Product
2. View All Products
3. View Product by Barcode
4. Edit Product
5. Delete Product
6. Quit
```

---

## API Reference

**Base URL:** `http://127.0.0.1:5000`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check / welcome message |
| `GET` | `/products` | Retrieve all products |
| `GET` | `/products/<barcode>` | Retrieve a single product by barcode |
| `POST` | `/products` | Add a new product |
| `PATCH` | `/products/<id>` | Update a product's price or stock |
| `DELETE` | `/products/<id>` | Delete a product |

---

### POST `/products`

Add a new product. The backend calls the Open Food Facts API to enrich it with barcode, brand, and ingredient data.

**Request body:**
```json
{
  "name": "Nutella",
  "price": 8.99,
  "stock": 90
}
```

**Success response (`201 Created`):**
```json
{
  "id": "3017620422003",
  "product": {
    "barcode": "3017620422003",
    "name": "Nutella",
    "brand": "Ferrero",
    "ingredients": "sugar, palm oil, hazelnuts, ...",
    "price": "8.99",
    "stock": 90
  }
}
```

**Error responses:**
| Status | Reason |
|--------|--------|
| `400` | Missing required fields (`name`, `price`, `stock`) |
| `502` | Product not found in Open Food Facts |

---

### PATCH `/products/<id>`

Update a product's `price` or `stock`. Only one field may be updated per request.

**Request body (either field):**
```json
{ "price": 7.49 }
```
```json
{ "stock": 150 }
```

**Success response (`200 OK`):**
```json
{
  "message": "Product updated",
  "product": { ... }
}
```

**Error responses:**
| Status | Reason |
|--------|--------|
| `400` | Invalid or missing field in request body |
| `404` | Product with given ID not found |

---

### DELETE `/products/<id>`

Remove a product from inventory.

**Success response (`200 OK`):**
```json
{ "message": "Product deleted" }
```

**Error response:**
| Status | Reason |
|--------|--------|
| `404` | Product with given ID not found |

---

## Data Model

Each product stored in inventory has the following shape:

```json
{
  "barcode": "3017620422003",
  "name": "Nutella",
  "brand": "Ferrero",
  "ingredients": "sugar, palm oil, hazelnuts, ...",
  "price": "8.99",
  "stock": 90
}
```

| Field | Type | Source |
|-------|------|--------|
| `barcode` | string | Open Food Facts API |
| `name` | string | User input |
| `brand` | string | Open Food Facts API |
| `ingredients` | string | Open Food Facts API |
| `price` | string (2 decimals) | User input |
| `stock` | integer | User input |

---

## Running Tests

```bash
python3 -m unittest testing -v
```

The test suite contains 11 tests across two classes:

| Class | Tests |
|-------|-------|
| `TestProductRoutes` | GET all products, POST product, PATCH product, DELETE product |
| `TestCLICommands` | Response formatting, view all, add product, delete with confirmation |

All external HTTP calls and user input are mocked using `unittest.mock.patch`.

---

## Limitations & Future Improvements

This project is designed for learning and prototyping. Known limitations:

- **No persistence** — inventory resets every time the server restarts (no database)
- **No authentication** — all endpoints are publicly accessible
- **Single user** — no multi-user or session support
- **No pagination** — `GET /products` returns the entire inventory at once

Potential improvements:
- Add a database (e.g. SQLite via SQLAlchemy or PostgreSQL)
- Add user authentication (e.g. Flask-Login or JWT)
- Build a web frontend (e.g. React or plain HTML/JS)
- Add API documentation with Swagger/OpenAPI
- Containerize with Docker
