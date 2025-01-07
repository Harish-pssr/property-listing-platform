# Property Listing Platform

## Overview

The Property Listing Platform is a comprehensive FastAPI-based solution designed to manage and interact with property listings. It allows users to create, update, and retrieve properties while maintaining user-specific shortlists and enabling advanced property search functionalities. 

Key features include:
- **Property Management**: CRUD operations to manage property details such as location, price, type, status, and amenities.
- **User-Specific Shortlists**: Manage personalized shortlists with options to add, view, and remove properties, while maintaining their order by shortlist date.
- **Advanced Search and Filtering**: Supports filtering properties based on price range, location, property type, and sorting by price or creation timestamp.
- **Scalability**: Optimized data structures and indexing strategies ensure high performance for filtering and sorting operations, even with large datasets.

This platform is designed to be modular, scalable, and ready for deployment in real-world scenarios. It serves as a robust backend for property management applications, catering to the needs of users, property managers, and search functionalities.

---

## **Project Structure**

```
property_listing_platform/
├── app/
│   ├── main.py               # Application entry point
│   ├── config/               # Configuration files
│   ├── models/               # Database models and Pydantic schemas
│   ├── routers/              # API route handlers
│   ├── services/             # Core business logic
│   ├── utils/                # Utility functions
|   ├── tests/                # Unit tests for APIs
|   ├── API_Documentation.md  # API endpoints and usecases
|   ├── Design_Document.md    # Design and implementatin strategy 
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
```

---

## **Setup**

### **1. Clone the Repository**
```bash
git clone <repository_url>
cd property_listing_platform
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # Linux/MacOS
venv\Scripts\activate      # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run the Application**
```bash
cd app
uvicorn main:app --reload
```

---

## **Testing**

### **Run All Tests**
```bash
pytest
```

### **Run Specific Tests**
```bash
pytest tests/test_properties.py
```