# **Design Document**

## **1. Data Structure Design**

### **1.1 Property Listings Data**
**Structure**: A dictionary mapping `property_id` to property objects.

```python
properties = {
    "property_1": Property(
        property_id="property_1",
        user_id="user_1",
        location="New York",
        price=500000,
        property_type="Apartment",
        status="Available",
        timestamp=datetime(2025, 1, 1),
        description="A beautiful 2BHK apartment",
        amenities=["Pool", "Gym"]
    )
}
```

**Justification**:
- **Dictionary**: Provides **O(1)** average time complexity for lookup by `property_id`.
- **Ease of Access**: Facilitates quick updates, deletions, and access to specific properties.
- **Scalability**: Handles large datasets efficiently.

**Property Status Updates**:
- **Logic**:
  - Update the `status` field of the corresponding property object.
  - Adjust search indices (e.g., remove from `price_index` or `location_index` if the status changes to `Sold`).

---

Here’s the updated version of **1.2 User Portfolios** to reflect the on-the-fly calculation approach:

---

### **1.2 User Portfolios**

**Structure**:  
User portfolios are not stored directly as a separate data structure. Instead, they are calculated on the fly by filtering properties owned by a specific user from the `properties` dictionary.

```python
user_portfolios = {
    user_id: [
        property_id
        for property_id, property in properties.items()
        if property.user_id == user_id
    ]
}
```

**Justification**:
- **On-the-Fly Calculation**: Avoids maintaining a separate data structure for user portfolios, reducing memory usage and complexity.
- **Flexibility**: Always reflects the latest state of properties for the user.
- **Efficiency**: Filters the `properties` dictionary, which is sufficient for the expected usage frequency.


---

### **1.3 Shortlisted Properties**
**Structure**: A dictionary mapping `user_id` to a sorted list of tuples containing `shortlist_time` and `property_id`.

```python
shortlisted_properties = {
    "user_1": [(datetime(2025, 1, 2), property_3)]
}
```

**Justification**:
- **Dictionary**: Ensures efficient access to a user’s shortlist. Sorted list makes sure displaying properties in the order of shortlist_time.
- **List of Tuples**: Captures the `property_id` and `shortlist_date` for sorting by the most recently shortlisted properties.

**Handling Shortlist Updates**:
- Add: Append the property to the list and set the `shortlist_date` to the current timestamp. Use binary search to add the tuple at the right index.
- Remove: Remove the specific `property_id` from the user’s list.

---

### **1.4 Search Indices**
**Structure**:
1. **Price Index**: A sorted list of tuples (`price`, `property_id`).
   ```python
   price_index = [(300000, "property_1"), (500000, "property_2"), (700000, "property_3")]
   ```

2. **Location Index**: A dictionary mapping `location` to a list of `property_ids`.
   ```python
   location_index = {
       "New York": ["property_1", "property_2"],
       "San Francisco": ["property_3"]
   }
   ```

**Justification**:
- **Price Index**:
  - A sorted list ensures efficient range filtering using binary search (`O(log n)`).
- **Location Index**:
  - A dictionary ensures **O(1)** access to properties for a specific location.

**Index Management**:
- When properties are added, updated, or deleted, the indices are updated accordingly.
- **Example**: If a property is marked as `Sold`, it is removed from the `price_index` and `location_index`.

---

## **2. Search/Sort Implementation Strategy**

### **2.1 Price Range Filtering**
  - Use `bisect` to perform a binary search on the sorted `price_index` for efficient range filtering.
  - `bisect_left` and `bisect_right` determine the indices for the `min_price` and `max_price`.
---

### **2.2 Location-Based Search**
  - Use `location_index` to retrieve properties matching the location.
  - Combine the result with other filters (e.g., price range) using set intersection.

---

### **2.3 Multiple Criteria Sorting**
  - Retrieve the filtered properties.
  - Sort the result based on the `sort_key` (e.g., `price`, `timestamp`) and `descending` flag.

---

### **2.4 Search Result Pagination**
- **Approach**:
  - Use slicing (`results[start:end]`) to retrieve a specific page of results based on the `page` and `limit` parameters.
  - Calculate `start` and `end` as:
    ```python
    start = (page - 1) * limit
    end = start + limit
    ```

- **Performance**:
  - Slicing is **O(k)**, where `k` is the size of the filtered list.

---

## **3. Performance Considerations**
- Use sorted lists and dictionaries for efficient lookups and updates.
- Optimize filtering using indices (`price_index`, `location_index`).
- Use thread-safe locks to handle concurrent updates to `properties`, `price_index`, and `location_index`.

---

## **4. Indexing Strategy**
1. **Price Index**:
   - Sorted list enables efficient range queries using binary search.
   - Updated when a property is created, updated, or deleted.

2. **Location Index**:
   - Dictionary ensures fast retrieval for location-based filtering.
   - Updated during property creation or deletion.