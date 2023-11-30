
def get_response(message:str) -> str:
    # Makes everything lowerscase so it doesnt run into any capitalization issues
    l_message = message.lower()
    
    # Repsonses:
    if l_message == "help":
        return "help"
    if l_message == "hello" :
        return "Herro"
    # If the user doesnt say any of the above, it returns the following
    return "What are u trying to say? If you need help speaking, type `help`."
