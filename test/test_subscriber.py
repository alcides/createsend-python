import unittest

from createsend import Subscriber

class SubscriberTestCase(unittest.TestCase):

  def setUp(self):
    self.list_id = "d98h2938d9283d982u3d98u88"
    self.subscriber = Subscriber(self.list_id, "subscriber@example.com")

  def test_get(self):
    email = "subscriber@example.com"
    self.subscriber.stub_request("subscriber_details.json")
    subscriber = self.subscriber.get(self.list_id, email)
    self.assertEquals(subscriber.EmailAddress, email)
    self.assertEquals(subscriber.Name, "Subscriber One")
    self.assertEquals(subscriber.Date, "2010-10-25 10:28:00")
    self.assertEquals(subscriber.State, "Active")
    self.assertEquals(len(subscriber.CustomFields), 3)
    self.assertEquals(subscriber.CustomFields[0].Key, 'website')
    self.assertEquals(subscriber.CustomFields[0].Value, 'http://example.com')

  def test_add_without_custom_fields(self):
    self.subscriber.stub_request("add_subscriber.json")
    email_address = self.subscriber.add(self.list_id, "subscriber@example.com", "Subscriber", [], True)
    self.assertEquals(email_address, "subscriber@example.com")

  def test_add_with_custom_fields(self):
    self.subscriber.stub_request("add_subscriber.json")
    custom_fields = [ { "Key": 'website', "Value": 'http://example.com/' } ]
    email_address = self.subscriber.add(self.list_id, "subscriber@example.com", "Subscriber", custom_fields, True)
    self.assertEquals(email_address, "subscriber@example.com")

  def test_import(self):
    self.subscriber.stub_request("import_subscribers.json")
    subscribers = [
      { "EmailAddress": "example+1@example.com", "Name": "Example One" },
      { "EmailAddress": "example+2@example.com", "Name": "Example Two" },
      { "EmailAddress": "example+3@example.com", "Name": "Example Three" },
    ]
    import_result = self.subscriber.import_subscribers(self.list_id, subscribers, True)
    self.assertEquals(len(import_result.FailureDetails), 0)
    self.assertEquals(import_result.TotalUniqueEmailsSubmitted, 3)
    self.assertEquals(import_result.TotalExistingSubscribers, 0)
    self.assertEquals(import_result.TotalNewSubscribers, 3)
    self.assertEquals(len(import_result.DuplicateEmailsInSubmission), 0)

  def test_ubsubscribe(self):
    self.subscriber.stub_request(None)
    self.subscriber.unsubscribe()
  
  def test_history(self):
    self.subscriber.stub_request("subscriber_history.json")
    history = self.subscriber.history()
    self.assertEquals(len(history), 1)
    self.assertEquals(history[0].Name, "Campaign One")
    self.assertEquals(history[0].Type, "Campaign")
    self.assertEquals(history[0].ID, "fc0ce7105baeaf97f47c99be31d02a91")
    self.assertEquals(len(history[0].Actions), 6)
    self.assertEquals(history[0].Actions[0].Event, "Open")
    self.assertEquals(history[0].Actions[0].Date, "2010-10-12 13:18:00")
    self.assertEquals(history[0].Actions[0].IPAddress, "192.168.126.87")
    self.assertEquals(history[0].Actions[0].Detail, "")