class Message:
    def __init__(self, sender, recipient, content):
        self.sender = sender
        self.recipient = recipient
        self.content = content


class MessageService:
    def __init__(self):
        self.messages = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages
