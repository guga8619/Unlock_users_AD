import unittest
import sendemail

class TestUnlocker(unittest.TestCase):
    def test_sendemail(self):
        self.assertTrue(sendemail.sendEmail({"email":"email@email.com","user":"email_message_user_unlock","result":"result"}))
    
if __name__ == '__main__':
    unittest.main()