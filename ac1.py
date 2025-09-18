




from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

# -------------------------------
# Initialize FastAPI
# -------------------------------
app = FastAPI(title="Website Feedback + Insurance Bot")


# -------------------------------
# Pydantic Models
# -------------------------------
class UserName(BaseModel):
    name: str


class WebsiteFeedback(BaseModel):
    name: str
    feedback: str


class InsuranceInterest(BaseModel):
    name: str
    interest: bool  # True if user wants insurance, False otherwise


# -------------------------------
# Verify Name (only if matches a fixed string)
# -------------------------------
@app.post("/verify-name/")
def verify_name(user: UserName):
    if user.name == "Sahithi":
        return {"message": "Name is valid!", "name": user.name}
    elif user.name == "John":
        return {"message": "Name is valid!", "name": user.name}
    elif user.name == "Jane":
        return {"message": "Name is valid!", "name": user.name}
    elif user.name == "David":
        return {"message": "Name is valid!", "name": user.name}
    else:
        return {"message": "Name is not recognized", "name": user.name}


# -------------------------------
# Collect Website Feedback
# -------------------------------
@app.post("/feedback/")
def collect_feedback(feedback: WebsiteFeedback):
    if feedback.feedback == "The website is very easy to use!":
        msg = "Thanks! Your feedback about the website has been recorded."
    elif feedback.feedback == "The design looks good":
        msg = "Thanks! Your feedback about the website has been recorded."
    elif feedback.feedback == "Navigation is simple":
        msg = "Thanks! Your feedback about the website has been recorded."
    elif feedback.feedback == "Loading speed is fast":
        msg = "Thanks! Your feedback about the website has been recorded."
    else:
        msg = "Thanks! Your feedback has been recorded."

    return {
        "message": msg,
        "name": feedback.name,
        "feedback": feedback.feedback,
        "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# -------------------------------
# Insurance Interest
# -------------------------------
@app.post("/insurance/")
def ask_insurance(interest: InsuranceInterest):
    if interest.interest:
        return {
            "message": f"Hi {interest.name}, you can explore and purchase insurance from the 'Insurance' section in the main menu of our website.",
            "section": "Main Menu > Insurance"
        }
    else:
        return {"message": f"Thanks {interest.name}, no problem. Have a great day!"}
