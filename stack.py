import unittest


class Stack(object):
    def __init__(self):
        self.data = []

    def empty(self):
        return self.data == []

    def push(self, v):
        self.data.append(v)

    def top(self):
        if not self.empty():
            return self.data[-1]

    def pop(self):
        self.data = self.data[0:-1]

    def __len__(self):
        return len(self.data)

    def poptop(self):
        p = self.top()
        self.pop()
        return p


class TestStack(unittest.TestCase):
    def test_empty(self):
        s = Stack()

        self.assertEqual(s.empty(), True)

    def test_push_once(self):
        s = Stack()

        s.push(2137)
        self.assertEqual(s.empty(), False)
        self.assertEqual(s.top(), 2137)

    def test_e2e(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.empty(), False)
        self.assertEqual(s.poptop(), 3)
        self.assertEqual(s.poptop(), 2)
        self.assertEqual(s.top(), 1)
        self.assertEqual(s.empty(), False)
        s.pop()
        self.assertEqual(s.empty(), True)


if __name__ == '__main__':
    unittest.main()
