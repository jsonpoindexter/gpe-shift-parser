import unittest

class TestUM(unittest.TestCase):

    def determin_training_credits(self,
        pre_event_shifts,
        main_event_shifts,
        pre_event_train_r,
        main_event_train_r
    ):
        if (pre_event_train_r + main_event_train_r) > 1: # either pre/main event shifts > 1
            # even
            if pre_event_train_r == main_event_train_r:
                pre_event_shifts -= pre_event_train_r - 1
                main_event_shifts -= main_event_train_r

            # pre-event > main-event
            if pre_event_train_r > main_event_train_r:
                pre_event_shifts -= pre_event_train_r - 1
                main_event_shifts -= main_event_train_r
            # pre-vent < main-event
            if pre_event_train_r < main_event_train_r:
                main_event_shifts -= main_event_train_r - 1
        return pre_event_shifts, main_event_shifts

    def test_1(self): # no training session
        self.assertEqual(self.determin_training_credits(1,1,0,0), (1,1))

    def test_2(self): # pre-event train: 1 main-event train: 0
        self.assertEqual(self.determin_training_credits(1,1,1,0), (1,1))

    def test_3(self): # pre-event train: 0 main-event train: 1
        self.assertEqual(self.determin_training_credits(1,1,0,1), (1,1))

    def test_4(self): # pre-event train: 2 main-event train: 0
        self.assertEqual(self.determin_training_credits(2,1,2,0), (1,1))

    def test_5(self): # pre-event train: 0 main-event train: 2
        self.assertEqual(self.determin_training_credits(1,2,0,2), (1,1))

    def test_6(self): # pre-event train: 2 main-event train: 2
        self.assertEqual(self.determin_training_credits(2,2,2,2), (1,0))

    def test_7(self): # pre-event train: 2 main-event train: 2
        self.assertEqual(self.determin_training_credits(3,2,2,2), (2,0))

    def test_8(self): # pre-event train: 2 main-event train: 2
        self.assertEqual(self.determin_training_credits(3,2,3,2), (1,0))

    def test_8(self): # pre-event train: 2 main-event train: 2
        self.assertEqual(self.determin_training_credits(2,2,2,0), (1,2))


if __name__ == '__main__':
    unittest.main()
