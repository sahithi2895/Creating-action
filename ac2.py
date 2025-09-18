from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import random

# -------------------------------
# Initialize FastAPI
# -------------------------------
app = FastAPI(title="Dandiya Event Booking Agent")

# -------------------------------
# Allowed data sets
# -------------------------------
ALLOWED_DATES = {"2025-10-05", "2025-10-06", "2025-10-07"}
AVAILABLE_SLOTS = {"6-8 PM", "8-10 PM"}
ALLOWED_NAMES = {"Sahithi", "John Doe", "Jane Smith"}
ALLOWED_PHONE_NUMBERS = {"7358174456", "7358174457", "7358174458"}

# -------------------------------
# Pydantic Models
# -------------------------------
class PhoneNumber(BaseModel):
    phone_number: str

class FullName(BaseModel):
    name: str

class EventDate(BaseModel):
    date: str

class BookingDetails(BaseModel):
    name: str
    phone_number: str
    date: str
    time_slot: str

# -------------------------------
# Name Validation
# -------------------------------
@app.post("/validate-name/")
def validate_name(name: FullName):
    if name.name in ALLOWED_NAMES:
        return {"message": "Name is valid!", "name": name.name}
    return {"message": "Name is invalid!", "name": name.name}

# -------------------------------
# Phone Number Validation
# -------------------------------
@app.post("/validate-phone/")
def validate_phone(phone: PhoneNumber):
    if phone.phone_number in ALLOWED_PHONE_NUMBERS:
        return {"message": "Phone number is valid!", "phone_number": phone.phone_number}
    return {"message": "Phone number is invalid!", "phone_number": phone.phone_number}

# -------------------------------
# Date Validation
# -------------------------------
@app.post("/validate-date/")
def validate_date(event: EventDate):
    if event.date in ALLOWED_DATES:
        return {
            "message": "Date is valid!",
            "date": event.date,
            "available_slots": list(AVAILABLE_SLOTS)
        }
    return {"message": "Invalid date. No slots available.", "date": event.date}

# -------------------------------
# Booking Event (Flat Checks)
# -------------------------------
@app.post("/book-event/")
def book_event(details: BookingDetails):
    if details.name not in ALLOWED_NAMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid name provided."
        )
    if details.phone_number not in ALLOWED_PHONE_NUMBERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number provided."
        )
    if details.date not in ALLOWED_DATES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected date not available."
        )
    if details.time_slot not in AVAILABLE_SLOTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid time slot."
        )

    confirmation_id = f"DANDIYA-{random.randint(1000,9999)}"
    return {
        "message": f"🎉 Thank you {details.name}! Your booking is confirmed.",
        "name": details.name,
        "phone_number": details.phone_number,
        "date": details.date,
        "time_slot": details.time_slot,
        "confirmation_id": confirmation_id
    }
