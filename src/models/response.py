class Response:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    def __repr__(self):
        return 'Response(status={}, message={}, data={})'.format(
            self.status, self.message, self.data
        )

    def to_dict(self):
        return {
            'status': self.status,
            'message': self.message,
            'data': self.data
        }
