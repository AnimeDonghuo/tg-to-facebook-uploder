class FacebookError(Exception):
    def __init__(self, message, code=None, category="UNKNOWN"):
        super().__init__(message)
        self.code = code
        self.category = category

def classify_fb_error(data: dict) -> FacebookError:
    error = data.get("error", {})
    code = error.get("code")
    msg = error.get("message", "Unknown Meta Error")
    
    if code in [4, 17, 32, 613]: return FacebookError(msg, code, "RETRYABLE")
    if code in [102, 190, 10, 200]: return FacebookError(msg, code, "AUTHENTICATION")
    return FacebookError(msg, code, "PERMANENT")
