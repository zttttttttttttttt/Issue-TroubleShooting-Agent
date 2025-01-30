# utils/context_manager.py


class ContextManager:
    def __init__(self):
        self.context = {}

    def get_context(self):
        """Return the underlying dictionary (if needed)."""
        return self.context

    def get_context_dict(self):
        """Return the underlying dictionary (if needed)."""
        return self.context

    def get_context_str(self):
        return self.context_to_str()

    def clear_context(self):
        """Reset the context to an empty dict."""
        self.context = {}

    def add_context(self, key, value):
        self.context[key] = value
        print(f"Add '{key}' into the context.")

    def remove_context(self, key):
        if key in self.context:
            del self.context[key]
            print(f"Remove '{key}' from the context.")
        else:
            print(f"Key '{key}' not found in context.")

    def context_to_str(self):
        """
        If the context is empty, return an empty string.
        Otherwise, wrap each key/value pair in <key></key> inside <context></context>.
        """
        if not self.context:
            return ""
        context_str = "<Context>\n"
        for key, value in self.context.items():
            context_str += f"<{key}>\n{value}\n</{key}>\n"
        context_str += "</Context>\n"
        return context_str

    def __repr__(self):
        """So print(context) shows the stored keys and values nicely."""
        return f"ContextManager({self.context})"


def get_context():
    """
    Return a new Context instance.
    """
    return ContextManager()
