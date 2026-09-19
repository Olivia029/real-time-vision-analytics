class VehicleCounter:
    """Count vehicles crossing a horizontal line."""

    def __init__(self, line_y: int = 960):
        self.line_y = line_y

        self.in_count = 0
        self.out_count = 0

        # Last known position of each ID
        self.previous_positions = {}

        # IDs that have been already counted
        self.counted_ids = set()

    def update(self, track_id: int, center_y: int):

        if track_id is None:
            return

        previous = self.previous_positions.get(track_id)

        if previous is not None and track_id not in self.counted_ids:

            # Crosses up
            if previous > self.line_y and center_y <= self.line_y:
                self.out_count += 1
                self.counted_ids.add(track_id)

            # Crosses down
            elif previous < self.line_y and center_y >= self.line_y:
                self.in_count += 1
                self.counted_ids.add(track_id)

        self.previous_positions[track_id] = center_y