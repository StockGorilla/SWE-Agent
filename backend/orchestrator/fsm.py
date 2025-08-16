class IssueFSM:
    """
    Simple FSM to track the state of a Jira issue in the AI workflow
    States: planned → coded → reviewed → auto_fix → pr_created → failed
    """
    STATES = ["planned", "coded", "reviewed", "auto_fix", "pr_created", "failed"]

    def __init__(self, issue_id):
        self.issue_id = issue_id
        self.state = None
        self.history = []

    def transition(self, new_state):
        if new_state not in self.STATES:
            raise ValueError(f"Invalid state: {new_state}")
        self.state = new_state
        self.history.append(new_state)

    def get_state(self):
        return self.state

    def get_history(self):
        return self.history
