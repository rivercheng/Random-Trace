import unittest
from readtrace import State, transit

class TestReadTrace(unittest.TestCase):
    def setUp(self):
        self.state = State()

    def test_transistion_general(self):
        for ops in ["ZOOM_IN", "ZOOM_OUT", "MOVE_UP", "MOVE_DOWN",\
                    "MOVE_LEFT", "MOVE_RIGHT", "TILT_FORWARD",\
                    "TILT_BACKWARD", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",\
                    "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE",\
                    "RESET"]:
            state2 = transit(ops, 123456, self.state)
            self.assertEqual(self.state.next_op, ops)
            self.assertEqual(state2.last_op, ops)
            self.assertEqual(state2.duration, 123456)

    def test_count_same(self):
        self.state.last_op = "ZOOM_IN"
        state2 = transit("ZOOM_IN", 123456, self.state)
        self.assertEqual(self.state.count + 1, state2.count)

    def test_count_diff(self):
        self.state.last_op = "ZOOM_IN"
        self.state.count = 10
        state2 = transit("ZOOM_OUT", 123456, self.state)
        self.assertEqual(state2.count, 0)

    def test_zoom_in(self):
        state2 = transit("ZOOM_IN", 123456, self.state)
        self.assertEqual(self.state.z + 1, state2.z)

    def test_zoom_out(self):
        state2 = transit("ZOOM_OUT", 123456, self.state)
        self.assertEqual(self.state.z - 1, state2.z)

    def test_move_left(self):
        state2 = transit("MOVE_LEFT", 123456, self.state)
        self.assertEqual(self.state.x - 1, state2.x)
    
    def test_move_right(self):
        state2 = transit("MOVE_RIGHT", 123456, self.state)
        self.assertEqual(self.state.x + 1, state2.x)

    def test_move_up(self):
        state2 = transit("MOVE_UP", 123456, self.state)
        self.assertEqual(self.state.y + 1, state2.y)
    
    def test_move_down(self):
        state2 = transit("MOVE_DOWN", 123456, self.state)
        self.assertEqual(self.state.y - 1, state2.y)

    def test_tilt_forward(self):
        state2 = transit("TILT_FORWARD", 123456, self.state)
        self.assertEqual((self.state.ax - 1)%36, state2.ax)

    def test_tilt_backward(self):
        state2 = transit("TILT_BACKWARD", 123456, self.state)
        self.assertEqual((self.state.ax + 1)%36, state2.ax)

    def test_revolve_clockwise(self):
        state2 = transit("REVOLVE_CLOCKWISE", 123456, self.state)
        self.assertEqual((self.state.ay - 1)%36, state2.ay)
    
    def test_revolve_anticlockwise(self):
        state2 = transit("REVOLVE_ANTICLOCKWISE", 123456, self.state)
        self.assertEqual((self.state.ay + 1)%36, state2.ay)
    
    def test_rotate_clockwise(self):
        state2 = transit("ROTATE_CLOCKWISE", 123456, self.state)
        self.assertEqual((self.state.az + 1)%36, state2.az)
    
    def test_rotate_anticlockwise(self):
        state2 = transit("ROTATE_ANTICLOCKWISE", 123456, self.state)
        self.assertEqual((self.state.az - 1)%36, state2.az)

    def test_reset(self):
        state2 = transit("RESET", 123456, self.state)
        for i in [state2.x, state2.y, state2.z, \
                  state2.ax, state2.ay, state2.az]:
            self.assertEqual(i, 0)
    
    def test_reset(self):
        state2 = transit("BEGIN", 123456, self.state)
        for i in [state2.x, state2.y, state2.z, \
                  state2.ax, state2.ay, state2.az]:
            self.assertEqual(i, 0)

if __name__ == '__main__':
    unittest.main()
