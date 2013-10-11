
import datetime
from operator import itemgetter, attrgetter

# can get sample data here:
# wget http://www.grouplens.org/system/files/ml-100k.zip
# app data file config
APPDATA_DIRNAME = "/tmp"
USERS_FILENAME = "u.user"
USERS_FILE_DELIMITER = "|"
ITEMS_FILENAME = "u.item"
ITEMS_FILE_DELIMITER = "|"
RATE_ACTIONS_FILENAME = "u.ratings"
RATE_ACTIONS_DELIMITER = "|"


class User:
	def __init__(self, uid):
		self.uid = uid
		self.rec = [] # recommendations, list of iid

	def __str__(self):
		return "User[uid=%s,rec=%s]" % (self.uid, self.rec)

class Item:
	def __init__(self, iid):
		self.iid = iid

	def __str__(self):
		return "Item[iid=%s]" % (self.iid)

class RateAction:
	def __init__(self, uid, iid, rating):
		self.uid = uid
		self.iid = iid
		self.rating = rating

	def __str__(self):
		return "RateAction[uid=%s,iid=%s,rating=%s]" % (self.uid, self.iid, self.rating)


class AppData:

	def __init__(self):
		self._users = {} # dict of User obj
		self._items = {} # dict of Item obj
		self._rate_actions = [] # list of RateAction obj

		self._users_file = "%s/%s" % (APPDATA_DIRNAME, USERS_FILENAME)
		self._items_file = "%s/%s" % (APPDATA_DIRNAME, ITEMS_FILENAME)
		self._rate_actions_file = "%s/%s" % (APPDATA_DIRNAME, RATE_ACTIONS_FILENAME)
		self.__init_users()
		self.__init_items()
		self.__init_rate_actions()

	def __init_users(self):
		"""
		uid|
		"""
		print "[Info] Initializing users..."
		f = open(self._users_file, 'r')
		for line in f:
			data = line.rstrip('\r\n').split(USERS_FILE_DELIMITER)
			self.add_user(User(data[0]))
		f.close()
		print "[Info] %s users were initialized." % len(self._users)

	def __init_items(self):
		"""
		iid|
		"""
		print "[Info] Initializing items..."
		f = open(self._items_file, 'r')
		for line in f:
			data = line.rstrip('\r\n').split(ITEMS_FILE_DELIMITER)
			self.add_item(Item(data[0]))
		f.close()
		print "[Info] %s items were initialized." % len(self._items)

	def __init_rate_actions(self):
		"""
		rating|iid|uid
		"""
		print "[Info] Initializing rate actions..."
		f = open(self._rate_actions_file, 'r')
		for line in f:
			data = line.rstrip('\r\n').split(RATE_ACTIONS_DELIMITER)
			self.add_rate_action(RateAction(data[2], data[1], data[0]))
		f.close()
		print "[Info] %s rate actions were initialized." % len(self._rate_actions)

	def add_user(self, user):
		self._users[user.uid] = user

	def add_item(self, item):
		self._items[item.iid] = item

	def add_rate_action(self, action):
		self._rate_actions.append(action)

	def get_users(self):
		return self._users

	def get_items(self):
		return self._items

	def get_rate_actions(self):
		return self._rate_actions

	def get_user(self, uid):
		"""return single user
		"""
		if uid in self._users:
			return self._users[uid]
		else:
			return None

	def get_item(self, iid):
		"""return single item
		"""
		if iid in self._items:
			return self._items[iid]
		else:
			return None

	def get_top_rated_items(self, uid, n):
		"""get top n rated iids by this uid
		"""
		if uid in self._users:
			actions = filter(lambda u: u.uid==uid, self._rate_actions)
			top = sorted(actions, key=attrgetter('rating'), reverse=True)
			topn_iids = map(lambda a: a.iid, top[:n])
			return topn_iids
		else:
			return None

	def get_top_rate_actions(self, uid, n):
		"""get top n rated actions by this uid
		"""
		if uid in self._users:
			actions = filter(lambda u: u.uid==uid, self._rate_actions)
			top = sorted(actions, key=attrgetter('rating'), reverse=True)
			return top[:n]
		else:
			return None
