## **APIs**

### **1. Property Management**
#### **Create Property**
- **Endpoint**: `POST /api/v1/properties`
- **Description**: Creates a new property listing.
- **Request Body**:
  ```json
  {
      "location": "New York",
      "price": 5000,
      "property_type": "Apartment",
      "description": "A beautiful 2BHK apartment",
      "amenities": ["Pool", "Gym"]
  }
  ```
- **Query Params**: `user_id` (string)

#### **Update Property Status**
- **Endpoint**: `PATCH /api/v1/properties/{property_id}`
- **Description**: Updates the status of a property.
- **Query Params**:
  - `status` (string: "Available" or "Sold")
  - `user_id` (string)
- **Response**:
  ```json
  {
      "message": "Property property_1 status updated to Sold"
  }
  ```

---

### **2. User-Specific APIs**
#### **Get User Properties**
- **Endpoint**: `GET /api/v1/user/properties`
- **Description**: Retrieves all available properties owned by a user.
- **Query Params**: `user_id` (string)

#### **Shortlist Property**
- **Endpoint**: `POST /api/v1/user/shortlist/{property_id}`
- **Description**: Adds a property to the user's shortlist.
- **Query Params**: `user_id` (string)
- **Response**:
  ```json
  {
      "message": "Property property_1 has been successfully added to your shortlist."
  }
  ```

#### **Get Shortlisted Properties**
- **Endpoint**: `GET /api/v1/user/shortlist`
- **Description**: Retrieves all properties in the user's shortlist.
- **Query Params**: `user_id` (string)

#### **Remove Property from Shortlist**
- **Endpoint**: `DELETE /api/v1/user/shortlist/{property_id}`
- **Description**: Removes a property from the user's shortlist.
- **Query Params**: `user_id` (string)
- **Response**:
  ```json
  {
      "message": "Property property_1 has been successfully removed from your shortlist."
  }
  ```

---

### **3. Search API**
#### **Search Properties**
- **Endpoint**: `GET /api/v1/properties/search`
- **Description**: Searches available properties based on filters like price, location, and property type.
- **Query Params (Optional)**:
  - `min_price` (float)
  - `max_price` (float)
  - `location` (string)
  - `property_type` (string)
  - `sort_key` (string: "price" or "timestamp")
  - `descending` (boolean)
  - `page` (int)
  - `limit` (int)

---