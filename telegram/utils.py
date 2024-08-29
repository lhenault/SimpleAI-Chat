def parse_history(chat_log):
    history = []

    curr_message_id = None
    curr_user = "user"
    curr_user_msg = []
    curr_bot_msg = []
    
    for i in chat_log:
        # If bot->user, a piece of "history" just ended
        if curr_user == "bot" and i[0] == "user":
            # Append it to history
            history.append(
                {
                    "id": curr_message_id,
                    "input": "\n".join(curr_user_msg),
                    "response": "\n".join(curr_bot_msg),
                }
            )

            # Reset variables
            curr_message_id = None
            curr_user_msg.clear()
            curr_bot_msg.clear()

        # Update current user
        curr_user = i[0]

        # Set message id if needed
        if curr_message_id is None:
            curr_message_id = i[2]

        # Then, append appropriately
        if curr_user == "user":
            curr_user_msg.append(i[1])
        else:
            curr_bot_msg.append(i[1])
            
    # If there is a remaining message, add it
    if curr_message_id is not None:
        history.append(
            {
                "id": curr_message_id,
                "input": "\n".join(curr_user_msg),
                "response": "\n".join(curr_bot_msg),
            }
        )

    return history
